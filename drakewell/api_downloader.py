#!/usr/bin/env python3

# Download location and journey data from the Drakewell API and store
# it in a way that mimics what tfc_server is going to do

import itertools
import json
import os
import requests
import shutil

from datetime import datetime, timezone

LOCATIONS_URL = os.getenv('LOCATIONS_URL')
assert LOCATIONS_URL, 'LOCATIONS_URL not set'
JOURNEYS_URL = os.getenv('JOURNEYS_URL')
assert JOURNEYS_URL, 'JOURNEYS_URL not set'

OUTDIR = 'drakewell'

now = datetime.now(tz=timezone.utc)


def process_journeys():
    r = requests.get(JOURNEYS_URL)
    r.raise_for_status()

    request_data = {'request_data': r.json(),
                    'ts': int(now.timestamp())}

    # data_bin - all the data as received, into
    # data_bin/<YYYY>/<MM>/<DD>/<EPOC>_<YYYY>-<MM>-<DD>-<HH>-<MM>-<SS>.json

    save_file = os.path.join(
        OUTDIR,
        'link_data',
        'data_bin',
        '{0:%Y}',
        '{0:%m}',
        '{0:%d}',
        '{1}_{0:%Y}-{0:%m}-{0:%d}-{0:%H}-{0:%M}-{0:%S}.json').format(now, int(now.timestamp()))

    os.makedirs(os.path.dirname(save_file), exist_ok=True)
    with open(save_file, mode='w') as s:
        json.dump(request_data, s)

    # data_monitor - most recent data received
    # info dada_monitor/post_data.json (previous in post_data.json.prev)

    pid = os.getpid()

    current = os.path.join(
        OUTDIR,
        'link_data',
        'data_monitor',
        'post_data.json'
    )
    current_temp = '{}.{}'.format(current, pid)
    old = '{}.prev'.format(current)
    old_temp = '{}.{}'.format(old, pid)

    os.makedirs(os.path.dirname(current), exist_ok=True)

    try:
        shutil.copyfile(current, old_temp)
        os.rename(old_temp, old)
    except FileNotFoundError:
        pass

    with open(current_temp, mode='w') as s:
        json.dump(request_data, s)
    os.rename(current_temp, current)

    # data link - data broken down by day and link id
    # into data_link//<YYYY>/<MM>/<DD>/<LINK_ID>.txt

    save_dir = os.path.join(
        OUTDIR,
        'link_data',
        'data_link',
        '{0:%Y}',
        '{0:%m}',
        '{0:%d}'
    ).format(now)
    os.makedirs(save_dir, exist_ok=True)

    for record in request_data['request_data']:
        record['ts'] = request_data['ts']
        with open(os.path.join(save_dir, record['id'] + '.txt'), mode='a') as f:
            f.write(json.dumps(record))
            f.write('\n')


def process_locations():
    loc = requests.get(LOCATIONS_URL)
    loc.raise_for_status()

    request_data = {'request_data': loc.json(),
                    'ts': int(now.timestamp())}

    # data_bin - all the data as received, into
    # data_bin/<YYYY>/<MM>/<DD>/<EPOC>_<YYYY>-<MM>-<DD>-<HH>-<MM>-<SS>.json

    save_file = os.path.join(
        OUTDIR,
        'locations',
        'data_bin',
        '{0:%Y}',
        '{0:%m}',
        '{0:%d}',
        '{1}_{0:%Y}-{0:%m}-{0:%d}-{0:%H}-{0:%M}-{0:%S}.json').format(now, int(now.timestamp()))

    os.makedirs(os.path.dirname(save_file), exist_ok=True)
    with open(save_file, mode='w') as s:
        json.dump(request_data, s)

    # data_monitor - most recent data received
    # info dada_monitor/post_data.json (previous in post_data.json.prev)

    pid = os.getpid()

    current = os.path.join(
        OUTDIR,
        'locations',
        'data_monitor',
        'post_data.json'
    )
    current_temp = '{}.{}'.format(current, pid)
    old = '{}.prev'.format(current)
    old_temp = '{}.{}'.format(old, pid)

    os.makedirs(os.path.dirname(current), exist_ok=True)

    try:
        shutil.copyfile(current, old_temp)
        os.rename(old_temp, old)
    except FileNotFoundError:
        pass

    with open(current_temp, mode='w') as s:
        json.dump(request_data, s)
    os.rename(current_temp, current)

    # data link - data for links and compoundRoutes broken down by day
    # and link id into data_link/<LINK_ID>.json

    save_dir = os.path.join(
        OUTDIR,
        'locations',
        'data_link'
    ).format(now)
    os.makedirs(save_dir, exist_ok=True)

    for record in itertools.chain(
          request_data['request_data']['links'],
          request_data['request_data']['compoundRoutes']):
        record['ts'] = request_data['ts']
        with open(os.path.join(save_dir, record['id'] + '.json'), mode='w') as f:
            json.dump(record, f)


    # data site - data for sites broken down by day
    # and link id into data_site/<SITE_ID>.json

    save_dir = os.path.join(
        OUTDIR,
        'link_metadata',
        'data_site'
    ).format(now)
    os.makedirs(save_dir, exist_ok=True)

    for record in request_data['request_data']['sites']:
        record['ts'] = request_data['ts']
        with open(os.path.join(save_dir, record['id'] + '.json'), mode='w') as f:
            json.dump(record, f)


process_journeys()
process_locations()
