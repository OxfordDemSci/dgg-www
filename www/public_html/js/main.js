var API_URL = "./api/v2/";
var featureByName = {};

import * as _init from './init.js?version=0.73'
import * as _utils from './utils.js?version=0.675'
import * as _api from './api_requests.js?version=0.35'
import * as _worldLayer from './worldLayer.js?version=0.51'
import * as _worldSubNationalLayer from './worldSubNationalLayer.js?version=0.82'
import * as _worldBoundariesLayer from './worldBoundariesLayer.js?version=0.462'
import * as _controlTable from './bottom_table.js?version=0.1653'
import * as _plotxyLayer from './plotxyLayer.js?version=0.36'
import * as _infoBox from './infoBox.js?version=0.22'

import * as _palette from './palette.js?version=0.222'
import * as _modelsList from './models_list.js?version=0.12'

import * as _download from './download_csv.js?version=0.12'


var prSubNational = false;
var prGroundTruth = false;
var prPredictedError = false;

var loadGeoBoundaryFroDB = false;

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

const palette = _palette.loadPalette();
const modelsList = _modelsList.loadModelsList();

var data_plot=[];

var initJSONSettings = _api.getSettings(API_URL);

var ymDates = _init.getDates(initJSONSettings.national.dates);
var ymDates_Subnational = _init.getDates(initJSONSettings.subnational.dates);

var countriesList = _init.getCountriesList(initJSONSettings.national.countries);

let last_year_month = _utils.getLastDates(ymDates);
const lastYear   = last_year_month[0],
      lastMonth  = last_year_month[1];

let first_year_month = _utils.getFirstDates(ymDates);
const firstYear   = first_year_month[0],
      firstMonth  = first_year_month[1];      

var monthsToDisable = _utils.MonthsYearsToDisable(ymDates,firstYear,lastYear);

let last_year_month_Sub = _utils.getLastDates(ymDates_Subnational);
const lastYear_Sub   = last_year_month_Sub[0],
      lastMonth_Sub  = last_year_month_Sub[1];

let first_year_month_Sub = _utils.getFirstDates(ymDates_Subnational);
const firstYear_Sub   = first_year_month_Sub[0],
      firstMonth_Sub  = first_year_month_Sub[1];      

var monthsToDisable_Sub = _utils.MonthsYearsToDisable(ymDates_Subnational,firstYear_Sub,lastYear_Sub);

_init.loadDatesToMenu(firstMonth, firstYear, lastMonth, lastYear, monthsToDisable, true);

const firstModelfromList = Object.keys(modelsList)[0];

_init.load_models_to_menu(modelsList, initJSONSettings.descriptions);

    var world_geo_json = [];
    var worldSubNational_geo_json = [];
    
if (loadGeoBoundaryFroDB){
    world_geo_json = _api.getWorld_geo_db(API_URL);
    worldSubNational_geo_json = _api.getWorldSubNational_geo_db(API_URL);
}else{
    world_geo_json = _init.getWorld_geo();
    worldSubNational_geo_json = _init.getWorldSubNational_geo();
}

