#!/usr/bin/env python3

'''

'''

import datetime
import json
import os

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
            #print(slice)
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

    token = get_token()

    now = datetime.datetime.now()

    print('Now: ', now)

    steps = 40
    step = datetime.timedelta(seconds=15)
    start_time = (now-((steps//2)*step)).replace(second=0, microsecond=0)
    # #1: get data in 1 minute steps from `start_time` to `end_time`

    time = start_time
    for ctr in range(steps):

        counts = get_counts(token, countlines=['13074'], start=time, end=time+step)

        print(time.isoformat(), len(counts))

        time += step



if __name__ == '__main__':
    run()
