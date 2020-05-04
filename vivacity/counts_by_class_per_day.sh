#!/bin/bash

# This script produces the CSV file for chart of each vehicle class per day

for class in {pedestrian,cyclist,car,van,truck}
do
  echo Collecting counts for $class
  ./counts.sh vivacity_data .counts.$class >in_$class.csv
  echo Totalling per day for $class
  python count_per_line.py in_$class.csv >counts_in_per_day_$class.csv
  echo Completed counts_in_per_day_$class.csv
done

