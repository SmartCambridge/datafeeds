#!/usr/bin/env python3

# Read in Drakewell 'locations' and 'livejourneytimes' in Json and
# emit a flattened file containing all the 'links' and 'compoundRoutes'
# annotated with the journey times and with all site references expanded.

import json

journey_index = {}

with open('l') as ll:
    locations = json.load(ll)

with open('j') as jj:
    journeytimes = json.load(jj)

# build an index from link id to journey
for journey in journeytimes:
    journey_index[journey['id']] = journey

# Copy across journey data for links
for link in locations['links']:
    journey = journey_index[link['id']]
    for key in 'time', 'period', 'travelTime', 'normalTravelTime':
        link[key] = journey[key]

for route in locations['compoundRoutes']:
    journey = journey_index[route['id']]
    for key in 'time', 'period', 'travelTime', 'normalTravelTime':
        route[key] = journey[key]

print(json.dumps(locations))
