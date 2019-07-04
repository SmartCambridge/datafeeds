#!/usr/bin/env python3

'''
Download countline data for one or more days and store it
in json files in ACP style
'''


import argparse
import json
import os
import sys

from datetime import datetime, date, time, timedelta, timezone

import dateutil.parser

import requests

FIVE_MINUTES = timedelta(minutes=5)
ONE_HOUR = timedelta(hours=1)
ONE_DAY = timedelta(days=1)
MIDNIGHT = time(tzinfo=timezone.utc)

VCLASSES = (
    "pedestrian", "cyclist", "motorbike", "car", "taxi", "van",
    "minibus", "bus", "rigid", "truck", "emergency car",
    "emergency van", "fire engine"
)


username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')


def vivacity_time(t):
    '''
    Return t as a string in the particular version of ISO8601
    expected by the Vivacity API
    '''

    return (t.astimezone(tz=timezone.utc)
            .replace(tzinfo=None)
            .isoformat(timespec='milliseconds') + 'Z')


def get_token():

    assert username is not None and password is not None, (
        'USERNAME and/or PASSWORD environment variable missing')

    r = requests.post(
        'https://api.vivacitylabs.com/get-token',
        data={'username': username, 'password': password},
        headers={'api-version': '2'}
    )
    r.raise_for_status()
    all_data = r.json()
    return all_data['access_token']


def get_data(token, start, duration):
    '''
    Get raw data for time range `start` to `start+duration`
    '''

    headers = {
        'api-version': '2',
        'Authorization': 'Bearer ' + token
    }

    params = {
        'timeFrom': vivacity_time(start),
        'timeTo': vivacity_time(start+duration),
    }

    r = requests.get(
        'https://api.vivacitylabs.com/counts',
        params=params,
        headers=headers
    )
    r.raise_for_status()
    return r.json()


def store_data(results, directory):
    '''
    Store the data in `results` in conventional ACP format in `directory`

    Results:
    {
      <date>: {
        <countline>: {
          <direction>: [
            {
              time: <timestamp>,
              counts: {
                <class>: count,
              ...
            },
            ...
          ],
          ...
        },
        ...
      },
      ...
    }

    '''

    for this_date, day_data in results.items():

        day_dir = os.path.join(
            directory,
            this_date.strftime('%Y'),
            this_date.strftime('%m'),
            this_date.strftime('%d'))
        os.makedirs(day_dir, exist_ok=True)

        for countline, countline_data in day_data.items():

            countline_dir = os.path.join(day_dir, countline)
            os.makedirs(countline_dir, exist_ok=True)

            for direction, count_blocks in countline_data.items():

                filename = os.path.join(countline_dir, direction + '.txt')
                with open(filename, 'w') as file:
                    for count_block in count_blocks:
                        json.dump(count_block, file)
                        file.write('\n')


def accumulate_data(results, response, start, duration):
    '''
    Add API response data in `response` to `results`, assuming that
    `response` contains data for the period `start` to `start+duration`
    in 5 minute lumps.

    Include counts for all possible classes of vehicle (even if zero)
    and data for every 5 minute lump, even if all readings are zero (which
    is why we need `start` and `duration` - we can't derive them from
    what's in `results` because it could in principle be empty)

    API data:

    {
      <countline>: {
        <from>: {
          "from": <from>,
          "to": <to>
          "counts": [
            {
              "class": <class>,
              "countIn": <count>,
              "countOut": <count>
            },
            ...
          ]
        },
        ...
      },
      ...
    }

    Results has a top-level grouping by `date` to make directory and
    file management easier.

    Results:
    {
      <date>: {
        <countline>: {
          <direction>: [
            {
              time: <timestamp>,
              counts: {
                <class>: count,
              ...
            },
            ...
          ],
          ...
        },
        ...
      },
      ...
    }

    '''

    # For each countline in `response`...
    for countline, countline_data in response.items():

        # ...loop over the timestamped observations
        this_time = start
        while this_time < start+duration:

            date = this_time.date()
            observation = countline_data.get(vivacity_time(this_time), {'counts': []})

            # Add empty dicts to `results` as needed
            if date not in results:
                results[date] = {}
            if countline not in results[date]:
                results[date][countline] = {}

            # For each possible direction
            for their_direction, our_direction in {'countIn': 'in', 'countOut': 'out'}.items():

                # Add an empty list if needed
                if our_direction not in results[date][countline]:
                    results[date][countline][our_direction] = []

                # populate a results block and append it to results
                block = {
                    'ts': this_time.timestamp(),
                    'timestamp': this_time.isoformat(),
                    'from': observation.get('from', None),
                    'to': observation.get('to', None),
                    'countline': countline,
                    'direction': our_direction,
                    'counts': {vclass: 0 for vclass in VCLASSES}
                }
                for count in observation['counts']:
                    block['counts'][count['class']] = count[their_direction]
                results[date][countline][our_direction].append(block)

            this_time += FIVE_MINUTES


def get_day(token, date, path):
    '''
    Get data for one day in one hour chunks and store it
    '''

    print('Processing', date, file=sys.stderr)

    time = datetime.combine(date, MIDNIGHT)
    results = {}

    for counter in range(24):
        response = get_data(token, time, ONE_HOUR)
        accumulate_data(results, response, time, ONE_HOUR)
        time = time + ONE_HOUR

    store_data(results, path)


def get_days(token, start, end, path):
    '''
    Get data for each day from `start` to `end` inclusive and store
    it in the directory `path`
    '''
    day = start
    while day <= end:
        get_day(token, day, path)
        day += ONE_DAY


def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument('start', help='first (or only) day to download')
    parser.add_argument('--end', '-e', help='last day to download')
    parser.add_argument('--dest', '-d', default='vivacity_data', help='directory in which to store data')

    args = parser.parse_args()

    try:
        args.start = dateutil.parser.parse(args.start).date()
        if args.end:
            args.end = dateutil.parser.parse(args.end).date()
        else:
            args.end = args.start
    except ValueError as e:
        print(e.args, file=sys.stderr)
        sys.exit(1)

    return args

def run():

    params = parse_args()

    token = get_token()

    get_days(token, params.start, params.end, params.dest)


if __name__ == '__main__':
    run()
