Questions
=========

General
-------

1) We need to collect data from you to keep a local archive at the
maximum time resolution possible. We also want to keep the latency of
the realtime data as low as possible. How do you recomend we go about
this?

2) Should we be concentrating out efforts on using the 'new' api, or the
'old' one, or both? [If the answer is exclusively one or the other then
feel free ignore the irrelevant questions below]

3) The 15 sensors visible on the portal and accessible from the APIs are
not the only Vivacity sensors in Cambridge (there are at least some on
Lensfield Road and a pair at the Grand Arcade car park entrance, and
probably at least one at Milton and we are involved with each of these
projects). Can we access to the data from these too? If so, how?

4) Is there any way to relate data returned by the two APIs? It seems
to relate to the same set of sensors but there don't seem to be any common
identifiers?

'New' API
---------

1) What do the returned counts represent?

2) When a first 5 minute bucket is truncated because it start isn't
aligned on a 5 minute boundary, what do the returned counts represent?
Actual counts in the truncated time range, pro-rata counts from the
entire 5 minute count? Something else?

3) Ditto, when the last 5 minute bucket is truncated?

4) Countlines seem to have an 'in' and 'out' property. What does this
mean? Is it consistent for each sensor?

5) What do the various classes of vehicle actually mean? There seem to
be at least "bus", "car", "cyclist", "minibus", "motorbike",
"pedestrian", "rigid", "taxi", "truck". "van".

6) The `/get-token` response includes a `refresh-token` field. Does this
imply that tokens can be refreshed, and if so how?

7) We understand that these particular sensors don't support ANPR and
therefore that the /journey-time endpoint won't have anything to report.
Is that correct?

8) How much past data can we access? The documentation says that for
/counts the maximum time range allowed between "from" and "to" is 48
hours but can we use this to go back to when you started collecting
data?

10) In the 'original' API, countlines have a semi-human-readable
"countlineId". Any chance of something similar in v2? Ditto sensors?

'Original' API
--------------

1) What does the returned data represent? From inspection it seems to
contain counts of various
vehicle types in two directions at each of 15 sensor locations, which
look to match the information I can see in the portal. In particular:

* What's the timescale and sampling interval for the counts? The
  data contains 'fromTime' and 'toTime' values but, assuming they
  represent milliseconds since the Unix epoch, they vary in a way I don't
  understand and represent periods of between 3m50s and 5m0s.

* What do the counts represent?

* What do the various classes of vehicle actually mean? There seem
  to be at least "Car", "Pedestrian", "Cyclist", "Motorbike", "Bus", "OGV1", "OGV2", "LGV".

* Countlines seem to be defined by a single Latitude/Longitude
  pair - how is this interpreted?

* What's the definition of 'In' and 'Out' in respect of counts?

2) The API only gives access to 'current' information. Is it possible to
access data that has already been collected? While we can arrange to
sample and store this data ourselves for further analysis it would be
better if we could prime our collection with everything that has been
collected to date.

Examples
========

For reference.

'Original API'
--------------

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
          {
            "class": "cyclist",
            "countIn": 2,
            "countOut": 3
          },
          {
            "class": "motorbike",
            "countIn": 1,
            "countOut": 0
          },
          {
            "class": "bus",
            "countIn": 1,
            "countOut": 0
          },
          {
            "class": "van",
            "countIn": 2,
            "countOut": 0
          }
        ]
      }
    ]
  },
  <...>
]
```

'New' API - Sensors
-------------------

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
    ]
  },
  <...>
]
```

'New API' - Countlines

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

'New' API - Counts
------------------

```
{
  "13069": {
    "2019-05-31T08:18:00.153Z": {
      "from": "2019-05-31T08:18:00.153Z",
      "to": "2019-05-31T08:20:00.000Z",
      "counts": [
        {
          "class": "car",
          "countIn": 1,
          "countOut": 4
        },
        {
          "class": "cyclist",
          "countIn": 2,
          "countOut": 3
        },
        {
          "class": "pedestrian",
          "countIn": 2,
          "countOut": 0
        },
        {
          "class": "van",
          "countIn": 1,
          "countOut": 1
        }
      ]
    },
    "2019-05-31T08:20:00.000Z": {
      "from": "2019-05-31T08:20:00.000Z",
      "to": "2019-05-31T08:23:00.153Z",
      "counts": [
        {
          "class": "car",
          "countIn": 0,
          "countOut": 4
        },
        {
          "class": "cyclist",
          "countIn": 0,
          "countOut": 1
        },
        {
          "class": "van",
          "countIn": 1,
          "countOut": 0
        }
      ]
    }
  },
  <...>
]
```