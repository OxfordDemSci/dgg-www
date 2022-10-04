import * as _utils from './utils.js?version=6'
import * as _api from './api_requests.js?version=1'



//var breaks = [1, 0.2, 0.4, 0.6, 0.8, 1, 1.1, 1.2, 1.3, 1.4];
//var colors = ["#e76254", "#ef8a47", "#f7aa58", "#ffd06f", "#ffe6b7", "#aadce0", "#72bcd5", "#528fad", "#376795", "#1e466e"];

var breaks = [];
var colors = [];


export function get_color(d) {
    for (let i = 0;
    i < breaks.length; i++) {
        if (d > breaks[i] && d <= breaks[i + 1]) {
            return colors[i];
        }
    }
}

export function style(feature) {

    return {
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7,
        fillColor: get_color(feature.properties.su_dif)
    };
}

export function highlightFeature(e) {

    var su_dif = e.target.feature.properties.su_dif;
    if ((su_dif !== undefined) && (su_dif !== null) && (su_dif !== "")) {
        
        var layer = e.target;

        layer.setStyle({
            weight: 1,
            color: '#666',
            dashArray: '',
            fillOpacity: 0.7
        });

        if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
            layer.bringToFront();
        }
        
    }

}

export function resetHighlight(e, _layer) {
    _layer.resetStyle(e.target);
}

export function zoomToFeature(_e, _map, data_national, countriesTemplate_json) {

    var layer = _e.target;
    var countryCode = _e.target.feature.properties.iso_a2;

    if (window.mdebug === true)
        console.log("clicked countryCode " + countryCode);
    
    var su_dif = _e.target.feature.properties.su_dif;
    

    if ((su_dif !== undefined) && (su_dif !== null) && (su_dif !== "")) {
        
        _utils.progressMenuOn();
        
        _map.fitBounds(layer.getBounds(), {paddingBottomRight: [0, 100]});
        
       var iso = _e.target.feature.properties.iso_a2; 
       var sParams = _utils.getSelectedParameters();

       load_data_to_controlTable_Bottom(data_national.data, 
                                        sParams[0],
                                        sParams[1], 
                                        countriesTemplate_json, 
                                        sParams[2], 
                                        iso); 
                                        
       _utils.progressMenuOff();                                 
        
    }

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

export function load_data_to_controlTable_Bottom(data, ytime, mtime, countriesTemplate_json, model_selected, iso=null) {

    var tb_container = document.getElementById('tb_container');

    var d_time = ytime + String(mtime).padStart(2, '0');
    var models = [];

    // getting first country in the data
    var fCountry = Object.keys(data)[0];

    // getting the list of models
    for (var k in data[fCountry][d_time]) {
        models.push(k);
    }


    var tb_updated = `
<table class="table" >
  <colgroup>
    <col class=""></col>
    <col class=""></col>`;

    for (var i = 0; i < models.length; i++) {

        if (models[i] === model_selected) {
            tb_updated = tb_updated + '<col class="" style="background-color: #D7D4D4"></col>';
        } else {
            tb_updated = tb_updated + '<col></col>';
        }

    }



    tb_updated = tb_updated + '</colgroup>';


    var tb_updated = tb_updated + `<thead>
    <tr>
      <th scope="col"></th>
      <th scope="col">Country</th>`;

    for (var i = 0; i < models.length; i++) {
        var nameModel = models[i].replace(/_/g, " ");

        tb_updated = tb_updated + '<th scope="col">' + nameModel + '</th>';
    }

    tb_updated = tb_updated + '</tr></thead<tbody>';

    for (var k in data) {
        
        var hilighted_country_style = '';
        if (_utils.isEmpty(iso)){
            hilighted_country_style = '';
            console.log("iso is emty " + iso);
        }else{
            console.log("iso is not emty " + iso);
            if (iso === k) hilighted_country_style = 'style="background-color: #D7D4D4"';
        }

        var country_name = countriesTemplate_json.find(x => x["alpha-2"] === k)["name"];

        tb_updated = tb_updated + `
                            <tr ` + hilighted_country_style + `>
                                <td class="fib" style="background-image: url(../img/flags/4x3/` + k + `.svg);background-size: 75% 75%;"></td>
                                <td>` + country_name + `</td>`;

        var country_date = data[k][d_time];

        for (var m in country_date) {

            tb_updated = tb_updated + `
                                <td>` + country_date[m] + `</td>`;

        }
        tb_updated = tb_updated + `</tr>`;
    }

    tb_updated = tb_updated + `</tbody></table>`;

    tb_container.innerHTML = tb_updated;


}


export function load_data_to_worldLayer(year, month, model, _map, _layer, json, countriesTemplate_json, data_national) {
    
    
    var m = String(month).padStart(2, '0');
    var year_month = year+m;
    var model_title = year+' '+_utils.toMonthName(m)+'<hr style="padding:1px;margin:0">'+model.replace(/_/g, " ")+'' ;
    
    //var query_national = _api.query_national(year, month);

    //console.log(JSON.stringify(json));

    colors = data_national.palette;
    breaks = data_national.breaks;
    
    for (var i = 0; i < json.features.length; i++) {
        
            var iso = json.features[i].properties.iso_a2;
            if (data_national.data[iso]){
                json.features[i].properties.su_dif = data_national.data[iso][year_month][model];
                //console.log("iso " + iso + " value "+ data_national.data[iso]["202206"]["ground_truth_internet_gg"]);
            }else{
                json.features[i].properties.su_dif = null;
            }

    }

   _utils.loadLagent(model_title, colors, breaks);
   
   load_data_to_controlTable_Bottom(data_national.data, year, month, countriesTemplate_json, model);

   _map.removeLayer(_layer);
   _layer.addTo(_map);
   
   _layer.addData(json);

}
