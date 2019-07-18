#!/bin/bash

TARGET=/Volumes/userfiles/public_html/acp/classified_traffic_0252853452/

./graphit-3way.py
./graphit-motor.py

cp 3way-date.pdf 3way-hour.pdf motor-date-fixed.pdf motor-date.pdf motor-hour.pdf \
      ${TARGET}

chmod go+r ${TARGET}/*.pdf
