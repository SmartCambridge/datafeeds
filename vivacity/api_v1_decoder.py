#!/usr/bin/env python3

import datetime
import requests
import time

SOURCE = 'https://api.vivacitylabs.com/cambridge-mill-road/v1/counts'
req_params = {'apikey': 'deSwbTn3duihqRLyvgfFGdvft2w28nhKthPWa'}

# Top of the next minute
next = datetime.datetime.now().replace(second=0, microsecond=0) + datetime.timedelta(minutes=1)
#print(F'Start at {next}')

for x in range(100):

    # Sleep to our next run time
    delay = (next - datetime.datetime.now()).total_seconds()
    #print(F'Sleeping for {delay}')
    time.sleep(delay)

    now = datetime.datetime.now()
    r = requests.get(SOURCE, req_params)
    r.raise_for_status()

    all_data = r.json()

    device = all_data[0]
    #print(F'Device {device["deviceId"]}')

    countline = device['countlines'][0]

    id = countline["countlineId"]

    f = datetime.datetime.fromtimestamp(countline["fromTime"]/1000)
    t = datetime.datetime.fromtimestamp(countline["toTime"]/1000)

    d = t-f

    print(F'{id} - {now}: from={f:%H:%M:%S.%f} to={t:%H:%M:%S.%f} {d}', flush=True)

    # Schedule the next run in 5 seconds
    next = next + datetime.timedelta(seconds=5)
