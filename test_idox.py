#!/usr/bin/env python3

import collections
import json
import time

import requests

BASE = 'http://91.151.215.136/CloudAmber'

FORMATS = {
    'Json': 'Cambs1DateXII/Json',
    'XML': 'CambsDateXII/pox',
}

PARAMS1TO4 = {
    'Easting': 0,
    'EastingEnd': 999999,
    'Northing': 0,
    'NorthingEnd': 999999,
}

PARAMS1TO6 = dict(PARAMS1TO4)
PARAMS1TO6.update({
    'startDate': '01-May-2019',
    'endDate': '30-May-2019',
})

PARAM7 = {
    'Value': 1,
}

ENDPOINTS = [
    {'name': 'Events',
     'method': 'Events',
     'params': PARAMS1TO6,
     },
    {'name': 'Road Works',
     'method': 'RoadWorks',
     'params': PARAMS1TO6,
     },
    {'name': 'Traffic Data',
     'method': 'TrafficData',
     'params': PARAMS1TO4,
     },
    {'name': 'Traffic Data Extension',
     'method': 'TrafficDataExtension',
     'params': PARAMS1TO4,
     },
    {'name': 'Variable Message Sign',
     'method': 'AllVMS',
     'params': PARAMS1TO4,
     },
    {'name': 'Car Park (v1.0)',
     'method': 'CarPark',
     'params': PARAMS1TO4,
     },
    {'name': 'Car Park (v2.2.0)',
     'method': 'CarPark20',
     'params': PARAMS1TO4,
     },
    {'name': 'CCTV',
     'method': 'CCTV',
     'params': PARAMS1TO4,
     },
    {'name': 'Journey Times - Current',
     'method': 'TransportRouteJourneyTime',
     'params': PARAMS1TO4,
     },
    {'name': 'Journey Times - Predictive',
     'method': 'TransportRoutePredictiveJourneyTimes',
     'params': PARAM7,
     },
    {'name': 'CycleHubs',
     'method': 'CycleHubs',
     'params': PARAMS1TO4,
     },
    {'name': 'EV Charging Points',
     'method': 'EVChargingPoints',
     'params': PARAMS1TO4,
     },
    {'name': 'Walkers Facilities',
     'method': 'WalkersFacilities',
     'params': PARAMS1TO4,
     },
    {'name': 'Point of Interest',
     'method': 'PointOfInterest',
     'params': PARAMS1TO4,
     },
    {'name': 'Meteorological',
     'method': 'Meteorological',
     'params': PARAMS1TO4,
     },
]

LOCATIONS = [
    {'name': 'PredefinedLocation(Traffic Data)',
     'param': 'link',
     },
    {'name': 'PredefinedLocation(Traffic Data Section)',
     'param': 'section',
     },
    {'name': 'PredefinedLocation(VMS)',
     'param': 'vms',
     },
    {'name': 'PredefinedLocation(Matrix)',
     'param': 'matrix',
     },
    {'name': 'PredefinedLocation(Journey Time Sections)',
     'param': 'tr',
     },
    {'name': 'PredefinedLocation(CCTV)',
     'param': 'cctv',
     },
]

AUTH = ('CambsUni', 'P8MSatsW9L3')

results = collections.OrderedDict()

for endpoint in ENDPOINTS:

    results[endpoint['name']] = {}

    for format_name, format_fragment in FORMATS.items():

        url = '{}/{}/GetDateXII{}'.format(BASE, format_fragment, endpoint['method'])
        print('Format: {}, method {}'.format(format_fragment, endpoint['name']))

        try:
            r = requests.get(url, params=endpoint['params'], auth=AUTH)
            print('URL: {}'.format(r.url))
            print('Status: {}, Length: {}, Content type: {}'.format(
                r.status_code, r.headers.get('Content-Length'), r.headers.get('Content-type')))
            results[endpoint['name']][format_name] = {'status': r.status_code, 'size': r.headers.get('Content-Length')}
        except requests.exceptions.ConnectionError:
            print('Connection reset')
            results[endpoint['name']][format_name] = {'status': 'reset', 'size': None}
        print()
        time.sleep(10)

for location in LOCATIONS:

    results[location['name']] = {}

    for format_name, format_fragment in FORMATS.items():

        url = '{}/{}/GetDateXIIPredefinedLocation'.format(BASE, format_fragment)
        params = {'type': location['param']}

        print('Format: {}, location {}'.format(format_fragment, location['param']))
        try:
            r = requests.get(url, params=params, auth=AUTH)
            print('URL: {}'.format(r.url))
            print('Status: {}, Length: {}, Content-type: {}'.format(
                r.status_code, r.headers.get('Content-Length'), r.headers.get('Content-type')))
            results[location['name']][format_name] = {'status': r.status_code, 'size': r.headers.get('Content-Length')}
        except requests.exceptions.ConnectionError:
            print('Connection reset')
            results[location['name']][format_name] = {'status': 'reset', 'size': None}
        print()
        time.sleep(10)


print('{:45} | {:^15} | {:^15}'.format(
        '', 'Json', 'XML'))
print('{:45} | {:>6} {:>8} | {:>6} {:>8}'.format(
        'Method', 'Status', 'Size', 'Status', 'Size'))
print('--------------------------------------------- | ------ | ------ | ------ | ------')

for method in results:
    result = results[method]
    print('{:45} | {:>6} {:>8} | {:>6} {:>8}'.format(
        method,
        result['Json']['status'],
        result['Json']['size'] or '',
        result['XML']['status'],
        result['XML']['size'] or '',
        ))