var basemaps = {
        "OpenStreetMaps": L.tileLayer(
            "https://cartodb-basemaps-b.global.ssl.fastly.net/light_nolabels/{z}/{x}/{y}.png", {
                attribution: "<a href='http://www.esri.com/'>Esri</a>, HERE, Garmin, (c) OpenStreetMap",
                minZoom: 1,
                maxZoom: 14,
                // noWrap: true,
                id: "osm.streets"
            }
        )
    };

    var mapOptions = {
        zoomControl: false,
        attributionControl: false,
        center: [20, 40],
        zoom: 4,
        maxZoom: 11,
        minZoom: 2,
        maxBounds: [[90, -180],[-75, 230]],
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

L.DomEvent.disableClickPropagation(controlTable_Bottom);
L.DomEvent.disableScrollPropagation(controlTable_Bottom);



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

L.control.zoom({
    position: 'topleft'
}).addTo(map);


var worldLayer = L.geoJson(null, {
    style: function (feature){
        return {
            color: "#ffffff",
            weight: 0,
            fillOpacity: .0,
            fillColor:  "#ffffff"
        };
    },
    onEachFeature: function (feature, layer) {

        //featureByName[feature.properties.iso_a3] = layer;
        
        layer.on({
            mouseover: _worldLayer.highlightFeature,
            mouseout: function (e) {
                _worldLayer.resetHighlight(e.target, worldLayer, palette);
            },
            click: function (e) {
                
                _utils.progressMenuOn();
                var iso_gid_0 = e.target.feature.properties.GID_0;
                    _api.query_national_data_with_dates(firstYear, firstMonth, lastYear, lastMonth , iso_gid_0, prGroundTruth, API_URL)
                        .then((data) => {
                                var sParams = _utils.getSelectedParameters();
                                if (prGroundTruth){
                                    
                                    let _countriesList = _utils.getContriesList(initJSONSettings, prGroundTruth);
                                    
                                    _plotxyLayer.display("hide");
                                    _infoBox.display("show");
                                    
                                     let _countryName = _countriesList.find(x => x["iso3code"] === iso_gid_0)["country"].substring(0, 25);
                                    _infoBox.updateInfoBox(modelsList[sParams[2]].name, 
                                                           data[iso_gid_0][sParams[2]] , 
                                                           _countryName, 
                                                           data[iso_gid_0]["survey_year"], 
                                                           data[iso_gid_0]["source"] );                                    
                                }else{
                                    _infoBox.display("hide");
                                    _plotxyLayer.display("show");
                                    var sParams = _utils.getSelectedParameters();
                                    
                                    data_plot=data[iso_gid_0];
                                    _plotxyLayer.updateData(xy_Chart, data[iso_gid_0], sParams[2], initJSONSettings.descriptions, prSubNational);                                    
                                }

                             }).then(() => {

                                 var sParams = _utils.getSelectedParameters();
                                 let _countriesList = _utils.getContriesList(initJSONSettings, prGroundTruth);
                                 let _countriesListSubnational = _utils.getContriesListSubnational(initJSONSettings, prGroundTruth);
                                     
                                _api.query_national_promis(sParams[0], sParams[1], sParams[2], prGroundTruth, API_URL)
                                .then((data) => {   
                                    _utils.progressMenuTableOn();
                            
                                    data = Object.keys(data).filter(x => data[x][sParams[2]] !== undefined).reduce((obj, key) => {
                                        obj[key] = data[key];
                                        return obj;
                                    }, {});                                
                            
                                    _api.query_sub_national_promis(sParams[0], sParams[1], sParams[2], prGroundTruth, API_URL).then((data_sub) => {
                                        _controlTable.load_data_BottomTable(data, data_sub, prGroundTruth, _countriesList, _countriesListSubnational, sParams[2], modelsList, iso_gid_0, true, true);
                                    }).then(() => {
                                        _utils.progressMenuTableOff();  
                                    }).catch((error) => {
                                        console.log(error);
                                    });
                
                                }).catch((error) => {
                                    console.log(error);
                                });

                             _worldLayer.zoomToFeature(e, map, world_geo_json);         
                             }).then(() => {
                              _utils.progressMenuOff();  
                            }).catch((error) => {
                                _utils.progressMenuOff();  
                                 console.log(error);
                            }); 
                            
                            
                            
            }
        });
    }.bind(this)
}).addTo(map);






var worldSubNationalLayer = L.geoJson(null, {
    style: function (feature) {
        return {
            color: "#ffffff",
            weight: 0,
            fillOpacity: .0,
            fillColor: "#ffffff"
        };
    },
    onEachFeature: function (feature, layer) {

        layer.on({
            mouseover: _worldSubNationalLayer.highlightFeature,
            mouseout: function (e) {
                _worldSubNationalLayer.resetHighlight(e.target, worldSubNationalLayer, palette);
            },
            click: function (e) {
                
                 let _countriesListSubnational = _utils.getContriesListSubnational(initJSONSettings, prGroundTruth);
                 
                var iso_gid_0 = e.target.feature.properties.GID_0;
                var iso_gid_1 = e.target.feature.properties.GID_1;

                var sParams = _utils.getSelectedParameters();
                let vModel_title = initJSONSettings["descriptions"]["indicator"][sParams[2]].name;
                _utils.progressMenuOn();
                _api.query_sub_national_promis(sParams[0], sParams[1], sParams[2], prGroundTruth, API_URL)
                        .then((data) => {
                            _worldSubNationalLayer.load_data_to_worldSubNationalLayer_ISO(
                                    sParams[0],
                                    sParams[1],
                                    sParams[2],
                                    vModel_title,
                                    map,
                                    worldSubNationalLayer,
                                    worldSubNational_geo_json,
                                    data,
                                    prGroundTruth,
                                    _countriesListSubnational,
                                    palette,
                                    iso_gid_0);
                             return(data);       
                        }).then((data) => {
                                
                                _utils.progressMenuTableOn();
                                 let _countriesList = _utils.getContriesList(initJSONSettings, prGroundTruth);
                                     
                                _api.query_national_promis(sParams[0], sParams[1], sParams[2], prGroundTruth, API_URL)
                                .then((data_naional) => {   
                                    _controlTable.load_data_BottomTable(data_naional, data, prGroundTruth, _countriesList, _countriesListSubnational, sParams[2], modelsList, iso_gid_0, true, true);
                                }).then(() => {
                                    _utils.progressMenuTableOff();  
                                }).catch((error) => {
                                    console.log(error);
                                });                            
                            
                          
                        }).then(() => {
                            
                    _api.query_sub_national_data_with_dates(firstYear_Sub, firstMonth_Sub, lastYear_Sub, lastMonth_Sub, iso_gid_1, prGroundTruth, API_URL)
                            .then((data) => {
                                var sParams = _utils.getSelectedParameters();
                                if (prGroundTruth){
                                    _plotxyLayer.display("hide");
                                    _infoBox.display("show");
                                     let _regionName = _countriesListSubnational.find(x => x["admin_id"] === iso_gid_1)["region_name"].substring(0, 25);
                                    _infoBox.updateInfoBox(modelsList[sParams[2]].name, 
                                                           data[iso_gid_0][iso_gid_1][sParams[2]] , 
                                                           _regionName, 
                                                           data[iso_gid_0][iso_gid_1]["survey_year"], 
                                                           data[iso_gid_0][iso_gid_1]["source"] );

                                }else{
                                    _infoBox.display("hide");
                                    _plotxyLayer.display("show");
                                     data_plot=data[iso_gid_0][iso_gid_1];
                                    _plotxyLayer.updateData(xy_Chart, data[iso_gid_0][iso_gid_1], sParams[2], initJSONSettings.descriptions, prSubNational);
                                }
                 
                            }).then(() => {
                        _utils.progressMenuOff();  
                    }).catch((error) => {
                        _utils.progressMenuOff();  
                        console.log(error);
                    });
                    _utils.showRefreshButton();
                    _worldSubNationalLayer.zoomToFeature(e, map, world_geo_json);  
                }).then(() => {
                        _utils.progressMenuOff();  
                }).catch((error) => {
                            _utils.progressMenuOff();
                            console.log(error);
                });


            },
            filter: function (feature, layer) {                     
                //console.log("asas");
            }
        });
    }.bind(this)
}).addTo(map);


var worldBoundariesLayer = L.geoJson(null, {
    style: function (){
        return {
            color: "#888c8d",
            weight: 1,
            fillOpacity: 0
        };
    },
    onEachFeature: function (feature, layer) {
      layer.on({
            mouseover: _worldBoundariesLayer.highlightFeature,
            mouseout: function (e) {
                _worldBoundariesLayer.resetHighlight(e.target, worldBoundariesLayer);
            },
            click: function (e) {
                            
            }
        });
    }.bind(this)
}).addTo(map);


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


var infoBoxLayer = L.control({
        position: 'bottomleft'
});

infoBoxLayer.onAdd = function(map) {

        var div = L.DomUtil.create('div', 'leaflet-control-infoBox');
        div.setAttribute('id',"infoBox_div_id");
        div.innerHTML += '<div id="infoBox_div">\n\
        <span id="infoBox_span_close" style="">\n\
        <i class="fa fa-times"></i>\n\
        </span>\n\
        <p class="pl-3 m-1 fw-bold" id="infoBox_title_model">Mobile women : 45</p>\n\
        <p class="pl-2 m-1" id="infoBox_title_iso">AFG</p>\n\
        <p class="pl-2 m-1" id="infoBox_title_survey_year">Survey year : 2016</p>\n\
        <p class="pl-2 m-1" id="infoBox_title_source">Source : dhc</p>\n\
        </div>';
        L.DomEvent.disableClickPropagation(div);
        L.DomEvent.disableScrollPropagation(div);    
        return div;
};

infoBoxLayer.addTo(map);
_infoBox.display("hide");


map.createPane('labels');
map.getPane('labels').style.zIndex = 650;
map.getPane('labels').style.pointerEvents = 'none';
var cartocdn = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_only_labels/{z}/{x}/{y}.png',{ 
    pane: 'labels'
}).addTo(map);

