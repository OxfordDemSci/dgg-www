var API_URL = "./api/v1/";
var featureByName = {};

import * as _init from './init.js?version=12'
import * as _utils from './utils.js?version=26'
import * as _worldLayer from './worldLayer.js?version=48'
import * as _api from './api_requests.js?version=4'
import * as _plotxyLayer from './plotxyLayer.js?version=7'
import * as _downloadData from './downloadData.js?version=2'

        const config_plot_xy_Chart = {
            type: 'line',
            data: {},
            options: {
                plugins: {
                    legend: {
                        title: {
                            display: false,
                            text: ''
                        }
                    }, subtitle: {
                        display: false,
                        text: ''
                    }
                }
            }
        };

var initJSONSettings = _api.getSettings(API_URL);
var ymDates = _init.getDates(initJSONSettings.dates);
var countriesList = _init.getCountriesList(initJSONSettings.countries);
var palette = _init.getCountriesList(initJSONSettings.palette);

if (window.mdebug === true){
    console.log("countriesList" + countriesList[1]["country"]);
}

var world_geo_json = _init.getWorld_geo();

var modelsList = initJSONSettings.models;

_init.load_models_to_menu(modelsList);

_init.load_countries_to_menu(countriesList);


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
    //console.log("monthsToDisable " + monthsToDisable);
}

_init.loadDatesToMenu(firstMonth, firstYear, lastMonth, lastYear, monthsToDisable);
_init.loadDatesToDownloadMenu(firstMonth, firstYear, lastMonth, lastYear, monthsToDisable);

const firstModelfromList = Object.keys(modelsList)[0];


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
        center: [16.841065, 22.618704],
        zoom: 3,
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



var legendLayer = L.control({position: 'bottomright'});

legendLayer.onAdd = function (map) {
    var legent_text = "legend ";
    var div = L.DomUtil.create('div', 'legend_data');
    div.innerHTML += '<div id="legend_data_info"></div>';
    L.DomEvent.disableClickPropagation(div);
    L.DomEvent.disableScrollPropagation(div);
    return div;
};
//var legendLayer = L.DomUtil.get('legendLayer');

legendLayer.addTo(map);


var scaleLayer = L.control.scale({position: 'bottomleft'});
scaleLayer.addTo(map);


var plotxyLayer = L.control({
        position: 'bottomleft'
});

plotxyLayer.onAdd = function(map) {

        var div = L.DomUtil.create('div', 'leaflet-control-plotxy');
        div.setAttribute('id',"plotxy_div_id");
        div.innerHTML += '<div id="plotxy_div">\n\
        <span id="plotxy_span_close" style="">\n\
        <i class="fa fa-times"></i>\n\
        </span>\n\
        <p class="text-center p-0 m-0 fw-bold" id="plotxy_title"></p>\n\
        <canvas id="plotxyChart" style="padding-left:10px; "></canvas>\n\
        </div>';
        L.DomEvent.disableClickPropagation(div);
        L.DomEvent.disableScrollPropagation(div);    
        return div;
};

plotxyLayer.addTo(map);
_plotxyLayer.display("hide");


var xy_Chart = new Chart(
    document.getElementById('plotxyChart'),
    config_plot_xy_Chart
);


window.controlTable_Bottom = L.control.bar('table_bottom',{
    position:'bottom',
    visible:true
});

controlTable_Bottom.onAdd = function(map) {
this._div = L.DomUtil.get('table_bottom');
    return this._div;
};


map.addControl(controlTable_Bottom);
controlTable_Bottom.setContent(`<div class="progressMenuTable" id="progressMenuTable"><div id="progressMenuTable-content" ></div></div>
                                <a class="button mousechangeHand" id="lbTableMaximize" style="color: #444">
                                <i class="p-2 fa fa-window-maximize" aria-hidden="true" id="iconTableMaximize"></i>
                                </a>
                                <div id="tb_container"></div>
                               `);
controlTable_Bottom.hide();

L.DomEvent.disableClickPropagation(table_bottom);
L.DomEvent.disableScrollPropagation(table_bottom);



var worldLayer = L.geoJson(null, {
    style: function (feature){
        _worldLayer.style(feature, palette, firstModelfromList);
    },
    onEachFeature: function (feature, layer) {

        featureByName[feature.properties.iso_a3] = layer;
        
        layer.on({
            mouseover: _worldLayer.highlightFeature,
            mouseout: function (e) {
                _worldLayer.resetHighlight(e.target, worldLayer, palette);
            },
            click: function (e) {
                    _utils.progressMenuOn();
                    //sidebar.open('home');
                    
                    var sParams = _utils.getSelectedParameters();
                    var iso2code = e.target.feature.properties.iso_a2;
                    //console.log("iso2code " + iso2code);
                    _api.query_model_promis(iso2code, sParams[2], API_URL)
                        .then((data) => {
                            _utils.hilightRowTable(iso2code, countriesList);
                            _plotxyLayer.display("show");
                            _plotxyLayer.updateData(xy_Chart, data, iso2code, sParams[2], modelsList, countriesList);
                            _worldLayer.zoomToFeature(e, map, data, countriesList);
                             }).then(() => {
                              _utils.progressMenuOff();  
                            }).catch((error) => {
                                 console.log(error);
                            });
                            
            }
        });
    }.bind(this)
}).addTo(map);



L.control.zoom({
    position: 'topleft'
}).addTo(map);



