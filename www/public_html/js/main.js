import * as _initSettings from './init.js?version=2'
import * as _utils from './utils.js?version=2'

var initJSONSettings = _initSettings.getInitSettings();
var ymDates = _initSettings.getDates(initJSONSettings.dates);


_utils.load_year_to_menu(ymDates);
_utils.load_models_to_menu(initJSONSettings.models);

_utils.load_countries_to_menu(initJSONSettings.countries);
_utils.load_data_to_tb();




var basemaps = {
        "OpenStreetMaps": L.tileLayer(
            "https://cartodb-basemaps-b.global.ssl.fastly.net/light_nolabels/{z}/{x}/{y}.png", {
                attribution: "<a href='http://www.esri.com/'>Esri</a>, HERE, Garmin, (c) OpenStreetMap",
                minZoom: 1,
                maxZoom: 14,
                id: "osm.streets"
            }
        )
    };

    var mapOptions = {
        zoomControl: false,
        attributionControl: false,
        center: [0.09, 18.54],
        zoom: 4,
        maxZoom: 11,
        layers: [basemaps.OpenStreetMaps]
    };


var map = L.map("map", mapOptions);
map.invalidateSize();

var sidebar = L.control.sidebar('sidebar', {
        position: 'right',
        container: "sidebar",
        autopan: true
}).addTo(map);
sidebar.open("home");


// https://github.com/filipzava/leaflet-control-bar
window.controlBar = L.control.bar('table_bottom',{
    position:'bottom',
    visible:true
});
map.addControl(controlBar);
controlBar.hide();
controlBar.setContent(`<div id="tb_container">
</div>`);