//var cartocdn = L.tileLayer('https://{s}.basemaps.cartocdn.com/{z}/{x}/{y}' + (L.Browser.retina ? 'light_only_labels@2x.png' : '.png'), {
//   attribution:'&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attributions">CARTO</a>',
//   subdomains: 'abcd',
//   maxZoom: 20,
//   minZoom: 0,
//   pane: 'labels'
// }).addTo(map);

function main_query_national(vYear, vMonth, vModel, vGroundTruth, api_url, _map, _wLayer, _geojson, _palette) {

    _utils.showCoverScreen();
    let _countriesList = _utils.getContriesList(initJSONSettings, prGroundTruth);
    let _countriesListSubnational = _utils.getContriesListSubnational(initJSONSettings, prGroundTruth);
    let vModel_title = initJSONSettings["descriptions"]["indicator"][vModel].name;
    _utils.progressMenuTableOn();
    _api.query_national_promis(vYear, vMonth, vModel, vGroundTruth, api_url)
            .then((data) => {
                //clean the data from undefined
                data = Object.keys(data).filter(x => data[x][vModel] !== undefined).reduce((obj, key) => {
                    obj[key] = data[key];
                    return obj;
                }, {});
  
                _worldLayer.load_data_to_worldLayer(
                        vYear,
                        vMonth,
                        vModel,
                        vModel_title,
                        _map,
                        _wLayer,
                        _geojson,
                        data,
                        prGroundTruth,
                        _countriesList,
                        _palette);
                return(data);
            }).then(function (data) {

        let iso = null;
        _api.query_sub_national_promis(vYear, vMonth, vModel, vGroundTruth, api_url).then((data_sub) => {
            _controlTable.load_data_BottomTable(data, data_sub, vGroundTruth, _countriesList, _countriesListSubnational, vModel, modelsList, iso, true, false);
        }).then(() => {
            _utils.progressMenuTableOff();
        }).catch((error) => {
            console.log(error);
        });

        _utils.updateModelInfoonPanel(vModel, initJSONSettings.descriptions, prGroundTruth);
        _utils.hideCoverScreen();
    })
            .catch((error) => {
                _utils.hideCoverScreen();
                _utils.progressMenuTableOff();
                console.log(error);
            });

}

