#!/bin/bash

. setup_env

TOKEN=$(./get_token.py)

http https://api.vivacitylabs.com/sensor \
  "Authorization: Bearer $TOKEN" \
  api-version:2.0.0 > all_sensors.json

http https://api.vivacitylabs.com/countline \
  "Authorization: Bearer $TOKEN" \
  api-version:2.0.0 > all_countlines.json

http https://api.vivacitylabs.com/counts \
  "Authorization: Bearer $TOKEN" \
  api-version:2 > latest_counts.json

sed -e 's/^/all_sensors=/' all_sensors.json > all_sensors.js
sed -e 's/^/all_countlines=/' all_countlines.json > all_countlines.js
sed -e 's/^/latest_counts=/' latest_counts.json > latest_counts.js
