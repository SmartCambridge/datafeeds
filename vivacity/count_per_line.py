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

#print(days['20200410'])

#print(countlines)

# Print a header line with the column names
line = "Date,TOTAL"

for countline in countlines:
    line += ","+countline

print(line)

# Print a line-per-day containing Date, TOTAL, and a column for each countline
for date in days:
    total = 0
    line = ""
    for countline in countlines:
        # the 'count' from the input data is a string
        if not countline in days[date]:
            print("countline "+countline+" missing from "+date, file=sys.stderr)
            count=str(0)
        else:
            count=days[date][countline]

        total += int(count)    # somehow I found this line and the next pleasingly symmetrical
        line += ","+count

    print(date+","+str(total)+line)


