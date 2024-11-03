import * as _ImageFromRGB from './createImageFromRGBdata.js?version=1'

const zeroPad = (num, places) => String(num).padStart(places, '0');

export function roundToTwo(num) {
    return +(Math.round(num + "e+2")  + "e-2");
}

export function progressMenuOn() {
    document.getElementById("progressMenu").style.visibility = 'visible';
    document.getElementById("progressMenu").style.display = 'block';
}

export function progressMenuOff() {

    setTimeout(function () {
        document.getElementById("progressMenu").style.visibility = 'hidden';
        document.getElementById("progressMenu").style.display = 'none';
    }, 100);//wait 1 seconds

}


export function progressMenuTableOn() {
    document.getElementById("progressMenuTable").style.visibility = 'visible';
    document.getElementById("progressMenuTable").style.display = 'block';
    return;
}

export function progressMenuTableOff() {

    setTimeout(function () {
        document.getElementById("progressMenuTable").style.visibility = 'hidden';
        document.getElementById("progressMenuTable").style.display = 'none';
    }, 1000);//wait 1 seconds

}


export function hideCoverScreen() {

    var coverScreen = document.getElementById('coverScreen');
    coverScreen.style.visibility = 'hidden';

    var sidebar = document.getElementById('sidebar');
    sidebar.style.visibility = 'visible';
}

export function showCoverScreen() {

    var coverScreen = document.getElementById('coverScreen');
    coverScreen.style.visibility = 'visible';
}


export function isEmpty(value) {
    return (value === null || value.length === 0);
}

export function onlyUnique(value, index, self) {
    return self.indexOf(value) === index;
}


// select last year and month
export function getLastDates(ymArray) {

    var yrs = [];
    for (var k in ymArray)
        yrs.push(k);

    var years = yrs.sort(function (a, b) {
        if (a < b)
            return 1;
        if (a > b)
            return -1;
    });

    var yr = years[0];

    var monthArray = ymArray[yr];
    var mn = monthArray.slice(-1)[0];

    return([yr, mn]);
}

export function getFirstDates(ymArray) {

    var yrs = [];
    for (var k in ymArray)
        yrs.push(k);

    var years = yrs.sort(function (a, b) {
        if (a < b)
            return 1;
        if (a > b)
            return -1;
    });

    var yr = years.slice(-1)[0];

    var monthArray = ymArray[yr];
    var mn = monthArray[0];

    return([yr, mn]);
}


export function MonthsYearsToDisable(ymArray, fyear, lyear) {

    var ymrToDisable = [];
    for (let i = fyear; i <= lyear; i++) {

        var mArray = ymArray[i];

        for (let k = 1; k <= 12; k++) {
            if (!mArray.includes(k)) {
                ymrToDisable.push(i + '-' + zeroPad(k, 2));
            }
        }

    }
    return(ymrToDisable);
}

export function getSelectedParameters() {

    var year = $("#datepicker").data('datepicker').getFormattedDate('yyyy');
    var month = $("#datepicker").data('datepicker').getFormattedDate('mm');
    //var model = document.getElementById("select_models").value;
    var model = $('#select_models').find(":selected").val();

    return([year, month, model]);
}

export function getSelectedParametersDownload() {

    var year_start = $("#datepicker_start_date").data('datepicker').getFormattedDate('yyyy');
    var month_start = $("#datepicker_start_date").data('datepicker').getFormattedDate('mm');
    var year_end = $("#datepicker_end_date").data('datepicker').getFormattedDate('yyyy');
    var month_end = $("#datepicker_end_date").data('datepicker').getFormattedDate('mm');
    var select_level = $('#select_level_download').find(":selected").val();

    return([year_start, month_start, year_end, month_end, select_level]);
}


export function removeSelectedLayer(_map, fname) {

    if (_map) {
        _map.eachLayer(function (layer) {
            if (layer.feature) {
                let n = layer.feature.properties[fname];
                if (typeof n === 'undefined' || n === null) {
                    _map.removeLayer(layer);
                }
            }
        });
    }
}


