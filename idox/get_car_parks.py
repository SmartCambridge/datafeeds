#!/usr/bin/env python3

import os

import xml.etree.ElementTree as et

import requests
from tabulate import tabulate

ns = {'d2': 'http://datex2.eu/schema/1_0/1_0'}

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

url = 'http://91.151.215.136/CloudAmber/CambsDateXII/pox/GetDateXIICarPark'
params = {'Easting': 0, 'EastingEnd': 999999, 'Northing': 0,  'NorthingEnd': 999999}
auth = (username, password)


def run():

    data = requests.get(url=url, params=params, auth=auth)

    tree = et.fromstring(data.text)

    results = []

    for situation in tree.findall('.//d2:situation', ns):
        situation_record = situation.find('d2:situationRecord', ns)

        id = situation_record.findtext('d2:carParkIdentity', '', ns)
        if id != 'CAMB-CP001':
            continue

        timestamp = situation_record.findtext('d2:situationRecordCreationTime', '', ns)

        name = situation_record.findtext('d2:nonGeneralPublicComment/d2:comment/d2:value', '', ns)
        occupancy = int(situation_record.findtext('d2:carParkOccupancy', '', ns))
        capacity = int(situation_record.findtext('d2:totalCapacity', '', ns))
        fill_rate = int(situation_record.findtext('d2:fillRate', '', ns))
        exit_rate = int(situation_record.findtext('d2:exitRate', '', ns))

        results.append({'time': timestamp, 'id': id, 'name': name, 'capacity': capacity,
            'occupancy': occupancy, 'free': capacity-occupancy, 'fill_rate': fill_rate,
            'exit_rate': exit_rate})

    print(tabulate(results, headers='keys'))


if __name__ == '__main__':
    run()