function main_query_sub_national(vYear, vMonth, vModel, vGroundTruth, api_url, _map, _wLayer, _geojson, _palette) {
    
    _utils.showCoverScreen();
    let _countriesList = _utils.getContriesList(initJSONSettings, prGroundTruth);
    let _countriesListSubnational = _utils.getContriesListSubnational(initJSONSettings, prGroundTruth);
    let vModel_title = initJSONSettings["descriptions"]["indicator"][vModel].name;
    _utils.progressMenuTableOn();
    _api.query_sub_national_promis(vYear, vMonth, vModel, vGroundTruth, api_url)
            .then((data) => {
                _worldSubNationalLayer.load_data_to_worldSubNationalLayer(
                        vYear,
                        vMonth,
                        vModel,
                        vModel_title,
                        _map,
                        _wLayer,
                        _geojson,
                        data,
                        prGroundTruth,
                        _countriesListSubnational,
                        _palette);
                        return(data);
            }).then((data_sub) => {
                let iso=null; 
                _api.query_national_promis(vYear, vMonth, vModel, vGroundTruth, api_url).then((data) => {
                    
                    //clean the data from undefined
                    data = Object.keys(data).filter(x => data[x][vModel] !== undefined).reduce((obj, key) => {
                        obj[key] = data[key];
                        return obj;
                    }, {});                    
                    
                    _controlTable.load_data_BottomTable(data, data_sub, vGroundTruth, _countriesList, _countriesListSubnational, vModel, modelsList, iso, true, false);
                }).then(() => {
                    _utils.progressMenuTableOff();  
                }).catch((error) => {
                    console.log(error);
                }); 
                _utils.hideCoverScreen();
                 _utils.updateModelInfoonPanel(vModel, initJSONSettings.descriptions, prGroundTruth);
    })
            .catch((error) => {
                _utils.hideCoverScreen();
                _utils.progressMenuTableOff();  
                console.log(error);
            });

}

