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
        params['timeFrom'] = start.isoformat(timespec='milliseconds') + 'Z'
    if end:
        params['timeTo'] = end.isoformat(timespec='milliseconds') + 'Z'

        print('start: ', start, 'end: ', end)

    r = requests.get(
        'https://api.vivacitylabs.com/counts',
        params=params,
        headers=headers
    )
    r.raise_for_status()
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
            print('slice from: ', slice['from'], 'slice to: ', slice['to'])
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

    start_time = datetime.datetime(2019, 6, 17, 8, 0)
    steps = 10
    step = datetime.timedelta(seconds=62)

    # #1: get data in 1 minute steps from `start_time` to `end_time`

    time = start_time
    result1 = {}
    for ctr in range(steps):

        counts = get_counts(token, countlines=['13074'], start=time, end=time+step)
        # print(json.dumps(counts))

        for countline, line_data in counts.items():
            if countline not in result1:
                result1[countline] = {'from': None, 'to': None, 'counts': {}}
            result1[countline]['from'] = (line_data['from'] if result1[countline]['from'] is None
                                          else min(result1[countline]['from'], line_data['from']))
            result1[countline]['to'] = (line_data['to'] if result1[countline]['to'] is None
                                        else max(result1[countline]['to'], line_data['to']))
            for vclass in line_data['counts']:
                if vclass not in result1[countline]['counts']:
                    result1[countline]['counts'][vclass] = {'countIn': 0, 'countOut': 0}
                result1[countline]['counts'][vclass]['countIn'] += (
                    line_data['counts'][vclass]['countIn'])
                result1[countline]['counts'][vclass]['countOut'] += (
                    line_data['counts'][vclass]['countOut'])

        time += step

    # #2: get the same data in a single step

    result2 = get_counts(token, countlines=['13074'], start=start_time, end=start_time+(step*steps))

    print(json.dumps(result1, indent=4))
    print()
    print(json.dumps(result2, indent=4))

    diff = DeepDiff(result2, result1)
    if diff:
        print()
        print("Differences")
        print()
        print(json.dumps(diff, indent=4))


if __name__ == '__main__':
    run()
