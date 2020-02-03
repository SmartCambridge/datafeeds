// Javascript functions for displaying Vivacity data

/* eslint no-console: "off" */
/*global $, L, LOCATIONS_URL, JOURNEYS_URL, MB_ACCESS_TOKEN, TF_API_KEY */

GET_TOKEN = 'https://api.vivacitylabs.com/get-token'

var map;

// Initialise
$(document).ready(function () {

    setup_map();
    load_data();

});

function setup_map(){

    map = new L.Map('map');

    var osm = new
        //L.TileLayer('http://map.cam.ac.uk/tiles/{z}/{x}/{y}.png',
        L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        {
            attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a></a>',
            maxZoom: 19
        }
    );

    var cambridge = new L.LatLng(52.20038, 0.1197);
    map.setView(cambridge, 15).addLayer(osm);

}

function load_data(){

    // Get a token

    token = prompt('Enter a token')

    headers = {
        'api-version': '2',
        Authorization: 'Bearer ' + token
    }




    $.when (
        $.get({
            url: 'https://api.vivacitylabs.com/countline',
            headers: headers,
            dataType: 'json',
        }),
        $.get({
            url: 'https://api.vivacitylabs.com/sensor',
            headers: headers,
            dataType: 'json',
        })
    )
    .done(function(all_countlines, all_sensors) {
        console.log(all_countlines, all_sensors)
    });

}


function not_in_use() {



  // Build a lookup index for countlines, and add the line's midpoint
  var countline_index = {};
  for (i = 0; i < all_countlines.length; ++i) {
    var countline = all_countlines[i];
    countline.location.middle =
       {'lat': (countline.location.start.lat + countline.location.end.lat)/2,
        'long': (countline.location.start.long + countline.location.end.long)/2};
    countline_index[countline.id] = countline;
  }

  sensors = L.featureGroup();
  joinlines = L.featureGroup();
  var sensor_map = {};

  console.log('About to draw sensors');

  for (i = 0; i < all_sensors.length; ++i) {
    var sensor = all_sensors[i];
    if (sensor.location !== null) {
      console.log(i, sensor.location)
      var key = sensor.location.lat + '|' + sensor.location.long;
      var countlines = sensor.countlines.join(', ');
      var desc = `Count: ${i}<br>Sensor: ${sensor.id}<br>Latitude: ${sensor.location.lat}<br>Longitude: ${sensor.location.long}<br>Countlines: ${countlines}`
      if (sensor_map.hasOwnProperty(key)) {
        marker = sensor_map[key];
        popup = marker.getPopup();
        popup.setContent(popup.getContent() + '<br><br>' + desc);
      }
      else {
        marker = L.marker([sensor.location.lat, sensor.location.long], {radius: 1, fillOpacity: 1, color: 'red'});
        sensor_map[key] = marker;
        marker.bindPopup(desc);
        marker.addTo(sensors);
      }
      console.log('countlines', sensor.countlines);
      for (j=0; j < sensor.countlines.length; ++j) {
        line = sensor.countlines[j];
        console.log('line', line);
        if (countline_index.hasOwnProperty(line)) {
          countline = countline_index[line];
          console.log('countline', countline);
          L.polyline(
            [ [sensor.location.lat, sensor.location.long],
              [countline.location.middle.lat, countline.location.middle.long]
            ], { color: 'black', weight: 1, dashArray: '4'}
          ).addTo(joinlines);
        }
      }
    }
  }

  countlines = L.featureGroup();
  var countline_map = {};

  console.log('About to draw countlines');

  for (i = 0; i < all_countlines.length; ++i) {
    var countline = all_countlines[i];
    console.log(countline.id)
    var key = countline.location.start.lat + '|' + countline.location.start.long + '|' + countline.location.end.lat + '|' + countline.location.end.long;
    var desc = `Count: ${i}<br>Countline: ${countline.id}`;
    if (countline_map.hasOwnProperty(key)) {
      countline = countline_map[key];
      popup = countline.getPopup();
      popup.setContent(popup.getContent() + '<br><br>' + desc);
    }
    else {
      var popup = L.featureGroup();
      L.polyline([[countline.location.start.lat, countline.location.start.long],
                [countline.location.end.lat, countline.location.end.long]],
                )
        .addTo(popup);
      L.circle([countline.location.start.lat, countline.location.start.long],
        {radius: 1, fillOpacity: 1, color: 'red'})
        .addTo(popup);
      L.circle([countline.location.end.lat, countline.location.end.long],
        {radius: 1, fillOpacity: 1, color: 'green'})
        .addTo(popup);
      countline_map[key] = popup;
      popup.bindPopup(desc);
      popup.addTo(countlines);
    }
  }

  map.addLayer(sensors).addLayer(countlines).addLayer(joinlines);

  map.fitBounds(sensors.getBounds());

}
