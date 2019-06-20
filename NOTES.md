Drakewell
=========

The web portal at https://drakewell04.drakewell.com/ seems to work with the supplied credentials. Unfortunatly the 'user Guide' link on the home page gives 'Access denied'.

These examples seem to work:

```
https://drakewell04.drakewell.com/datex2/datex2_predefinedlocations.asp?v=2.2&node=cambridge_jtms&key=<key>
https://drakewell04.drakewell.com/datex2/datex2_trafficdata.asp?v=2.2&node=cambridge_jtms&key=<key>
```

Based on 'Datex 2 & JSON API Information JTMS' document you might think

```
https://drakewell02.drakewell.com/npmatchv2/exports/a/locations.asp?group=cambridge_jtms&key=<key>
```

would also work, but it gives

```
{
    "FAIL": true,
    "data": {
        "message": "Access Denied"
    }
}
```

which suggests that I'd need a different key (and indeed in the examples there are seperate keys).

Extracting predefined locations from XML:
```
xmlstarlet sel -N d=http://datex2.eu/schema/2/2_0 -t -m '//d:predefinedLocationName' -m "d:values" -v "d:value" -n predefinedlocations.xml
```

## Outstanding questions

1) Access to the Json format data for Cambridge?

2) Is live ATC flow data available? If so, how? ANSWERED (Michael: it's an
at-cost add-on that the County didn't purchase)

3) Can we have a meeting to discuss raw data feeds?

4) CCC's IDOX system seems to be getting TrafficFlow data at the individual sensors.
Can we access that?

