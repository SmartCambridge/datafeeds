#!/bin/bash

TARGET=/Volumes/userfiles/public_html/acp/journey_time_3899101775/

echo
echo "** Remember to update downloaded data if needed..."
echo

./graphit_mill_road.py

cd bus_comparison || exit
./graphit_mill_road.py
cd .. || exit

cp journey_time_mill_road_area.pdf bus_comparison/journey_time_mill_road_area_BUS.pdf \
      ${TARGET}

chmod go+r ${TARGET}/*.pdf
