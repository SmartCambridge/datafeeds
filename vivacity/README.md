Vivacity notes
==============

*These notes relate to the situation in late summer 2019, unless
otherwise mentioned. Things have changed since then.*

Sensors
=======

Vivacity sensors count and classify pedestrians, cyclists and various
vehicle types crossing 'virtual countlines' in both directions in their
field of view . Some (perhaps all?) can monitor multiple countlines;
some (perhaps all?) can track journey times of objects within their
field of view though we have not seen data from this. Newer sensors
include ANPR allowing vehicles to be tracked between sensors to derive
journey times.

Direction across a countline is recorded as 'in' or 'out'. 'in' seems to
represent traffic crossing the countline while travelling towards the
corresponding sensor. Vivacity have a more formal definition using the
relative positions of the sensor and the start and end points of the
coutline.

Various batches of sensors have been deployed:

Lensfield Road
--------------

Some sensors were deployed in the Lensfield Road area supporting air
quality work in Chemistry. We have never seen any data from these
sensors.

Grand Arcade Car Park entrance
------------------------------

Some sensors were deployed near the entrance to the Grand Arcade car
park to support work by GCP on Milton Road journey times. We have never
seen any data from these sensors though Ian helped to get them
installed.

Mill Road Area
--------------

15 sensors monitoring the effect of the Mill Road bridge closure in 2019
were deployed In April 2019 and are expected to remain in place
until October 2020. Most are located in streets around Mill Road but
also one each on Milton Road and Histon Road. The Histon Road sensor
never worked properly and was subsequently removed.

Each of these sensors monitor a single countline and none are capable
of ANPR.

There are some oddities about the metadata for these sensors:

* A 16th sensor (`{a355adca-66a6-11e9-a851-42010af00366}`) is listed but
has `'location': null, 'countlines': []` so was presumably never used.

* Two sensors (`{8e8e616c-6a6a-11e9-a71b-42010af00366}` and
`{ad757950-6806-11e9-bef4-42010af00366}`) claim to be in identical
locations on Newmarket Road. In practice `{8e8e61...` is probably the
one actually located on on the east side of Perne Road just north of the
junction with Radegund Road/Birdwood Road.

* `{8e8e61...` lists two countlines (`13083` and `13086`). These were
both originally shown at identical locations on Perne Road, but now
`13086` is showing up on Newmarket Road which may be a mistake. `13083`
has never appeared in the counts data and so was probably never used.

We can see data from these sensors on the Council's Vivacity dashboard
and API. Data is available from midday on 2019-05-09. We have done some
work on the data from these sensors. This data is also publicly
available on Cambridgeshire Insight
https://cambridgeshireinsight.org.uk/

Histon Road and Milton Road
---------------------------

2 sensors were deployed at opposite ends of each of Histon Road and
Milton Road in Autumn 2019 to monitor the effects of planed GCP work on
these roads and are still in place. All 4 monitor three separate
countlines (one on the main carriageway, one on each of the footways)
and we are told that they support ANPR.

One of these sensor (`{c55438dc-ca48-11e9-8d57-42010af00327}`) has a
fourth countline `13344` which doesn't seem to be in use.

We can see data from these sensors on the Council's Vivacity dashboard
and API. Data is available from 2019-10-11.

We briefly used the data from one of these in our work on Milton Road
traffic speeds but otherwise haven't really looked at their data.

Fendon Road Area
----------------

7 sensors seem to have been deployed sometime in late 2019 around Fendon
Road, probably to monitor the effect of the extensive road works at
Fendon Road Roundabout. 6 of them monitor three separate countlines (one
on the main carriageway, one on each of the footways) and probably
support ANPR. One only monitors a single countline on Fendon Road and
could be the old Milton Road one redeployed.

We can see data from these sensors on the Council's Vivacity dashboard
and API. Data is available from 2019-11-01 though not for all countlines.
We haven't really looked at their data.

West Cambridge Site
-------------------

