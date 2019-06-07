// Javascript functions for displaying Bluetruth data

/* eslint no-console: "off" */
/*global $, L, DRAKEWELL_KEY, MB_ACCESS_TOKEN, TF_API_KEY */

var LOCATIONS_URL = `https://drakewell02.drakewell.com/npmatchv2/exports/a/locations.asp?group=PORTSMOUTH_JT&key=${DRAKEWELL_KEY}`;
var JOURNEYS_URL = `https://drakewell02.drakewell.com/npmatchv2/exports/a/livejourneytimes.asp?group=PORTSMOUTH_JT&key=${DRAKEWELL_KEY}`;

// m/sec to mph
var TO_MPH = 2.23694;

// Style options for markers and lines
var SITE_OPTIONS = { color: 'black', fillColor: 'green', fill: true, fillOpacity: 0.5, radius: 7 };
var NORMAL_COLOUR = '#3388ff';
var HILIGHT_COLOUR = 'red';
var LINK_OPTIONS = { color: NORMAL_COLOUR };
var COMPOUND_ROUTE_OPTIONS = { color: NORMAL_COLOUR };

// Misc script globals
var map, sites_layer, links_layer, compound_routes_layer, layer_control;
var hilighted_line = null;


// Initialise
$(document).ready(function () {

    setup_map();
    load_data();

});

// Setup the map environment
function setup_map() {

    map = new L.Map('map');

    // various map providers
    var osm = L.tileLayer.provider('OpenStreetMap.Mapnik');
    var mb = L.tileLayer.provider('MapBox', {
        id: 'mapbox.streets',
        accessToken: MB_ACCESS_TOKEN
    });
    var tf = L.tileLayer.provider('Thunderforest.Neighbourhood', {
        apikey: TF_API_KEY
    });

    sites_layer = L.featureGroup();
    links_layer = L.featureGroup();
    compound_routes_layer = L.featureGroup();

    var cambridge = new L.LatLng(52.20038, 0.1197);
    map.setView(cambridge, 15).addLayer(tf).addLayer(sites_layer).addLayer(links_layer);

    var base_layers = {
        'MapBox': mb,
        'OSM': osm,
        'ThunderForest': tf,
    };
    var overlay_layers = {
        'Sites': sites_layer,
        'All links': links_layer,
    };
    layer_control = L.control.layers(base_layers, overlay_layers, {collapsed: false}).addTo(map);

    // Clear any highlighting caused by clicking lines
    map.on('click', clear_line_highlight);

}


// Async load locations and current live journey times
function load_data() {

    $.when(
        $.get(LOCATIONS_URL),
        $.get(JOURNEYS_URL)
    ).done(function(locations_result, journeys_result) {

        var locations = locations_result[0];
        var journeys = journeys_result[0];

        // Sites
        add_sites(locations.sites);

        // Links and Compound routes
        add_lines(locations.links, locations.sites, journeys, links_layer, LINK_OPTIONS);
        add_lines(locations.compoundRoutes, locations.sites, journeys, compound_routes_layer, COMPOUND_ROUTE_OPTIONS);

        // Scale map to fit
        var region = sites_layer.getBounds().extend(links_layer);
        map.fitBounds(region);

    });


}


// Helper function to draw  sites
function add_sites(sites) {

    for (var i = 0; i < sites.length; ++i) {
        var site = sites[i];
        var marker = L.circleMarker([site.location.lat, site.location.lng], SITE_OPTIONS);
        marker.properties = { 'site': site };
        marker.bindPopup(site_popup);
        marker.addTo(sites_layer);
    }
}


// Helper function to draw links and compound routes
function add_lines(lines, sites, journeys, layer, options) {

    for (var i = 0; i < lines.length; ++i) {
        var line = lines[i];

        // Accumulate points
        var points = [];
        for (var j = 0; j < line.sites.length; ++j) {
            var site = find_object(sites, line.sites[j]);
            if (site) {
                points.push([site.location.lat, site.location.lng]);
            }
        }

        var polyline = L.polyline(points, options);
        polyline.properties = { 'line': line, 'journey': find_object(journeys, line.id) };
        polyline.bindPopup(line_popup);
        polyline.on('click', line_highlight);
        polyline.addTo(layer);

        // Add compound routes to the map individually, becasu they can overlap each other
        if (layer === compound_routes_layer) {
            layer_control.addOverlay(polyline, `Route: ${line.name}`);
        }

    }

}


// Hilight a clicked line
function line_highlight(e) {

    var line = e.target;

    clear_line_highlight();
    line.setStyle({color: HILIGHT_COLOUR});
    hilighted_line = line;
}

// Clear any line highlight
function clear_line_highlight() {

    if (hilighted_line !== null) {
        hilighted_line.setStyle({color: NORMAL_COLOUR});
        hilighted_line  = null;
    }

}


// Find an object from a list of objects by matching each object's 'id'
// attribute with the supplied 'id'. Could build/use lookup tables instead?
function find_object(list, id) {

    for (var i = 0; i < list.length; ++i) {
        var object = list[i];
        if (object.id === id) {
            return object;
        }
    }
    console.log('Failed to find object with id ', id);
    return undefined;
}


// Handle site popups
function site_popup(marker) {

    var site = marker.properties.site;

    return '<table>' +
           `<tr><th>Name</th><td>${site.name}</td></tr>` +
           `<tr><th>Description</th><td>${site.description}</td></tr>` +
           `<tr><th>Id</th><td>${site.id}</td></tr>` +
           '</table>';

}


// Handle line popups
function line_popup(polyline) {

    var line = polyline.properties.line;
    var journey = polyline.properties.journey;

    var message = '<table>' +
                  `<tr><th>Name</th><td>${line.name}</td></tr>` +
                  `<tr><th>Description</th><tr>${line.description}</td></tr>` +
                  `<tr><th>Id</th><td>${line.id}</td></tr>` +
                  `<tr><th>Length</th><td>${line.length} m</td></tr>`;
    if (journey) {
        message += `<tr><th>Time</th><td>${journey.time} </dt></tr>` +
                   `<tr><th>Period</th><td>${journey.period} s</td></tr>`;
        if (journey.travelTime) {
            var speed = (line.length / journey.travelTime) * TO_MPH;
            message += `<tr><th>Travel Time</th><td>${journey.travelTime.toFixed(0)}s (${speed.toFixed(1)} mph)</td></tr>`;
        }
        if (journey.normalTravelTime) {
            var normal_speed = (line.length / journey.normalTravelTime) * TO_MPH;
            message += `<tr><th>Normal Travel Time</th><td>${journey.normalTravelTime.toFixed(0)}s (${normal_speed.toFixed(1)} mph)</td></tr>`;
        }
    }

    message += '</table>';

    return message;

}

