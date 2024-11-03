import * as _utils from './utils.js?version=0.2'

export function restyleLayer(propertyName, _layer) {

    _layer.eachLayer(function (featureInstanceLayer) {
        var propertyValue = featureInstanceLayer.feature.properties[propertyName];

        if (typeof propertyValue !== 'undefined' && propertyValue !== null) {
            featureInstanceLayer.setStyle({
                color: '#888c8d',
                fillOpacity: 0,
                weight: 1
            });
        }

    });
}


export function resetHighlight(e, _layer) {
    //_layer.resetStyle(e.target);
    restyleLayer("dvalue", _layer);
    
}

export function highlightFeature(e) {
    

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



export function load_data_to_worldBoundariesLayer(_map, _layer, json, data_national) {
    
    _layer.clearLayers();
   _map.removeLayer(_layer);
   
    json.dvalue = null;
	
    for (var i = 0; i < json.features.length; i++) {
			
            var iso = json.features[i].properties.GID_0;
            var data_filter = data_national.filter(element => element.iso3code === iso);
            
            if (data_filter.length > 0){
                //json.features[i].properties.dvalue = data_national[iso];
            }else{
                json.features[i].properties.dvalue = null;
            }
    }    
    

   _layer.addTo(_map);
   _layer.addData(json);
   
   _utils.removeSelectedLayer(_map, "dvalue");

   restyleLayer("dvalue", _layer);

}