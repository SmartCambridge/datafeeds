#!/bin/bash

# Usage ./counts.sh <directory> <counts_property>
# E.g. ./counts.sh vivacity_data .counts.car
#
# Where the data will be <directory>/YYYY/MM/DD/<countline>/in.txt
# i.e. the directory *must* contain year/month/day vivacity counts

dir=$1

count_property=$2

IFS='/' read -ra dirpath <<< "$dir"
dirlen=${#dirpath[@]}

# echo "countline,year,month,day,car"
for yearpath in $dir/*
do
    year="$(basename "$yearpath")"
    for monthpath in $dir/$year/*
    do
        month="$(basename "$monthpath")"
        for daypath in $dir/$year/$month/*
        do
            day="$(basename "$daypath")"
            for f in $dir/$year/$month/$day/*
            do
                IFS='/' read -ra fpath <<< "$f"
                y=${fpath[$dirlen]}
                m=${fpath[$dirlen+1]}
                d=${fpath[$dirlen+2]}
                line=${fpath[$dirlen+3]}
                ( cat $f/in.txt |
                  jq $count_property |
                  awk -v l=$line -v f=$f -v y=$y -v m=$m -v d=$d '{ s+=$1} END { print l","y","m","d","s}'
                )
            done
       done
    done
done