One sensor was installed on Charles Babbage Road in late December 2019
near the junction with JJ Thompson Avenue, apparently monitoring the
path through the Broers Building.

This sensor does not appear on on the Council's Vivacity dashboard or
API and we haven't seen any data from it.

Dashboard
=========

There's an interactive dashboard at

https://audacity.vivacitylabs.com/

Access is by individual username/password which are created by following
what looks like a customised invitation link in an email. Usernames
appear to be linked to the group of sensors the user can see.

The dashboard provides a map showing countlines. Clicking a countline
shows a traffic breakdown graph for that countline, initially for today.
The direction ('in', 'out') and the date can be changed. Historic data
for one or more countlines can be downloaded.

APIs
====

We are aware of two different APIs:

The 'original' API
------------------

https://api.vivacitylabs.com/cambridge-mill-road/v1/counts?apikey=<key>

We have a API key for this and it has worked but is currently failing
with a server error.

When working this returns a JSON list of 'device' objects (sensors),
each containing device metadata and a list of countline objects, each
containing countline metadata and a list of classified counts in both
directions:

```
[
  {
    "deviceId": 1,
    "deviceLatLong": {
      "lat": 52.19651,
      "lng": 0.15303
    },
    "countlines": [
      {
        "countlineId": "S1_MillRoad_CAM003",
        "countlineLatLong": {
          "lat": 52.19659,
          "lng": 0.15293
        },
        "direction": "both",
        "fromTime": 1559306123814,
        "toTime": 1559306355656,
        "counts": [
          {
            "class": "car",
            "countIn": 22,
            "countOut": 26
          },
          {
            "class": "pedestrian",
            "countIn": 4,
            "countOut": 14
          },
          <...>
        ]
      },
      <...>
    ]
  },
  <...>
]
```

We have no documentation on what any of this means.

The countline IDs returned by this API match those displayed by the
dashboard.

Vivacity have suggested that it would be better to concentrate on using
their 'new' API (see next).

New API
-------

This is documented in an automatically-generated page at

https://api.vivacitylabs.com/docs/

A number of API endponts have been added since we last used this API and
we know little about them. We only have experience of the one listed below.

As originally implemented the API didn't support CORS, making it
impossible to call from Javascript inside a browser. Now endpoints other
than `/get-token` return a `Access-Control-Allow-Origin: *` header.
However this is only sufficient for CORS 'Simple Requests' but the
requests to the API aren't 'Simple' because they include headers not on
the acceptable list. CORS requires that non-simple requests are
'pre-flighted' via an OPTIONS request and currently all OPTIONS requests
seem to fail with '400 Not Foud' and an explanatory text 'no Route
matched with those values'.

### `/get-token`

To use the API a username and password is first converted into a token
using the `/get-token` endpoint. These are distinct from the credentials
used to access the dashboard. SmartCambridge has a 'group' account for
this with username `cambridge-api-user`. This token is then used to
authorise access to most other API endpoints by including it in an
'Authorizaton' header of type 'Bearer'.

Tokens expire after 5 minutes but come with a 'renewal token' with
a 30 minuite lifetime. It looks as though the new `/refresh-token`
endpoint can be used to get a new token using the renewal token without
having to re-quote the password.

As mentioned above, `/get-token` doesn't include a
`Access-Control-Allow-Origin: *` header in its response, making it
impossible to call from browser Javascript. This suggests that the
intent is that this is always called server-side, thus protecting
username and password, with browsers relying on the resulting token and
renewal token for authorisation.

### `/sensor`

Returns a JSON list of objects representing sensors, including their ID,
location, and the countlines that they monitor.

The objects also include a list of the vehicle classes that they can report,
though they didn't when our initial work was done.

The sensor and countline IDs returned here **do not** match those
returned by the 'original' API or the dashboard. I'm not aware of any
cross reference table, though by inspection it's clear that they are the
same.

