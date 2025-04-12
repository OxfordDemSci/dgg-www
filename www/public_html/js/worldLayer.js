import * as _utils from './utils.js?version=2.0'
import * as _api from './api_requests.js?version=2.0'
import * as _controlTable from './bottom_table.js?version=2.0'
import * as _quartile from './quartile.js?version=2.0'

export function get_color(d) {
    for (let i = 0;
    i < breaks2.length; i++) {
        if (d > breaks2[i] && d <= breaks2[i + 1]) {
            return colors2[i];
        }
    }
}

export function style(feature, palette, model) {
    return {
        color: "#ffffff",
        weight: 0,
        fillOpacity: .15,
        fillColor:  getColor(feature.properties.dvalue, palette, model)
    };
}

export function highlightFeature(e) {
    
    var Opacity = document.getElementById("customRangeOpacity").value;
    var dvalue = e.target.feature.properties.dvalue;
    
    if ((dvalue !== undefined) && (dvalue !== null) && (dvalue !== "")) {
    //console.log(e);     
        var layer = e.target;
        // color: '#3388ff',
        layer.setStyle({
            weight: 1,
            color: 'black',
            fillOpacity: Opacity
        });

        if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
            layer.bringToFront();
        }
        
    }

}

export function resetHighlight(e, _layer, palette) {
    //_layer.resetStyle(e.target);
    var sParams = _utils.getSelectedParameters();
    restyleLayer("dvalue", _layer, palette, sParams[2]);
    
}

export function zoomToFeature(_e, _map, _world_geo_json) {

    //var data_national = data_raw.data;
//    var layer = _e.target;
//    var countryCode = _e.target.feature.properties.iso_a2;
//
//    if (window.mdebug === true)
//        console.log("clicked countryCode " + countryCode);
//    
//    var su_dif = _e.target.feature.properties.su_dif;
//    
//
//    if ((su_dif !== undefined) && (su_dif !== null) && (su_dif !== "")) {
//        
//        
//        
//       _map.fitBounds(layer.getBounds(), {paddingBottomRight: [0, 100]});
//        
//       var iso = _e.target.feature.properties.iso_a2; 
//       var sParams = _utils.getSelectedParameters();
//
//      
//    }

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

export function onEachFeature(feature, layer, _map, _layer, _layer_grey, _L1_layer, _year, _month) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: function (e) {
            resetHighlight(e.target, _layer);
        },
        click: function (e) {
            zoomToFeature(e, _map, _layer, _layer_grey, _L1_layer, _year, _month);
        }
    });
}


export function getRandomArbitrary(min, max) {
    return Math.random() * (max - min) + min;
}

const zeroPad = (num, places) => String(num).padStart(places, '0');




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

export function load_data_to_worldLayer(
        year,
        month,
        model,
        model_title,
        _map,
        _layer,
        json,
        data_national,
        _prGroundTruth,
        countriesList,
        palette) {

    _layer.clearLayers();
    _map.removeLayer(_layer);

    var _PredictedError = document.getElementById('chPredictedError');
    let PredictedType="predicted";
    
    if(_PredictedError.checked) {
        PredictedType="predicted_error";
    }

    json.dvalue = null;
    
    for (var i = 0; i < json.features.length; i++) {

        var iso = json.features[i].properties.GID_0;

        if (data_national[iso] && _utils.isContains(countriesList, iso)) {
            if (_prGroundTruth){
                json.features[i].properties.dvalue = data_national[iso][model];
            }else{
                json.features[i].properties.dvalue = data_national[iso][model][PredictedType];
            }
        } else {
            json.features[i].properties.dvalue = null;
        }
    }

    let _country_count;
    if (_prGroundTruth){
        _country_count = Object.keys(data_national).map(key => data_national[key][model]);
    }else{
        _country_count = Object.keys(data_national).map(key => data_national[key][model][PredictedType]);
    }
    //let _country_count = Object.keys(data_national).map(key => data_national[key][model]["predicted"]);
    _country_count = _country_count.filter( Number );

    let breaks = [];
    let cont = 1;
    let Quartile;

    for (var i = 0; i < 10; i++) {
        Quartile = (_quartile.Quartile(_country_count, cont * 0.1).toFixed(3));
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


export function getPaletteGlobalImactMap(dataCountries_counts, palette_colors) {
    
    let  all_country_count = Object.keys(dataCountries_counts).map(key => dataCountries_counts[key].country_count);

    let breaks = [];
    let cont = 1;
    let Quartile;

    
    for (var i = 0; i < 10; i++) {
       Quartile = Math.round(_quartile.Quartile(all_country_count, cont*0.1));
       breaks.push(Quartile);
        cont++;  
    }  

    let breaks_unique = uniqueArray2(breaks);

    let palette_final = [];
    let diference = palette_colors.length-breaks_unique.length;
    for (var i = 0; i < breaks_unique.length; i++) {
             palette_final.push(
                    palette_colors[i+diference]
            );
    }  
    let palette = {"breaks":breaks_unique, "colors":palette_final};
   
    return palette;
 
}