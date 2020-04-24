import csv
import sys

days = {}

countlines = {}

with open(sys.argv[1]) as csvfile:
    carsin = csv.reader(csvfile, delimiter=',')
    for row in carsin:
        countline = row[0]
        year = row[1]
        month = row[2]
        day = row[3]
        count = row[4]
        
        date = year+month+day
        
        if countline not in countlines:
            countlines[countline] = date
            
        if not date in days:
            days[date] = {}
            
        days[date][countline] = count

print(days['20200410'])

print(countlines)

line = ""

for countline in countlines:
    line += ","+countline
    
print(line)

for date in days:
    line = date
    for countline in countlines:
        if not countline in days[date]:
            print("countline "+countline+" missing from "+date, file=sys.stderr)
            count=str(0)
        else:
            count=days[date][countline]
            
        line += ","+count
    print(line)
        
        
