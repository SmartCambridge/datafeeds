#!/usr/bin/env python3

'''
Download countline data for one or more days and store it
in json files in ACP style
'''


import argparse
import json
import os
import sys
import time as stdlib_time

from datetime import datetime, time, timedelta, timezone

import dateutil.parser

import requests

from graphit_base import COUNTLINES, VCLASSES

FIVE_MINUTES = timedelta(minutes=5)
ONE_HOUR = timedelta(hours=1)
ONE_DAY = timedelta(days=1)
MIDNIGHT = time(tzinfo=timezone.utc)


username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

token = None


def vivacity_time(t):
    '''
    Return t as a string in the particular version of ISO8601
    expected by the Vivacity API
    '''

    return (t.astimezone(tz=timezone.utc)
            .replace(tzinfo=None)
            .isoformat(timespec='milliseconds') + 'Z')


def get_token():

    print('Getting a new token', file=sys.stderr)

    assert username is not None and password is not None, (
        'USERNAME and/or PASSWORD environment variable missing')

    r = requests.post(
        'https://api.vivacitylabs.com/get-token',
        data={'username': username, 'password': password},
        headers={'api-version': '2'}
    )
    r.raise_for_status()
    global token
    token = r.json()
    token['ts'] = datetime.utcnow()


def get_data(start, duration):
    '''
    Get raw data for time range `start` to `start+duration`
    '''

    params = {
        'timeFrom': vivacity_time(start),
        'timeTo': vivacity_time(start+duration),
    }

    retries = 0

    while True:

        print('Trying {} from {}'.format(duration, start.isoformat()))

        # Get or renew the token as needed
        if not token or (datetime.utcnow()-token['ts']).total_seconds() > 0.9*token['expires_in']:
            get_token()

        headers = {
            'api-version': '2',
            'Authorization': 'Bearer ' + token['access_token']
        }

        r = requests.get(
            'https://api.vivacitylabs.com/counts',
            params=params,
            headers=headers
        )

        if r.ok or retries > 10:
            break

        print("Error: {} {} - retrying in {} sec".format(r.status_code, r.reason, 30 * retries))
        if retries > 0:
            stdlib_time.sleep(30 * retries)

        retries += 1

    r.raise_for_status()

    if r.status_code == 204:
        return {}
    else:
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
    Add API response data in `response` to `results` for each countline
    in COUNTLINES, assuming that `response` contains data for the period
    `start` to `start+duration` in 5 minute lumps.

    Include counts for all countlines, for all possible classes of vehicle
    (even if zero) and data for every 5 minute lump, even if all readings
    are zero (which is why we need COUNLINES, VCLASSES and `start` and
    `duration` - we can't derive them from what's in `results` because
    it could in principle be empty)

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
    for countline in COUNTLINES:
        countline_data = response.get(countline, {})

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


def get_day(date, path):
    '''
    Get data for one day in one hour chunks and store it
    '''

    print('Processing', date, file=sys.stderr)

    time = datetime.combine(date, MIDNIGHT)
    results = {}

    for counter in range(24):
        response = get_data(time, ONE_HOUR)
        accumulate_data(results, response, time, ONE_HOUR)
        time = time + ONE_HOUR

    store_data(results, path)


def get_days(start, end, path):
    '''
    Get data for each day from `start` to `end` inclusive and store
    it in the directory `path`
    '''
    day = start
    while day <= end:
        get_day(day, path)
        day += ONE_DAY


def parse_args():

    parser = argparse.ArgumentParser(epilog='''
        <first> and <last> can be anything dateutil.parser.parse understands
        ''')

    parser.add_argument('last', type=dateutil.parser.parse,
                        default=(datetime.now()-ONE_DAY), nargs='?',
                        help='last (or only) day to download (default yesterday)')
    parser.add_argument('--dest', default='vivacity_data',
                        help='directory in which to store data (default \'%(default)s\')')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--first', '-f', type=dateutil.parser.parse,
                       help='first day to download')
    group.add_argument('--days', '-d', type=int, help='number of days to download')

    args = parser.parse_args()

    if args.days:
        args.first = args.last - timedelta(days=args.days - 1)
    elif args.first is None:
        args.first = args.last

    return args


def run():

    params = parse_args()

    get_days(params.first.date(), params.last.date(), params.dest)


if __name__ == '__main__':
    run()
