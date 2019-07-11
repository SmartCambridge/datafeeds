Vivacity notes
==============

'original' API
--------------

https://api.vivacitylabs.com/cambridge-mill-road/v1/counts?apikey=<key>

### Outstanding questions

1) Is there any documentation on what the data accessed by the API call
represents? From inspection it seems to contain counts of various
vehicle types (Car,Pedestrian,Cyclist,Motorbike,Bus,OGV1,OGV2,LGV) in
two directions at each of 15 sensor locations, which look to match the
information I can see in the portal. I have two immediate questions:

    * What's the timescale and sampling interval for the counts? The data
contains 'fromTime' and 'toTime' values but, if I'm interpreting them
correctly, they vary in a way I don't understand and represent periods
of between 3m50s and 5m0s.

    * What do the counts represent? Vehicles passing a line? Vehicles in
view? Something else?

2) The API only gives access to 'current' information. Is it possible to
access data that has already been collected? While we can arrange to
sample and store this data ourselves for further analysis it would be
better if we could prime our collection with everything that has been
collected to date.

4) These 15 sensors are not the only Vivacity sensors in Cambridge
(there are at least some on Lensfield Road and a pair at the Grand
Arcade car park entrance, and I think at least one at Milton and we are
involved with each of these projects). Can we access to the data from
these too?


New API
-------

### Notes

https://api.vivacitylabs.com/api-docs/

```
. setup_env
TOKEN=`./get_token.py`
http https://api.vivacitylabs.com/sensor "Authorization: Bearer $TOKEN" api-version:2.0.0 > all_sensors.json
http https://api.vivacitylabs.com/countline "Authorization: Bearer $TOKEN" api-version:2.0.0 > all_countlines.json
http https://api.vivacitylabs.com/counts "Authorization: Bearer $TOKEN" api-version:2 > latest_counts.json

[or ./get_latest_data.sh]


jq '. | length' all_sensors.json
jq '. | length' all_countlines.json
jq '. | length' all_counts.json

jq  [.[].countlines]  all_sensors.json
jq keys all_counts.json
jq values all_counts.json
jq [.[].id] all_countlines.json

jq '..|.class?' all_counts.json | sort | uniq
```

16 sensors:
* One (`a355adca-66a6-11e9-a851-42010af00366`) has
`'location': null, 'countlines': []` so is presumably not in use.
* Two sensors (`8e8e616c-6a6a-11e9-a71b-42010af00366` and
`ad757950-6806-11e9-bef4-42010af00366`) claim to be in identical
locations on Newmarket Road
* `8e8e616c-6a6a-11e9-a71b-42010af00366`) lists two countlines
(`13083` and `13086`) both at identical locations on Perne Road.

16 countlines. All direction 'both'.

Only 14 countlines reporting data. These two are missing:
* `13082` (on sensor `ad7580b2-6806-11e9-bef4-42010af00366` on Histon Road)
* `13083` (mentioned above, on `8e8e616c-6a6a-11e9-a71b-42010af00366` on Perne Road).



Outstanding questions
---------------------

1) In the V1 API, countlines have a semi-human-readable "countlineId".
Any chance of something similar in v2? Dito sensors?

2) When a first or last 5 minute bucket is truncated because its star/end
isn't aligned on a 5 minuet boundary, what do the returned counts represent?
actual counts in the truncated time range, pro-rata counts from the entire
5 minute count? Something else? ANSWER: Actual counts for the time range.

3) The `/get-token` response includes a `refresh-token` field. Does this imply that
tokens can be refreshed, and if so how? ANSWER: Yes, documentation to follow

4) Countlines seem to have an 'in' and 'out' direction. How is this defined?
ANSWER: The 'in' direction is clockwise around the start point (normally also
towards the sensor, but that's not guaranteed)

5) We understand that these particular sensors don't support ANPR and therefore that the
/journey-time endpoint won't have anything to report. Is that correct?
ANSWER: Yes (but note that individual sensors can track vehicles through
their field of view and this data may be available)

6) How much past data can we access? The documentation says that for /counts
the maximum time range allowed between "from" and "to" is 48 hours but can we
use this to go back to when you started collecting data? ANSWER: All data collected

7) We'd like to collect data from you to keep a local archive at the
maximum time resolution possible. What's the best way for us to go about this?

8) What do the various classes of vehicle actually mean? I've seen at least "bus",
"car", "cyclist", "minibus", "motorbike", "pedestrian", "rigid", "taxi", "truck".
"van". ANSWER: Definitive list is "pedestrian", "cyclist", "motorbike", "car",
"taxi", "van", "minibus", "bus", "rigid", "truck", "emergency car", "emergency van",
"fire engine".

9) What do the returned counts represent? Vehicles crossing the countline
in the period of the sample, or something else? ANSWER: Vehicles crossing
the countline in the period.

10) Missing data/misplaced sensors (see above)

11) If this API is to be callable from JavaScript in third-party web pages
then the endoints need to support CORS.



Conference call 2019-06-04
--------------------------

Present:
* Gemma Schroeder (CCC)
* Michael Stevens (CCC)
* Yang Lu (Vivacity CTO)
* Sarah Chaillot (Vivactiy)
* Benjamin Kilner (Vivacity, and ex-Cambridge?)
* Julian ?? (Vivacity, API developer)

Bugs
----

1) /counts `timerange` parameters seem to be ignored

2) Submitting more than one countline to the /counts endpoint results in error
500: countlineIds.split is not a function.

3) Submitting more than one class to the /counts endpoint results in error
500: classes.split is not a function.

4) Any edit to the timerange parameter in the Swagger 'try it out' functionality
causes the input box to go pink and the 'Execute' button to no longer function.

Vehicle classes
---------------

```
"label_map": {
            "0": "pedestrian",
            "1": "cyclist",
            "2": "motorbike",
            "3": "car",
            "4": "taxi",
            "5": "van",
            "6": "minibus",
            "7": "bus",
            "8": "rigid",
            "9": "truck",
            "10": "emergency car",
            "11": "emergency van",
            "12": "fire engine"
```

Date Ranges
-----------

Data started being recorded 2019-05-09 at about 13:00 (actually 12:05:00.000Z).

S11_HISTONROAD_CAM003 broke 2019-05-21 and was fixed on 2019-06-11.