```
[
  {
    "id": "422ff7b0-669e-11e9-a599-42010af00366",
    "location": {
      "lat": 52.19994,
      "long": 0.13679
    },
    "countlines": [
      "13069"
    ],
    "availableClasses": [
      "pedestrian",
      "cyclist",
      "motorbike",
      "car",
      "taxi",
      "van",
      "minibus",
      "bus",
      "rigid",
      "truck",
      "emergency car",
      "emergency van",
      "fire engine"
    ]
  },
  <...>
]
```

### `/countline`

Returns a JSON list of objects representing countlines and the location
of their start end end points. See above for comments on the IDs used.

```
[
  {
    "id": "13069",
    "location": {
      "start": {
        "lat": 52.19988,
        "long": 0.13677
      },
      "end": {
        "lat": 52.1999,
        "long": 0.13665
      }
    },
    "direction": "both"
  },
  <...>
]
```

### `/counts`

Returns a JSON object with keys corresponding to countline IDs. Each
value is a further object with keys corresponding to timestamps and
values representing counts for a period starting at that timestamp.
These values contain the start and end timestamp of the period and a
list of objects giving the 'in' and out' counts of vehicles in each
class:

```
{
  "13070": {
    "2020-01-27T17:24:50.993Z": {
      "from": "2020-01-27T17:24:50.993Z",
      "to": "2020-01-27T17:25:00.000Z",
      "counts": [
        {
          "class": "car",
          "countIn": 0,
          "countOut": 2
        }
      ]
    },
    "2020-01-27T17:25:00.000Z": {
      "from": "2020-01-27T17:25:00.000Z",
      "to": "2020-01-27T17:29:50.993Z",
      "counts": [
        {
          "class": "car",
          "countIn": 10,
          "countOut": 23
        },
        {
          "class": "pedestrian",
          "countIn": 0,
          "countOut": 1
        }
      ]
    }
  },
  <...>
}
}
```

The API allows you to specify the time range for the results (default
the last 5 minutes, limited to 48 hours), a list of countlines to
include (default all), and a list of vehicle classes to return (default
all).

A new parameter `includeZeroCounts` apparently includes classes with
zero vehicles in the output - previously and by default they are omitted.

Data is returned grouped in buckets 5 minutes wide. While not
documented, these buckets seem to be aligned on the hour and every 5
minutes thereafter. If the start and/or end of the specified time range
does not fall on a bucket boundary then the first and/or last the bucket
will represent less than 5 minutes. There is some evidence that in these
cases the returned counts represent the actual counts in the truncated
time range and not just a pro-rata of the 5 minute figures.

In the API as used in Summer 2019, buckets with no traffic counts were
completely omitted, making iterating over the returned data difficult. It
is possible that the `includeZeroCounts` parameter suppresses this
behaviour.

Experimentation suggests that counts are updated asynchronously at
roughly 60 second intervals. See for example `v2-timing_test5.py` which
retrieves count data every 5 seconds for a period covering 15 minutes
into the future from its start and reports every time the number of
vehicles changes:

```
Sleeping 22.579892 seconds to the top of the next minute
Start: 2020-01-28T16:33:00 Vehicles: 0 Countline: 13080
Change: 2020-01-28T16:33:55.338356 Vehicles: 19 Diff: 19
Change: 2020-01-28T16:34:55.268516 Vehicles: 50 Diff: 31
Change: 2020-01-28T16:35:55.306114 Vehicles: 90 Diff: 40
Change: 2020-01-28T16:36:55.376578 Vehicles: 129 Diff: 39
Change: 2020-01-28T16:37:55.864199 Vehicles: 171 Diff: 42
Change: 2020-01-28T16:38:50.747798 Vehicles: 208 Diff: 37
Change: 2020-01-28T16:39:50.219419 Vehicles: 251 Diff: 43
Change: 2020-01-28T16:40:51.614725 Vehicles: 281 Diff: 30
Change: 2020-01-28T16:41:52.430874 Vehicles: 312 Diff: 31
Change: 2020-01-28T16:42:50.373154 Vehicles: 345 Diff: 33
Change: 2020-01-28T16:43:51.743008 Vehicles: 375 Diff: 30
Change: 2020-01-28T16:44:51.779719 Vehicles: 401 Diff: 26
```

