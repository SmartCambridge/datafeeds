#!/usr/bin/env python3

# Read in Drakewell 'locations' and 'livejourneytimes' in Json and
# emit a flattened file containing all the 'links' and 'compoundRoutes'
# annotated with the journey times and with all site references expanded.

import json

new_links = []
site_index = {}
journey_index = {}


# Expand list of site ids into a list of sites
def expand(obj):
    expanded_sites = []
    for site_id in obj['sites']:
        expanded_sites.append(site_index[site_id])
    obj['sites'] = expanded_sites


with open('l') as ll:
    locations = json.load(ll)

with open('j') as jj:
    journeytimes = json.load(jj)

# build an index from site id to site data
for site in locations['sites']:
    site_index[site['id']] = site

# build an index from link id to journey
for journey in journeytimes:
    journey_index[journey['id']] = journey

# Expand all the links
for link in locations['links']:
    expand(link)
    new_links.append(link)

# Expand all the (compound) routes
for route in locations['compoundRoutes']:
    expand(route)
    new_links.append(route)

# Copy across journey data
for link in new_links:
    journey = journey_index[link['id']]
    for key in 'time', 'period', 'travelTime', 'normalTravelTime':
        link[key] = journey[key]

results = {'links': new_links}

print(json.dumps(results, indent=4))
