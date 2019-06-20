#!/usr/bin/env python3

'''

'''

import datetime
import json
import os
import time

from collections import defaultdict

import requests

from deepdiff import DeepDiff
from dateutil.parser import parse

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

    token = get_token()

    now = datetime.datetime.now()

    print("Now: ", now.isoformat())

    first_counts = get_counts(token, countlines=['13074'])

    start = parse(first_counts['13074']['from'])
    end = parse(first_counts['13074']['to'])

    print("Initial from: ", first_counts['13074']['from'], start.isoformat())
    print("Initial to: ", first_counts['13074']['to'], end.isoformat())

    for ctr in range(20):

        time.sleep(5)

        second_counts = get_counts(token, countlines=['13074'], start=start, end=end)

        print(ctr, ': ', json.dumps(DeepDiff(first_counts, second_counts), indent=4))

        first_counts = second_counts


if __name__ == '__main__':
    run()