main_query_national(lastYear, lastMonth, firstModelfromList, prGroundTruth, API_URL, map, worldLayer, world_geo_json, palette);

_utils.hideCoverScreen();
_utils.progressMenuOff();
_utils.progressMenuTableOff();  

function main_query(_prSubNational, _prGroundTruth) {
    
    _plotxyLayer.display("hide");
    _infoBox.display("hide");
    
    var select_model = $('#select_models').find(":selected").val();
    var sParams = _utils.getSelectedParameters();
        if (_prSubNational) {
            if (worldLayer) {
                worldLayer.clearLayers();
                map.removeLayer(worldLayer);
                main_query_sub_national(sParams[0], sParams[1], sParams[2], _prGroundTruth, API_URL, map, worldSubNationalLayer, worldSubNational_geo_json, palette);
            }
        } else {
            if (worldSubNationalLayer) {
                worldSubNationalLayer.clearLayers();
                worldBoundariesLayer.clearLayers();
                map.removeLayer(worldBoundariesLayer);
                map.removeLayer(worldSubNationalLayer);
                main_query_national(sParams[0], sParams[1], sParams[2], _prGroundTruth, API_URL, map, worldLayer, world_geo_json, palette);
                _utils.hideRefreshButton();
            }            
        }

}


$('#chSubNational').change(function () {

    var sParams = _utils.getSelectedParameters();

    if ($(this).is(":checked")) {
        
        prSubNational = true;
        
        if (_utils.check_if_date_exists_Sub(parseInt(sParams[0]), parseInt(sParams[1]), ymDates_Subnational) === true) {
        
             _init.loadDatesToMenu(firstMonth_Sub, firstYear_Sub, lastMonth_Sub, lastYear_Sub, monthsToDisable_Sub, false); 
            $('#datepicker').datepicker('setDate', parseInt(sParams[0]) + '-' + parseInt(sParams[1]));
            
        }else{
             _init.loadDatesToMenu(firstMonth_Sub, firstYear_Sub, lastMonth_Sub, lastYear_Sub, monthsToDisable_Sub, true);
        }
        
    } else {
        
        prSubNational = false;
        _init.loadDatesToMenu(firstMonth, firstYear, lastMonth, lastYear, monthsToDisable, true);
        
    }

   // main_query(prSubNational, prGroundTruth);

});


$('#chGroundTruth').change(function () {
    
        if ($(this).is(":checked")) {
            prGroundTruth=true;
            document.getElementById("chPredictedError").disabled=true;
        } else {
            prGroundTruth=false;
            document.getElementById("chPredictedError").disabled=false;
        }
        main_query(prSubNational, prGroundTruth);
});

$('#chPredictedError').change(function () {
    
        if ($(this).is(":checked")) {
            prPredictedError=true;
            document.getElementById("chGroundTruth").disabled=true;
        } else {
            document.getElementById("chGroundTruth").disabled=false;
            prPredictedError=false;
        }
        main_query(prSubNational, prGroundTruth);
});




