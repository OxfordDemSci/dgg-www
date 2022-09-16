var API_URL = "http://127.0.0.1/api/v1/";
var featureByName = {};

import * as _init from './init.js?version=9'
import * as _utils from './utils.js?version=10'
import * as _worldLayer from './worldLayer.js?version=11'
import * as _api from './api_requests.js?version=2'


var initJSONSettings = _api.getSettings(API_URL);
var ymDates = _init.getDates(initJSONSettings.dates);

if (window.mdebug === true){
    console.log(ymDates);
}

var world_geo_json = _init.getWorld_geo();

_init.load_models_to_menu(initJSONSettings.models);

var countriesTemplate_json = _init.getCountries_teamplate();
_init.load_countries_to_menu(initJSONSettings.countries, countriesTemplate_json);


let last_year_month = _utils.getLastDates(ymDates);
const lastYear   = last_year_month[0],
      lastMonth  = last_year_month[1];


let first_year_month = _utils.getFirstDates(ymDates);
const firstYear   = first_year_month[0],
      firstMonth  = first_year_month[1];      

var monthsToDisable = _utils.MonthsYearsToDisable(ymDates,firstYear,lastYear);

if (window.mdebug === true){
    console.log("lastYear " + lastYear + " lastMonth "+ lastMonth);
    console.log("firstYear " + firstYear + " firstMonth "+ firstMonth);
    console.log("monthsToDisable " + monthsToDisable);
}

_init.loadDatesToMenu(firstMonth, firstYear, lastMonth, lastYear, monthsToDisable);

const firstModelfromList = initJSONSettings.models[0];

var data_national = _api.query_national(lastYear, lastMonth);

_utils.hideCoverScreen();

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
        center: [50.378472, 14.970598 ],
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
window.controlTable_Bottom = L.control.bar('table_bottom',{
    position:'bottom',
    visible:true
});
map.addControl(controlTable_Bottom);
controlTable_Bottom.setContent(`<div id="tb_container"></div>`);
controlTable_Bottom.hide();

var worldLayer = L.geoJson(null, {
    style: _worldLayer.style,
    onEachFeature: function (feature, layer) {

        featureByName[feature.properties.iso_a3] = layer;
        layer.on({
            mouseover: _worldLayer.highlightFeature,
            mouseout: function (e) {
                _worldLayer.resetHighlight(e.target, worldLayer);
            },
            click: function (e) {
                _worldLayer.zoomToFeature(e, map, data_national, countriesTemplate_json);
            }
        });
    }.bind(this)
}).addTo(map);



var legendLayer = L.control({position: 'bottomright'});

legendLayer.onAdd = function (map) {
    var legent_text = "Population ";
    // Create Div Element and Populate it with HTML
    var div = L.DomUtil.create('div', 'legend_data');
    div.innerHTML += '<div id="legend_data_info"></div>';
    return div;
};

legendLayer.addTo(map);

var scaleLayer = L.control.scale({position: 'bottomleft'}); // Creating scale control
scaleLayer.addTo(map); 



_worldLayer.load_data_to_worldLayer(lastYear, 
                                    lastMonth, 
                                    firstModelfromList, 
                                    map, 
                                    worldLayer, 
                                    world_geo_json, 
                                    countriesTemplate_json, 
                                    data_national);

map.createPane('labels');
map.getPane('labels').style.zIndex = 650;
map.getPane('labels').style.pointerEvents = 'none';
var cartocdn = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_only_labels/{z}/{x}/{y}.png',{ 
    pane: 'labels'
}).addTo(map);


$('#select_country').on('select2:select', function (e) {
    
    _utils.progressMenuOn();  
    
    var data = e.params.data;
    
    worldLayer.eachLayer(function (layer) {
        if (layer.feature.properties.iso_a2 ===  data.id) {
            map.fitBounds(layer.getBounds(), {paddingBottomRight: [0, 110]});
        }
    });
    
    var sParams = _utils.getSelectedParameters();

     _worldLayer.load_data_to_controlTable_Bottom(data_national.data, 
                                                  sParams[0],
                                                  sParams[1], 
                                                  countriesTemplate_json, 
                                                  sParams[2], 
                                                  data.id);

    _utils.progressMenuOff();
    
});


$("#downloadBtn").click(function (event) {

    var sParams = _utils.getSelectedParameters();
    var d_time = sParams[0]+sParams[1];
    var fname_download = "Digital_Gender_Gaps_" + d_time + ".csv";
    bootbox.confirm({
        closeButton: false,
        message: 'The following file wil be downloaded '+'"'+fname_download+'"',
        callback: function (result) {
            if (result) {
                event.preventDefault();
                event.stopPropagation();
                console.log(result);
                _utils.downloadCSV(data_national.data, d_time, fname_download);
            }
        }
    });

});


$('#select_models').on('change', function() {
    
    _utils.progressMenuOn();
    var select_model = $(this).find(":selected").val();
    var sParams = _utils.getSelectedParameters();
    var d_time = sParams[0]+sParams[1];
    data_national = _api.query_national(sParams[0], sParams[1]);
    
    _worldLayer.load_data_to_worldLayer(sParams[0], 
                                        sParams[1], 
                                        select_model, 
                                        map, 
                                        worldLayer, 
                                        world_geo_json, 
                                        countriesTemplate_json, 
                                        data_national);
    
    _utils.progressMenuOff();
});

$('#datepicker').on('changeMonth', function (e) {   
 
    _utils.progressMenuOn();
    
    var pickedMonth = new Date(e.date).getMonth() + 1;
    var pickedYear = new Date(e.date).getFullYear(); 
    var d_time = pickedYear + pickedMonth;
    var sParams = _utils.getSelectedParameters();
    data_national = _api.query_national(pickedYear, pickedMonth);    
    
    _worldLayer.load_data_to_worldLayer(pickedYear, 
                                        pickedMonth, 
                                        sParams[2], 
                                        map, 
                                        worldLayer, 
                                        world_geo_json, 
                                        countriesTemplate_json, 
                                        data_national);  
                                       
   _utils.progressMenuOff();   
   
});



