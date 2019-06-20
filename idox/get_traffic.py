#!/usr/bin/env python3

import os

import xml.etree.ElementTree as et

import requests
from tabulate import tabulate

ns = {'d2': 'http://datex2.eu/schema/1_0/1_0',
      'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

url = 'http://91.151.215.136/CloudAmber/CambsDateXII/pox/GetDateXIITrafficData'
params = {'Easting': 0, 'EastingEnd': 999999, 'Northing': 0,  'NorthingEnd': 999999}
auth = (username, password)


def run():

    data = requests.get(url=url, params=params, auth=auth)

    tree = et.fromstring(data.text)

    results = []

    for data in tree.findall('.//d2:elaboratedData', ns):
        data_value = data.find('d2:basicDataValue', ns)

        type = data_value.get('{http://www.w3.org/2001/XMLSchema-instance}type')
        time = data_value.findtext('d2:time', '', ns)
        location_ref = data_value.findtext('d2:affectedLocation/d2:locationContainedInGroup/d2:predefinedLocationReference', '', ns)

        vehicle_flow = data_value.findtext('d2:vehicleFlow', '-', ns)

        occupancy = data_value.findtext('d2:occupancy', '-', ns)

        travel_time = data_value.findtext('d2:travelTime', '-', ns)

        results.append({
           'type': type, 'time': time, 'location': location_ref,
           'vehicle_flow': vehicle_flow, 'occupancy': occupancy,
           'travel_time': travel_time})

    results.sort(key=lambda r: r['type'] + r['time'])

    print(tabulate(results, headers='keys'))


if __name__ == '__main__':
    run()
