#!/usr/bin/env python3

import datetime
import os
import time

import xml.etree.ElementTree as et

import requests
from tabulate import tabulate

ns = {'d2': 'http://datex2.eu/schema/2/2_0'}

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

url = 'http://91.151.215.136/CloudAmber/CambsDateXII/pox/GetDateXIICarPark20'
params = {'Easting': 0, 'EastingEnd': 999999, 'Northing': 0,  'NorthingEnd': 999999}
auth = (username, password)


def get_data():

    data = requests.get(url=url, params=params, auth=auth)

    tree = et.fromstring(data.text)

    results = []

    for area_status in tree.findall('.//d2:parkingAreaStatus', ns):
        facility_status = area_status.find('d2:parkingFacilityStatus', ns)

        id = facility_status.find('d2:parkingFacilityReference', ns).get('id')

        exit_rate = int(facility_status.findtext('d2:parkingFacilityExitRate', '', ns))
        fill_rate = int(facility_status.findtext('d2:parkingFacilityFillRate', '', ns))
        occupancy = int(facility_status.findtext('d2:parkingFacilityOccupancy', '', ns))
        trend = facility_status.findtext('d2:parkingFacilityOccupancyTrend', '', ns)
        status = facility_status.findtext('d2:parkingFacilityStatus', '', ns)
        timestamp = facility_status.findtext('d2:parkingFacilityStatusTime', '', ns)

        parking_area = tree.find(f".//d2:parkingArea[@id='{id}']", ns)

        name = parking_area.findtext('d2:parkingAreaName/d2:values/d2:value', '', ns)
        capacity = int(parking_area.findtext('d2:totalParkingCapacity', '', ns))

        now = datetime.datetime.now().isoformat(timespec='seconds')

        results.append({'time': now, 'timestamp': timestamp, 'id': id, 'name': name, 'capacity': capacity,
            'occupancy': occupancy, 'free': capacity-occupancy, 'fill_rate': fill_rate,
            'exit_rate': exit_rate, 'trend': trend, 'status': status})

    return results


def run():

    previous_timestamp = None

    while True:
        results = get_data()
        if results[0]['timestamp'] != previous_timestamp:
            print(tabulate(results, headers='keys'))
            previous_timestamp = results[0]['timestamp']
        time.sleep(5)


if __name__ == '__main__':
    run()
