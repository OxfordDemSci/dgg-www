import * as _utils from './utils.js?version=0.24'
import * as _api from './api_requests.js?version=0.1'
import * as _quartile from './quartile.js?version=1'

export function zoomToFeature(_e, _map, _world_geo_json,) {

    var layer = _e.target;
    var iso_gid_0 = _e.target.feature.properties.GID_0;

    for (var i = 0; i < _world_geo_json.features.length; i++) {
			
            var iso = _world_geo_json.features[i].properties.GID_0;
            
            if (iso===iso_gid_0){
                var geoJsonLayer = L.geoJson(_world_geo_json.features[i]);
            }
    }

     _map.fitBounds(geoJsonLayer.getBounds(), {paddingBottomRight: [0, 100]});
    
}

export function getColor(v, palette, model) {
    
    if (v === undefined || v === null) {
        return "#FFFFFF00";
    }

    let xcase = false;
    let color;
    let breaks = palette["breaks"][model];
    let colors = palette["colors"];
    let lp = breaks.length;

    if (breaks[lp - 2] === breaks[lp - 1]) {
        lp--;
        xcase = true;
    } 

    for (let i = 0; i < lp-1 ; i++) {

            if (v >= breaks[i] && v <= breaks[i + 1]) {
                color = colors[i];
            }
    }

    if (xcase && v >= breaks[lp-1]) {
         color = colors[lp-1];
    }  

    return color;

}

export function restyleLayer(propertyName, _layer, palette, model) {

    _layer.eachLayer(function (featureInstanceLayer) {
        var propertyValue = featureInstanceLayer.feature.properties[propertyName];

        if (typeof propertyValue !== 'undefined' && propertyValue !== null) {
            var mFillColor = getColor(propertyValue, palette, model);
            var Opacity = document.getElementById("customRangeOpacity").value;
            featureInstanceLayer.setStyle({
                color: '#888c8d',
                fillColor: mFillColor,
                fillOpacity: Opacity,
                weight: 1
            });
        }

    });
}

export function load_data_to_worldSubNationalLayer(year, 
                                                    month, 
                                                    model, 
                                                    model_title, 
                                                    _map, 
                                                    _layer, 
                                                    json, 
                                                    data_sub_national,
                                                    _prGroundTruth, 
                                                    countriesListSubnational,  
                                                    palette) {
                                                        
    var _PredictedError = document.getElementById('chPredictedError');
    let PredictedType="predicted";
    
    if(_PredictedError.checked) {
        PredictedType="predicted_error";
    }                                                                   

    _layer.clearLayers();
    _map.removeLayer(_layer);

    var m = String(month).padStart(2, '0');
    var year_month = year + m;

    let  _country_count_raw = [];
    json.dvalue = null;
    for (var i = 0; i < json.features.length; i++) {

        var iso_gid_0 = json.features[i].properties.GID_0;
        var iso_gid_1 = json.features[i].properties.GID_1;

        if (iso_gid_0 in data_sub_national) {

            var country_data = data_sub_national[iso_gid_0][iso_gid_1];
            if (country_data && _utils.isContains(countriesListSubnational, iso_gid_1)) {
                
                if (_prGroundTruth){
                    json.features[i].properties.dvalue = country_data[model];
                    _country_count_raw.push(country_data[model]);
                }else{
                    json.features[i].properties.dvalue = country_data[model][PredictedType];
                    _country_count_raw.push(country_data[model][PredictedType]);
                }                
                
                
            } else {
                json.features[i].properties.dvalue = null;
            }
        } else {
            json.features[i].properties.dvalue = null;
        }

    }

    _country_count_raw = _country_count_raw.filter( Number );
    let _country_count = _utils.uniqueArray(_country_count_raw.sort(function (a, b) {return a - b;}));
    _country_count_raw = null;
    

    
    let breaks = [];
    let cont = 1;
    let Quartile;

    for (var i = 0; i < 10; i++) {
       Quartile = (_quartile.Quartile(_country_count, cont*0.1).toFixed(2));
       breaks.push(Quartile);
        cont++;  
    }
  
    breaks[0] = Math.min(..._country_count).toFixed(2);
    palette["breaks"][model] = breaks;
    
    _utils.loadLagent(model_title, palette["colors"], breaks, "subtitles");

    _layer.addTo(_map);
    _layer.addData(json);

    _utils.removeSelectedLayer(_map, "dvalue");

    restyleLayer("dvalue", _layer, palette, model);

}


export function load_data_to_worldSubNationalLayer_ISO(year,
                                                        month, 
                                                        model, 
                                                        model_title, 
                                                        _map, 
                                                        _layer, 
                                                        json, 
                                                        data_sub_national,
                                                        _prGroundTruth, 
                                                        countriesListSubnational, 
                                                        palette, 
                                                        iso) {
                                                            
    var _PredictedError = document.getElementById('chPredictedError');
    let PredictedType="predicted";
    
    if(_PredictedError.checked) {
        PredictedType="predicted_error";
    }                                                            

    _layer.clearLayers();
    _map.removeLayer(_layer);

    var m = String(month).padStart(2, '0');
    var year_month = year + m;

    let _country_count_raw = [];
    json.dvalue = null;
    for (var i = 0; i < json.features.length; i++) {

        var iso_gid_0 = json.features[i].properties.GID_0;
        var iso_gid_1 = json.features[i].properties.GID_1;

        if (iso_gid_0 in data_sub_national) {

            var country_data = data_sub_national[iso_gid_0][iso_gid_1];
            if (country_data && iso_gid_0 === iso && _utils.isContains(countriesListSubnational, iso_gid_1)) {
                
                if (_prGroundTruth){
                    json.features[i].properties.dvalue = country_data[model];
                    _country_count_raw.push(country_data[model]);
                }else{
                    json.features[i].properties.dvalue = country_data[model][PredictedType];
                    _country_count_raw.push(country_data[model][PredictedType]);
                }                      
                
            } else {
                json.features[i].properties.dvalue = null;
            }
        } else {
            json.features[i].properties.dvalue = null;
        }

    }


    let _country_count = _utils.uniqueArray(_country_count_raw.sort(function (a, b) {return a - b;}));
    _country_count_raw = null;

    
    let breaks = [];
    let cont = 1;
    let Quartile;

    for (var i = 0; i < 10; i++) {
       Quartile = (_quartile.Quartile(_country_count, cont*0.1).toFixed(2));
       breaks.push(Quartile);
        cont++;  
    }
  
    breaks[0] = Math.floor(Math.min(..._country_count) * 100) / 100;
    palette["breaks"][model] = breaks;
    
    _utils.loadLagent(model_title, palette["colors"], breaks, "subtitles");

    _layer.addTo(_map);
    _layer.addData(json);

    _utils.removeSelectedLayer(_map, "dvalue");

    restyleLayer("dvalue", _layer, palette, model);

}


export function resetHighlight(e, _layer, palette) {
    //_layer.resetStyle(e.target);
    var sParams = _utils.getSelectedParameters();
    restyleLayer("dvalue", _layer, palette, sParams[2]);
    
}

export function highlightFeature(e) {
    
    var Opacity = document.getElementById("customRangeOpacity").value;
    var dvalue = e.target.feature.properties.dvalue;
    
    if ((dvalue !== undefined) && (dvalue !== null) && (dvalue !== "")) {
 
        var layer = e.target;

        layer.setStyle({
            weight: 1,
            color: 'black'
        });

        if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
            layer.bringToFront();
        }
        
    }

}