$('#select_models').on('change', function () {
//    _plotxyLayer.display("hide");
//    var chSubNational= document.getElementById('chSubNational');
//    
//    var select_model = $(this).find(":selected").val();
//    var sParams = _utils.getSelectedParameters();
//    var d_time = sParams[0] + sParams[1];
//
//    if (chSubNational.checked){
//        main_query_sub_national(sParams[0], sParams[1], select_model, prGroundTruth,  API_URL, map, worldSubNationalLayer, worldSubNational_geo_json, palette);
//    }else{
//        main_query_national(sParams[0], sParams[1], select_model, prGroundTruth, API_URL, map, worldLayer, world_geo_json, palette, countriesList, modelsList);
//    }
    main_query(prSubNational, prGroundTruth);
});



$("#lbTableMaximize").click(function () {

    var minPanelStatus = true;
    
    let _countriesList = _utils.getContriesList(initJSONSettings, prGroundTruth);
    let _countriesListSubnational = _utils.getContriesListSubnational(initJSONSettings, prGroundTruth);

    if ($("#iconTableMaximize").hasClass("fa-window-minimize")) {
        minPanelStatus = true;
    } else {
        minPanelStatus = false;
    }
    $(".fa-window-maximize").toggleClass("fa-window-minimize");
    
    var select_model = $(this).find(":selected").val();
    var sParams = _utils.getSelectedParameters();

    var coverScreen = document.getElementById('coverScreen');
    coverScreen.style.visibility = 'visible';
    
    _api.query_national_promis(sParams[0], sParams[1], sParams[2], prGroundTruth, API_URL)
        .then((data) => {
                    return(data);
        }).then(function (data)  {
                _api.query_sub_national_promis(sParams[0], sParams[1], sParams[2], prGroundTruth, API_URL).then((data_sub) => {
                    _controlTable.load_data_BottomTable(data, data_sub, prGroundTruth, _countriesList, _countriesListSubnational, sParams[2], modelsList,  null, minPanelStatus, false);
                    //_controlTable.load_data_BottomTable(data, data_sub, initJSONSettings, select_model, modelsList, worldSubNationalLayer, map,  null, minPanelStatus);
                    _utils.hideCoverScreen();
                }).catch((error) => {
                    console.log(error);
                    _utils.hideCoverScreen();
                });
            })
        .catch((error) => {
            console.log(error);
            _utils.hideCoverScreen();
        });    

});


$("#plotxy_span_close").click(function(event) {
        _plotxyLayer.display("hide");
        event.stopPropagation();
}); 

$("#infoBox_span_close").click(function(event) {
        _infoBox.display("hide");
        event.stopPropagation();
});


$("#refreshButton").click(function(event) {
    _utils.hideRefreshButton();
    
    var sParams = _utils.getSelectedParameters();
    
    main_query_sub_national(sParams[0], sParams[1], sParams[2], prGroundTruth, API_URL, map, worldSubNationalLayer, worldSubNational_geo_json, palette);
    _plotxyLayer.display("hide");
    _infoBox.display("hide");
    map.setZoom(4);
});


$('#datepicker').datepicker().on('changeDate', function (e) {
       main_query(prSubNational, prGroundTruth);
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
        worldSubNationalLayer.setStyle({
            fillOpacity: $(this).val()
        });         
});


$( "#btnDownloadData" ).on( "click", function() {
    _download.download_csv(API_URL);
});


$('#chPointPlot').change(function () {
    
        if ($(this).is(":checked")) {
            document.getElementById('chPointRadius').disabled =false;
        } else {
              document.getElementById('chPointRadius').disabled =true;
        }
        var sParams = _utils.getSelectedParameters();
        _plotxyLayer.updateData(xy_Chart, data_plot, sParams[2], initJSONSettings.descriptions, prSubNational);           

});


$('#chPointRadius').on("input", function () {
     document.getElementById('lbPointRadius').innerHTML = $(this).val();
});
$('#chPointRadius').change(function () {
     var sParams = _utils.getSelectedParameters();
    _plotxyLayer.updateData(xy_Chart, data_plot, sParams[2], initJSONSettings.descriptions, prSubNational);    
});


$('#chLineStrokeWidth').on("input", function () {
     document.getElementById('lbLineStrokeWidth').innerHTML = $(this).val();
});
$('#chLineStrokeWidth').change(function () {
    var sParams = _utils.getSelectedParameters();
    _plotxyLayer.updateData(xy_Chart, data_plot, sParams[2], initJSONSettings.descriptions, prSubNational);    
});

