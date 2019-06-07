// Javascript functions for displaying Bluetruth data

/* eslint no-console: "off" */
/*global $, L, DRAKEWELL_KEY, MB_ACCESS_TOKEN, TF_API_KEY */

var map, sites_layer, links_layer, compound_routes_layer, layer_control;
var hilighted_line = null;

var LOCATIONS_URL = `https://drakewell02.drakewell.com/npmatchv2/exports/a/locations.asp?group=PORTSMOUTH_JT&key=${DRAKEWELL_KEY}`;
var JOURNEYS_URL = `https://drakewell02.drakewell.com/npmatchv2/exports/a/livejourneytimes.asp?group=PORTSMOUTH_JT&key=${DRAKEWELL_KEY}`;

var NORMAL_COLOUR = '#3388ff';
var HILIGHT_COLOUR = 'red';

var TO_MPH = 2.23694;

var SITE_OPTIONS = {};
var LINK_OPTIONS = { color: NORMAL_COLOUR };

var COMPOUND_ROUTE_OPTIONS = { color: NORMAL_COLOUR };


$(document).ready(function () {

    setup_map();

    load_data();

});


function setup_map() {

    map = new L.Map('map');

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
        'Links': links_layer,
    };

    layer_control = L.control.layers(base_layers, overlay_layers, {collapsed: false}).addTo(map);

    map.on('click', function() {
        if (hilighted_line !== null) {
            hilighted_line.setStyle({color: NORMAL_COLOUR});
        }
    });

}


function load_data() {

    $.when(

        $.get(LOCATIONS_URL),
        $.get(JOURNEYS_URL)

    ).done(function(locations_result, journeys_result) {

        var locations = locations_result[0];
        var journeys = journeys_result[0];

        for (var i = 0; i < locations.sites.length; ++i) {
            var site = locations.sites[i];
            var marker = L.marker([site.location.lat, site.location.lng], SITE_OPTIONS);
            marker.properties = { 'site': site };
            marker.bindPopup(site_popup);
            marker.addTo(sites_layer);
        }

        add_lines(locations.links, locations.sites, journeys, links_layer, LINK_OPTIONS);
        add_lines(locations.compoundRoutes, locations.sites, journeys, compound_routes_layer, COMPOUND_ROUTE_OPTIONS);

        var region = sites_layer.getBounds().extend(links_layer);
        map.fitBounds(region);

    });


}


function add_lines(lines, sites, journeys, layer, options) {

    for (var i = 0; i < lines.length; ++i) {
        var line = lines[i];
        var points = [];
        for (var j = 0; j < line.sites.length; ++j) {
            var site = find_site(sites, line.sites[j]);
            if (site) {
                points.push([site.location.lat, site.location.lng]);
            }
        }
        var polyline = L.polyline(points, options);
        polyline.properties = { 'line': line, 'journey': find_journey(journeys, line.id) };
        polyline.bindPopup(line_popup);
        polyline.on('click', line_highlight);
        polyline.addTo(layer);
        if (layer === compound_routes_layer) {
            layer_control.addOverlay(polyline, `Route: ${line.name}`);
        }
    }

}

function line_highlight(e) {

    var line = e.target;

    if (hilighted_line !== null) {
        hilighted_line.setStyle({color: NORMAL_COLOUR});
    }
    line.setStyle({color: HILIGHT_COLOUR});
    hilighted_line = line;
}


function find_site(sites, id) {

    for (var i = 0; i < sites.length; ++i) {
        var site = sites[i];
        if (site.id === id) {
            return site;
        }
    }
    console.log('Failed to find site id', id);
    return undefined;
}

function find_journey(journeys, id) {

    for (var i = 0; i < journeys.length; ++i) {
        var journey = journeys[i];
        if (journey.id === id) {
            return journey;
        }
    }
    console.log('Failed to find journey id', id);
    return undefined;
}

function site_popup(marker) {

    var site = marker.properties.site;

    return `Name: ${site.name}<br>Description: ${site.description}<br>Id: ${site.id}`;

}

function line_popup(polyline) {

    var line = polyline.properties.line;
    var journey = polyline.properties.journey;

    var message = `Name: ${line.name}<br>Description: ${line.description}<br>` +
        `Id: ${line.id}<br>Length: ${line.length}m`;
    if (journey) {
        var speed = (line.length / journey.travelTime) * TO_MPH;
        var normal_speed = (line.length / journey.normalTravelTime) * TO_MPH;
        message += `<br>Time: ${journey.time}<br>Period: ${journey.period}<br>` +
        `Travel Time: ${journey.travelTime.toFixed(0)}s (${speed.toFixed(1)} mph)<br>` +
        `Normal Travel Time: ${journey.normalTravelTime.toFixed(0)}s (${normal_speed.toFixed(1)} mph)`;
    }

    return message;

}

