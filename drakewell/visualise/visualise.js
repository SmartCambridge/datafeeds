// Javascript functions for displaying Bluetruth data

/* eslint no-console: "off" */
/*global $, L, LOCATIONS_URL, JOURNEYS_URL, MB_ACCESS_TOKEN, TF_API_KEY */

// m/sec to mph
var TO_MPH = 2.23694;

// Style options for markers and lines
var SITE_OPTIONS = { color: 'black', fillColor: 'green', fill: true, fillOpacity: 0.5, radius: 7, pane: 'markerPane' };
var NORMAL_COLOUR = '#3388ff';
var SLOW_COLOUR = 'red';
var QUICK_COLOUR = 'green';
var BROKEN_COLOUR = '#BBB';

var VERY_SLOW = '#9A111A';
var SLOW = '#E00018';
var MEDIUM = '#EB7F1B';
var FAST = '#85CD50';

var NORMAL_LINE = { weight: 5, offset: -3 };
var HIGHLIGHT_LINE = { weight: 10, offset: -6 };

// Misc script globals
var map, sites_layer, links_layer, compound_routes_layer, layer_control, ledgend;
var hilighted_line = null;
var line_display = 'relative';


// Map link and compoundRoute ids onto the polylines representing them
var line_map = {};

// Initialise
$(document).ready(function () {

    setup_map();
    load_data();

});

// Setup the map environment
function setup_map() {

    map = L.map('map');

    // Various feature layers
    sites_layer = L.featureGroup();
    links_layer = L.featureGroup();
    compound_routes_layer = L.featureGroup();

    // Various map providers
    var osm = L.tileLayer.provider('OpenStreetMap.Mapnik');
    var mb = L.tileLayer.provider('MapBox', {
        id: 'mapbox.streets',
        accessToken: MB_ACCESS_TOKEN
    });
    var tf = L.tileLayer.provider('Thunderforest.Neighbourhood', {
        apikey: TF_API_KEY
    });

    // Layer control
    var base_layers = {
        'MapBox': mb,
        'ThunderForest': tf,
        'OSM': osm,
    };
    var overlay_layers = {
        'Sites': sites_layer,
        'All links': links_layer,
    };
    layer_control = L.control.layers(base_layers, overlay_layers, {collapsed: false}).addTo(map);

    L.control.toggle().addTo(map);

    // Handler to clear any highlighting caused by clicking lines
    map.on('click', clear_line_highlight);

    ledgend = get_legend().addTo(map);

    // Centre on Cambridge and add default layers
    var cambridge = new L.LatLng(52.20038, 0.1197);
    map.setView(cambridge, 15).addLayer(mb).addLayer(sites_layer).addLayer(links_layer);


}


function get_legend() {

    var legend = L.control({position: 'bottomleft'});
    legend.onAdd = function () {
        var div = L.DomUtil.create('div', 'info legend');
        if (line_display === 'relative') {
            div.innerHTML = '<div class="leaflet-control-layers leaflet-control-layers-expanded">' +
                'GREEN: speed is at least 20% above normal<br>' +
                'BLUE: speed close to normal<br>' +
                'RED: speed is at least 20% below normal<br>' +
                'GREY: no speed reported<br>' +
                'Trafic drives on the left. Updates every 60s.' +
                '</div>';
        }
        else {
            div.innerHTML = '<div class="leaflet-control-layers leaflet-control-layers-expanded">' +
                'GREEN: above 20mph<br>' +
                'AMBER: between 10 and 20mph<br>' +
                'RED: between 5 and 10mph<br>' +
                'DARK RED: below 5mph <br>' +
                'GREY: no speed reported<br>' +
                'Trafic drives on the left. Updates every 60s.' +
                '</div>';
        }
        return div;
    };
    return legend;

}


L.Control.Toggle = L.Control.extend({
    onAdd: function() {
        var container = L.DomUtil.create('div', 'toggle leaflet-bar');
        create_button('Absolute', 'Absolute', 'absolute', container, display_absolute);
        create_button('Relative', 'Relative', 'relative', container, display_relative);
        return container;
    },

    onRemove: function() {
        // Nothing to do here
    }
});

L.control.toggle = function(opts) {
    return new L.Control.Toggle(opts);
};