This makes downloading very recent data difficult since you need to be
sure that all pending reports have been received before depending on the
data received but there is no way to be sure that this has happened. The
default behaviour of returning data for the last 5 minutes is therefore flawed
since the returned data is almost guaranteed to be an undercount which
will be subsequently updated. `v2_timing_test4.py` demonstrates this
fairly reliably by retrieving the most recent 5 minutes of data for a
particular countline, and then repeatedly retrieving data for the same
interval at 5 second intervals and reporting if the results change.

```
Now:  2020-01-28T17:18:20.479957
{
    "13074": {
        "from": "2020-01-28T17:13:20.575Z",
        "to": "2020-01-28T17:18:20.575Z",
        "counts": {
            "bus": {
                "countIn": 5,
                "countOut": 0
            },
            "car": {
                "countIn": 25,
                "countOut": 25
            },
            "cyclist": {
                "countIn": 7,
                "countOut": 11
            },
            "pedestrian": {
                "countIn": 13,
                "countOut": 49
            },
            "motorbike": {
                "countIn": 1,
                "countOut": 0
            }
        }
    }
}
Initial from:  2020-01-28T17:13:20.575Z
Initial to:  2020-01-28T17:18:20.575Z
2020-01-28T17:18:27.668059 No change
2020-01-28T17:18:33.199068 No change
2020-01-28T17:18:39.851912 Changed
{
    "values_changed": {
        "root['13074']['counts']['bus']['countIn']": {
            "new_value": 6,
            "old_value": 5
        },
        "root['13074']['counts']['cyclist']['countOut']": {
            "new_value": 12,
            "old_value": 11
        },
        "root['13074']['counts']['pedestrian']['countOut']": {
            "new_value": 60,
            "old_value": 49
        },
        "root['13074']['counts']['pedestrian']['countIn']": {
            "new_value": 17,
            "old_value": 13
        }
    }
}
2020-01-28T17:18:45.108614 No change
2020-01-28T17:18:51.123451 No change
2020-01-28T17:18:57.052551 No change
2020-01-28T17:19:02.755401 No change
2020-01-28T17:19:10.561029 No change
2020-01-28T17:19:15.871895 No change
2020-01-28T17:19:21.423037 No change
2020-01-28T17:19:26.706659 No change
```

If the update interval could be guaranteed to be 60 seconds it would be
safe to only look at data from 60 seconds in the past. But it isn't
documented and appears to vary and might perhaps vary significantly in
the face of delays in whatever back-haul network Vivacity use.

Accuracy
========

The County commissioned a manual traffic count from ATR (Advanced Traffic
Research) at the site of the original Milton Road sensor on 2019-07-18.