_api.query_national_promis(lastYear, lastMonth, API_URL)
        .then((data) => {
            //console.log(data);
            //var data_national = JSON.parse(data.data);
            _worldLayer.load_data_to_worldLayer(
                    lastYear,
                    lastMonth,
                    firstModelfromList,
                    map,
                    worldLayer,
                    world_geo_json,
                    countriesList,
                    data,
                    palette,
                    modelsList);
        }).then(() => {
            _utils.updateModelInfoonPanel(firstModelfromList, modelsList);
            _utils.hideCoverScreen();
            })
        .catch((error) => {
            console.log(error);
        });


map.createPane('labels');
map.getPane('labels').style.zIndex = 650;
map.getPane('labels').style.pointerEvents = 'none';
var cartocdn = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_only_labels/{z}/{x}/{y}.png',{ 
    pane: 'labels'
}).addTo(map);


$('#select_country').on('select2:select', function (e) {

    _utils.progressMenuOn();


    var dataP = e.params.data;

    worldLayer.eachLayer(function (layer) {
        if (layer.feature.properties.iso_a2 === dataP.id) {
            map.fitBounds(layer.getBounds(), {paddingBottomRight: [0, 110]});
        }
    });

    var sParams = _utils.getSelectedParameters();

    _api.query_national_promis(sParams[0], sParams[1], API_URL)
            .then((data) => {
                //console.log(data);
                //var data_national = JSON.parse(data.data);
//                _worldLayer.load_data_to_controlTable_Bottom(data,
//                        sParams[0],
//                        sParams[1],
//                        countriesList,
//                        sParams[2],
//                        dataP.id);

            }).then(() => {
                _utils.progressMenuOff();
            })
            .catch((error) => {
                _utils.progressMenuOff();
                console.log(error);
            });


});



$('#select_models').on('change', function () {
    
    _plotxyLayer.display("hide");
    _utils.progressMenuOn();


    var select_model = $(this).find(":selected").val();
    var sParams = _utils.getSelectedParameters();
    var d_time = sParams[0] + sParams[1];


    _api.query_national_promis(sParams[0], sParams[1], API_URL)
            .then((data) => {
                //console.log(data);
                //var data_national = JSON.parse(data.data);
                _worldLayer.load_data_to_worldLayer(
                        sParams[0],
                        sParams[1],
                        select_model,
                        map,
                        worldLayer,
                        world_geo_json,
                        countriesList,
                        data,
                        palette,
                        modelsList);
            }).then(() => {
                 _utils.updateModelInfoonPanel(select_model, modelsList);
            }).then(() => {
                 _utils.progressMenuOff();
            })
            .catch((error) => {
                _utils.progressMenuOff();
                console.log(error);
            });
  

});

$('#datepicker').on('changeMonth', function (e) {

    _plotxyLayer.display("hide");
    _utils.progressMenuOn();

    var pickedMonth = new Date(e.date).getMonth() + 1;
    var pickedYear = new Date(e.date).getFullYear();
    var d_time = pickedYear + pickedMonth;
    var sParams = _utils.getSelectedParameters();

    _api.query_national_promis(pickedYear, pickedMonth, API_URL)
            .then((data) => {
                //console.log(data);
                //var data_national = JSON.parse(data.data);
                _worldLayer.load_data_to_worldLayer(pickedYear,
                        pickedMonth,
                        sParams[2],
                        map,
                        worldLayer,
                        world_geo_json,
                        countriesList,
                        data,
                        palette,
                        modelsList);
            }).then(() => {
                _utils.progressMenuOff();
            })
            .catch((error) => {
                _utils.progressMenuOff();
                console.log(error);
            });
});



$("#plotxy_span_close").click(function(event) {
        _plotxyLayer.display("hide");
        event.stopPropagation();
}); 


$("#btnDownloadData").click(function (event) {
   
    var pickedStartingDate = $("#datepicker_start_date").datepicker('getDate');
    var pickedEndingDate = $("#datepicker_end_date").datepicker('getDate');

    if (_downloadData.isBeforeDate(pickedStartingDate, pickedEndingDate)){
        
        _utils.progressMenuOn();
        
            var formattedDateStart = moment(pickedStartingDate).format('YYYYMM');
            var formattedDateEnd = moment(pickedEndingDate).format('YYYYMM');
            _api.download_data_with_dates(formattedDateStart, 
                                          formattedDateEnd,
                                          API_URL)
            .then((data) => {
                  _downloadData.downloadCSV(data, formattedDateStart, formattedDateEnd, countriesList, modelsList);
    
            }).then(() => {
                sidebar.open("home");
                $("#ToastDownloadCompleted").toast("show"); 
                _utils.progressMenuOff();
            })
            .catch((error) => {
                _utils.progressMenuOff();
                console.log(error);
            });
        

    }else{
        $("#ToastRrrorDownload").toast("show"); 
    }
});


$('#chCountryLabels').change(function () {
        if ($(this).is(":checked")) {
             map.addLayer(cartocdn);
        } else {
            map.removeLayer(cartocdn);
        }
});

$('#chLegend').change(function () {
        var x = document.getElementById("legend_data_info");
        if ($(this).is(":checked")) {
              x.style.display = "block";
        } else {
              x.style.display = "none";
        }
});

$('#customRangeOpacity').change(function () {

        worldLayer.setStyle({
            fillOpacity: $(this).val()
        });     
});

$("#mailtoLink").click(function (e) {
    e.preventDefault();
    e.stopPropagation();
    window.location.href = "mailto:"+initJSONSettings.contact;
});


//$('.link-table-zoom').on("click",  function (event) {
//    event.preventDefault();
//    alert("title");
//    var self = $(this);
////    var link = self.find(self.data('target')).attr('href');
//    var title = self.attr('title');
//    
//    alert(title);
//    event.stopPropagation();
//});



