#!/usr/bin/env python3

'''
Keep fetching counts for the same time interval which runs for 15 minutes
from when the script starts. Report each time the returned count data changes.
'''

import datetime
import os
import time

from collections import defaultdict

import requests

from deepdiff import DeepDiff

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')


def get_token():

    r = requests.post(
        'https://api.vivacitylabs.com/get-token',
        data={'username': username, 'password': password},
        headers={'api-version': '2'}
    )
    r.raise_for_status()

    all_data = r.json()
    return all_data['access_token']


def format_datetime(t):
    '''
    Format t as a string acceptable to the Vivacity API. Specifically,
    in UTC in exactly the format YYYY-MM-DDTHH-MM-SS.MMMZ
    '''

    return (t.astimezone(tz=datetime.timezone.utc)
            .replace(tzinfo=None)
            .isoformat(timespec='milliseconds') + 'Z')


def get_counts(token, countlines=[], classes=[], start=None, end=None):

    headers = {
        'api-version': '2',
        'Authorization': 'Bearer ' + token
    }

    params = {
        'countline': countlines,
        'class': classes,
    }
    if start:
        params['timeFrom'] = format_datetime(start)
    if end:
        params['timeTo'] = format_datetime(end)

    r = requests.get(
        'https://api.vivacitylabs.com/counts',
        params=params,
        headers=headers
    )
    r.raise_for_status()
    if r.status_code != 200:
        return {}
    raw_data = r.json()

    # Counts are returned as a list of up to 5 minute 'slices' of the full
    # time range requested. Merge these down to a single dictionary

    data = {}
    for countline, slices in raw_data.items():
        start = None
        end = None
        counts = defaultdict(lambda: dict(countIn=0, countOut=0))
        for slice in slices.values():
            start = slice['from'] if start is None else min(start, slice['from'])
            end = slice['to'] if end is None else max(end, slice['to'])
            for count in slice['counts']:
                counts[count['class']]['countIn'] += count['countIn']
                counts[count['class']]['countOut'] += count['countOut']
        data[countline] = {
            'from': start,
            'to': end,
            'counts': dict(counts)
        }

    return data


def run():

    # Top of the next minute
    start = ((datetime.datetime.now() + datetime.timedelta(minutes=1))
             .replace(second=0, microsecond=0))
    # 15 minutes later
    end = start+datetime.timedelta(minutes=15)

    pause = (start-datetime.datetime.now()).total_seconds()
    print('Sleeping', pause, 'seconds to the top of the next minute')
    time.sleep(pause)

    token = get_token()

    first_counts = get_counts(token, countlines=['13074'], start=start, end=end)
    print('Start:', start.isoformat())

    next = start
    while next < end:

        next += datetime.timedelta(seconds=5)
        pause = (next-datetime.datetime.now()).total_seconds()
        time.sleep(pause)

        second_counts = get_counts(token, countlines=['13074'], start=start, end=end)

        diff = DeepDiff(first_counts, second_counts)

        if diff:
            print('Change:', datetime.datetime.now().isoformat())

        first_counts = second_counts
        # Refresh the token in case it times out
        token = get_token()


if __name__ == '__main__':
    run()