Vivacity and ATR use slightly different vehicle classes but they can be
combined as follows (informed by http://www.videodatapad.com/faq/standard-uk-vehicle-classification,
https://democracy.york.gov.uk/mgConvert2PDF.aspx?ID=38557):

```
Vivacity        ATR                      Combined as
--------------- ------------------------ --------------------------------
pedestrian      Ped                      Pedestrian
cyclist         Cyc pavement + Cyc Road  Cyclist
motorbike       M/B                      Motorbike
car             Cars                     Car
taxi                                     Car
van             LGV                      Light Goods (LGV)
minibus                                  Car
bus             PSV                      Bus (PSV)
rigid           OGV1                     Rigid Goods (OGV1)
truck           OGV2                     Truck (OGV2)
emergency car                            Car
emergency van                            Car
fire engine                              (ignored)
```

Raw data and scripts in `check_counts/` compare Vivacity and ATR data, creating
the graph in `check_counts/comparison.pdf` and the following table covering the period
for which we have data from both sources:

```
Type                Dir       Vivacity    ATR    Diff         %
------------------  --------  ----------  -----  ------  --------
Pedestrian          inbound          820    769      51     6.22%
Pedestrian          outbound         605    703     -98   -16.20%
Cyclist             inbound         1260   1462    -202   -16.03%
Cyclist             outbound         850   1216    -366   -43.06%
Motorbike           inbound          142    156     -14    -9.86%
Motorbike           outbound         129    142     -13   -10.08%
Car                 inbound         6399   6429     -30    -0.47%
Car                 outbound        5604   5922    -318    -5.67%
Light Goods (LGV)   inbound          967    881      86     8.89%
Light Goods (LGV)   outbound        1022    910     112    10.96%
Bus (PSV)           inbound          196    203      -7    -3.57%
Bus (PSV)           outbound         180    189      -9    -5.00%
Rigid Goods (OGV1)  inbound          166    181     -15    -9.04%
Rigid Goods (OGV1)  outbound         168    201     -33   -19.64%
Truck (OGV2)        inbound           19     66     -47  -247.37%
Truck (OGV2)        outbound          30     66     -36  -120.00%

All Goods           inbound         1152   1128      24     2.08%
All Goods           outbound        1220   1177      43     3.52%

All Types           inbound         9969  10147    -178    -1.79%
All Types           outbound        8588   9349    -761    -8.86%
```

I think you can draw the following conclusions:

* There's a good match - these really are showing much the same
underlying data.

* Vivacity seem to be slightly under-counting in general, more so in the
'outbound' direction (which is actually the Vivacity 'in' direction,
towards the sensor and for road traffic is on the opposite side of the road
from the counter). There is some evidence of similar imbalances between
counts in the two directions in the data from other counters with flows
on the opposite side of the road from the counter being lower.

* Vivacity and ATR don't agree about goods vehicle classifications, but
their totals for all goods vehicles largely agree.

* Some Vivacity counts (e.g. cars) are better than other (e.g. cycles,
unfortunately, though perhaps not surprisingly). For cycles, it could
be that ATR captured more 'pavement' cyclists than Vivacity, or perhaps
because of distance or because the camera's view was blocked by other
traffic. Ditto pedestrians.

Directory content
=================

`v2-timing_test4.py`, `v2-timing_test5.py`, and `check_counts/` have
already been mentioned.

`get_token.py` obtains a 'new API' token using a username and password
from environment variables and prints it to stdout. In particular this
is handy for authenticating to the API documentation page.
`setup_env.skel` can be used as a template for a file to source to setup
the necessary variables. Such a file shouldn't be committed to a public
repository. In particular this is handy for authenticating to the API
documentation page.

`get_latest_data.sh` uses `get_token.py` to get a token and then the
`http` command from HTTPie (https://httpie.org/) to download current
sensor, countline and count data. It also converts the JSON files to
JavaScript ones which can then be loaded by opening `visualise.html` or
`visualise2.html` in a browser (the web pages work this way because the
API didn't support CORS and still doesn't seem to do so).
visualise3.html and visualise.js are an attempt to do all of this in
pure Javascript which was sabotaged by the lack of working CORS support.

`download.py` downloads historic journey time data into the directory
`vivacity_data` in a format mimicking the `tfc_server` platform. Run
with `--help` for details of arguments available to select the period to
download. It works by collecting data in hourly chunks for reasons that
currently escape me but have something to do with getting errors trying
to process an entire day. It is currently getting rather a lot of
502 Gateway Timeout errors but has some new retry logic in an attempt
to deal with this.

The various `graphit-*.py` scripts, along with `graphit_base.py` plot
aspects of the data in `vivacity_data` using pandas and matplotlib. Some
of the graphs were published at
https://www.cl.cam.ac.uk/~jw35/acp/classified_traffic/. The script
`update_website.py` assumes data from 2019-05-10 to yesterday is
available in `vivacity_data`, runs `graphit-3way.py` and
`graphit-motor.py` and transfers the result to the website.



