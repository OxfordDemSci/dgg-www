export function getSettings(api_url) {

    var result = "";
    $.ajax({
        url: api_url+'/init',
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

export function query_national(y, month) {
    
    var m = String(month).padStart(2, '0');
    var ym = y+m;
    
    if (window.mdebug === true)
            console.log("Sending request to API to get the data for "+ ym);
        
    var result = "";
    $.ajax({
        url: './data/query_national_test.json?version=4'+Date.now() + '' + Math.random(),
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