export function updateModelInfoonPanel(m, d, g) {

//  var titleModelName = document.getElementById('titleModelName');
//  var titleModelDescription = document.getElementById('titleModelDescription');
//
//  var titleModelDescription = document.getElementById('titleModelDescription');
//  titleModelDescription.innerHTML = d[m].description;

    var titleModelDescription = document.getElementById('titleModelDescription');

    if (g) {
        let txt = "<p class='pt-2'><strong>Description:</strong>&nbsp;"+ d["ground_truth"][m].description +".</br><strong>Data Frequency:</strong> "+ d["ground_truth"]["data_frequency"] + "</br><strong>Geographical Coverage:</strong> " + d["ground_truth"]["geographical_coverage"] +"</p>" ;
        titleModelDescription.innerHTML = txt;
    } else {
        let txt = "<p class='pt-2'><strong>Description:</strong>&nbsp;"+ d["indicator"][m].description +".</br><strong>Data Frequency:</strong> "+ d["indicator"]["data_frequency"] + "</br><strong>Geographical Coverage:</strong> " + d["indicator"]["geographical_coverage"] +"</p>" ;
        titleModelDescription.innerHTML = txt;
    }

}


export function hideRefreshButton() {

    var coverScreen = document.getElementById('refreshButton');
    coverScreen.style.visibility = 'hidden';

}

export function showRefreshButton() {

    var coverScreen = document.getElementById('refreshButton');
    coverScreen.style.visibility = 'visible';

}


export function isContains(json, value) {
    let contains = false;
    Object.keys(json).some(key => {
        contains = typeof json[key] === 'object' ? isContains(json[key], value) : json[key] === value;
         return contains;
    });
    return contains;
}


export function getContriesList(json, value) {
    
    let countriesList;
    
    if (value){
        countriesList = json.national_ground_truth;
    }else{
        countriesList = json.national.countries;
    } 
    
    return countriesList;
}


export function getContriesListSubnational(json, value) {
    
    let countriesListSubnational;
    
    if (value){
        countriesListSubnational = json.subnational_ground_truth;
    }else{
        countriesListSubnational = json.subnational.regions;
    } 
    
    return countriesListSubnational;
}

export function uniqueArray(arr) {
    var a = [];
    for (var i=0, l=arr.length; i<l; i++)
        if (a.indexOf(arr[i]) === -1 && arr[i] !== '')
            a.push(arr[i]);
    return a;
}


function hexToRGB(hexStr) {
    var col = {};
    col.r = parseInt(hexStr.substr(1, 2), 16);
    col.g = parseInt(hexStr.substr(3, 2), 16);
    col.b = parseInt(hexStr.substr(5, 2), 16);
    return col;
}

export function loadLagent(title, colors, breaks, subtitles) {
    
    var _PredictedError = document.getElementById('chPredictedError');
    let subtitles_='';
    if(_PredictedError.checked) {
        subtitles_="Predicted error";
    }


    //breaks=breaks.sort(function(a, b){return b - a});
    var html = '<div style="width:130px">' + title + '</div>';
    
    var subtitlesArray = Array(colors.length).fill('');
    subtitlesArray[0] = subtitles[0];
    subtitlesArray[colors.length-1] = subtitles[1];    
    
    html += '<div style="width:100px">' + subtitles_ + '</div>';
    
    html += '<ul style="list-style-type: none;margin-top: 2px;margin-bottom: 2px;padding-inline-start: 10px;">';
    //for (var i = 0, len = colors.length; i < len; i++) {
    let len = colors.length;
    for (var i = len -1;  i >= 0; i--) {        
        var rgb = hexToRGB(colors[i]);
        var mCanvas = _ImageFromRGB.createImageFromRGBdata(rgb.r, rgb.g, rgb.b, 20, 20);

        html += '<li><img width="20px" height="20px" src="' + mCanvas.toDataURL() + '"><span>&#32;&#32;&#32;&#32;	&nbsp;&nbsp;' + breaks[i] + '</span></li>';
    }
    html += '</ul>';
    //html += '<div style="width:100px">' + subtitles_ + '</div>';
    document.getElementById('legend_data_info').innerHTML = html;

}