function create_button(html, title, className, container, fn) {
    var link = L.DomUtil.create('a', className, container);
    link.innerHTML = html;
    link.href = '#';
    link.title = title;

    /*
     * Will force screen readers like VoiceOver to read this as "Zoom in - button"
    */
    link.setAttribute('role', 'button');
    link.setAttribute('aria-label', title);

    L.DomEvent.disableClickPropagation(link);
    L.DomEvent.on(link, 'click', L.DomEvent.stop);
    L.DomEvent.on(link, 'click', fn, this);
    //L.DomEvent.on(link, 'click', this._refocusOnMap, this);

    return link;
}


function display_absolute() {
    line_display = 'absolute';
    reload_ledgend();
    load_journey_times();
}

function display_relative() {
    line_display = 'relative';
    reload_ledgend();
    load_journey_times();
}

function reload_ledgend() {
    if (ledgend) {
        ledgend.remove();
    }
    ledgend = get_legend().addTo(map);
}

// Async load locations, annotate with auto-refreshing journey times
function load_data() {

    $.get(LOCATIONS_URL)
        .done(function(locations) {

            // Sites
            add_sites(locations.sites);

            // Links and Compound routes
            add_lines(locations.links, locations.sites, links_layer);
            add_lines(locations.compoundRoutes, locations.sites, compound_routes_layer);

            // Scale map to fit
            var region = sites_layer.getBounds().extend(links_layer);
            map.fitBounds(region);

            // Load (and schedule for reload) journey times
            load_journey_times();

        });

}


// Helper function to draw  sites
function add_sites(sites) {

    for (var i = 0; i < sites.length; ++i) {
        var site = sites[i];
        var marker = L.circleMarker([site.location.lat, site.location.lng], SITE_OPTIONS)
            .bindPopup(site_popup, {maxWidth: 500})
            .addTo(sites_layer);
        marker.properties = { 'site': site };

    }
}


// Helper function to draw links and compound routes
function add_lines(lines, sites, layer) {

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

        var polyline = L.polyline(points, NORMAL_LINE)
            .setStyle({color: NORMAL_COLOUR})
            .bindPopup(line_popup, {maxWidth: 500})
            .on('click', line_highlight)
            .addTo(layer);
        polyline.properties = { 'line': line };

        // Remember the polyline for the future
        line_map[line.id] = polyline;

        // Add compound routes to the map individually, because they can overlap each other
        if (layer === compound_routes_layer) {
            layer_control.addOverlay(polyline, `Route: ${line.name}`);
        }

    }

}


// Load journey times, annotate links and compound routes, and schedule to re-run
function load_journey_times() {

    console.log('(Re-)loading journey times');

    $.get(JOURNEYS_URL)
        .done(function(journeys){

            for (var i = 0; i < journeys.length; ++i) {
                var journey = journeys[i];
                // get corresponding (poly)line
                var line = line_map[journey.id];
                line.properties['journey'] = journey;
                update_line_colour(line);
            }

            // Re-schedule for a minute in the future
            setTimeout(load_journey_times, 60000);

        });

}


// Set line's colour based on corresponding journey's travelTime and
// normalTravelTime
function update_line_colour(polyline) {

    if (polyline !== undefined) {
        var journey = polyline.properties.journey;
        var choice;
        // journeyTime missing
        if (!journey.travelTime) {
            choice = BROKEN_COLOUR;
        }
        else if (line_display === 'relative') {
            // Worse than normal
            if (journey.travelTime > 1.2*journey.normalTravelTime) {
                choice = SLOW;
            }
            // Better then normal
            else if (journey.travelTime < 0.8*journey.normalTravelTime) {
                choice = FAST;
            }
            // Normal(ish)
            else {
                choice = NORMAL_COLOUR;
            }
        }
        else if (line_display === 'absolute') {
            var line = polyline.properties.line;
            var speed = (line.length / journey.travelTime) * TO_MPH;
            if (speed < 5) {
                choice = VERY_SLOW;
            }
            else if (speed < 10) {
                choice = SLOW;
            }
            else if (speed < 20) {
                choice = MEDIUM;
            }
            else {
                choice = FAST;
            }
        }
        polyline.setStyle({color: choice});
    }

}


// Hilight a clicked line
function line_highlight(e) {

    var line = e.target;

    clear_line_highlight();
    line.setStyle(HIGHLIGHT_LINE)
        .setOffset(HIGHLIGHT_LINE.offset);
    hilighted_line = line;
}


// Clear any line highlight
function clear_line_highlight() {

    if (hilighted_line !== null) {
        hilighted_line.setStyle(NORMAL_LINE)
            .setOffset(NORMAL_LINE.offset);
        hilighted_line  = null;
    }

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
