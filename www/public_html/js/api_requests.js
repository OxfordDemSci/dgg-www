import * as _utils from './utils.js?version=10'

export function getSettings(api_url) {

    var result = "";
    $.ajax({
        url: api_url+'init',
        async: false,
        type: 'get',
        dataType: 'json',
        success: function (data) {
            result = data;
        },
        error: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr.status);
            console.log(thrownError);
        }
    });
    return result;
}

export function query_national(y, month, api_url) {
    
    //_utils.progressMenuOn();
    
    var m = String(month).padStart(2, '0');
    var ym = y+m;
    
    if (window.mdebug === true)
            console.log("Sending request to API to get the data for "+ ym);
        
    var result = "";
    $.ajax({
        url: api_url+'query_national?date=['+ym+']',
        async: false,
        type: 'get',
        dataType: 'json',
        success: function (data) {
			//console.log(data);
			
            //result = JSON.parse(data.data);
            result = data.data;
        },
        error: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr.status);
            console.log(thrownError);
        },
        complete: function() {
           //_utils.progressMenuOff();
        }        
    });
    return result;
}


export function query_national_promis(y, month, api_url) {

    //_utils.progressMenuOn();

    var m = String(month).padStart(2, '0');
    var ym = y + m;

    return new Promise((resolve, reject) => {
        $.ajax({
            url: api_url+"query_national",
            type: 'get',
            data: {
                date: ym
            },
            success: function (data) {
                resolve(data);
            },
            error: function (error) {
                reject(error);
            }
        });
    });
}


export function query_model_promis(iso2code, model, API_URL) {

    return new Promise((resolve, reject) => {
        $.ajax({
            url: API_URL + "query_specific_country",
            type: 'get',
            data: {
                iso2code: iso2code,
                model: model
            },
            success: function (data) {
                resolve(data);
            },
            error: function (error) {
                reject(error);
            }
        });
    });
}


export function download_data_with_dates(sd, ed, API_URL) {

    return new Promise((resolve, reject) => {
        $.ajax({
            url: API_URL + "download_data_with_dates",
            type: 'get',
            data: {
                start_date: sd,
                end_date: ed
            },
            success: function (data) {
                resolve(data);
            },
            error: function (error) {
                reject(error);
            }
        });
    });
}