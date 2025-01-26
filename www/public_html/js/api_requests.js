import * as _utils from './utils.js?version=0.11'

export function getWorld_geo_db(api_url) {

    var result = "";
    $.ajax({
        url: api_url+'national_geometries',
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

export function getWorldSubNational_geo_db(api_url) {

    var result = "";
    $.ajax({
        url: api_url+'subnational_geometries',
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

export function query_national_promis(y, month, indicators, GroundTruth, api_url) {

    //_utils.progressMenuOn();

    var m = String(month).padStart(2, '0');
    var ym = y + "-" + m;

    return new Promise((resolve, reject) => {

        if (GroundTruth) {
            $.ajax({
                url: api_url + "get_ground_truth_national",
                type: 'get',
                data: {
                },
                success: function (data) {
                    resolve(data);
                },
                error: function (error) {
                    reject(error);
                }
            });
        } else {
            $.ajax({
                url: api_url + "get_national_data",
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
        }



    });

}


export function query_sub_national_promis(y, month, indicators, GroundTruth, api_url) {

    //_utils.progressMenuOn();

    var m = String(month).padStart(2, '0');
    var ym = y + "-" + m;

    if (GroundTruth) {
        return new Promise((resolve, reject) => {
            $.ajax({
                url: api_url + "get_ground_truth_subnational",
                type: 'get',
                data: {},
                success: function (data) {
                    resolve(data);
                },
                error: function (error) {
                    reject(error);
                }
            });
        });
    } else {
        return new Promise((resolve, reject) => {
            $.ajax({
                url: api_url + "get_subnational_data",
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

}



export function query_national_data_with_dates(y1, month1, y2, month2, iso, GroundTruth, api_url) {

    //_utils.progressMenuOn();

    var m1 = String(month1).padStart(2, '0');
    var ym1 = y1 + "-" + m1;
    var m2 = String(month2).padStart(2, '0');
    var ym2 = y2 + "-" + m2;


    if (GroundTruth) {
        return new Promise((resolve, reject) => {
            $.ajax({
                url: api_url + "get_ground_truth_national",
                type: 'get',
                data: {},
                success: function (data) {
                    resolve(data);
                },
                error: function (error) {
                    reject(error);
                }
            });
        });
    } else {
        return new Promise((resolve, reject) => {
            $.ajax({
                url: api_url + "download_national_data_with_dates",
                type: 'get',
                data: {
                    start_date: ym1,
                    end_date: ym2,
                    country: iso
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
}

export function query_sub_national_data_with_dates(y1, month1, y2, month2, iso_gid_1, GroundTruth, api_url) {

    //_utils.progressMenuOn();

    var m1 = String(month1).padStart(2, '0');
    var ym1 = y1 + "-" + m1;
    var m2 = String(month2).padStart(2, '0');
    var ym2 = y2 + "-" + m2;


    if (GroundTruth) {
        
        return new Promise((resolve, reject) => {
            $.ajax({
                url: api_url + "get_ground_truth_subnational",
                type: 'get',
                data: {},
                success: function (data) {
                    resolve(data);
                },
                error: function (error) {
                    reject(error);
                }
            });
        });        

    } else {
        return new Promise((resolve, reject) => {
            $.ajax({
                url: api_url + "download_subnational_data_with_dates",
                type: 'get',
                data: {
                    start_date: ym1,
                    end_date: ym2,
                    region: iso_gid_1
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


}