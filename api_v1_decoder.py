#!/usr/bin/env python3

import datetime
import requests
import time

SOURCE = 'https://api.vivacitylabs.com/cambridge-mill-road/v1/counts'
req_params = {'apikey': 'deSwbTn3duihqRLyvgfFGdvft2w28nhKthPWa'}

for x in range(100):

    now = datetime.datetime.now()
    r = requests.get(SOURCE, req_params)
    r.raise_for_status()

    all_data = r.json()

    device = all_data[0]
    #print(F'Device {device["deviceId"]}')

    countline = device['countlines'][0]

    f = datetime.datetime.fromtimestamp(countline["fromTime"]/1000)
    t = datetime.datetime.fromtimestamp(countline["toTime"]/1000)

    d = t-f

    print(F'{now}: from {f} to {t} ({d})')

    time.sleep(5)