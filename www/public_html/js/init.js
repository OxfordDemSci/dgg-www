import * as _utils from './utils.js?version=6'

export function getDates(data) {
  
 
   var ymArray = [];
   
   for (var i = 0; i < data.length; i++) {
       
        let split_date = data[i].split("-");
        ymArray.push(
                [
                    split_date[0],
                    split_date[1]
                ]
                );

    }
                 

    // select all years from matrix
    var col0 = ymArray.map(d => d[0]);
    // keeping only unique
    var years = col0.filter(_utils.onlyUnique);

    var ymObject = {};

    for (var ii = 0; ii < years.length; ii ++) {
        
        let yr = years[ii];
        var monthArray = [];
        for (let i = 0; i < ymArray.length; i++) {
            for (let j = 0; j < ymArray[i].length; j++) {
                if (ymArray[i][j] === yr){
                    monthArray.push(  parseInt(ymArray[i][1])  );
                }    
            }
        }
        // keeping only unique and sorted month for a particuler year
        ymObject[yr] = monthArray.filter(_utils.onlyUnique).sort((a, b) => a - b);
    }

    // access to the months of hte year  ymObject[2020]   
    return ymObject;
}


export function loadDatesToMenu(firstMonth, firstYear, lastMonth, lastYear, monthsToDisable, initialTime) {

    $("#datepicker").datepicker("destroy"); 
    
    $("#datepicker").datepicker({
        format: "yyyy-mm",
        minViewMode: "months",
        startDate:  firstYear+ '-' + firstMonth,
        endDate: lastYear+ '-' + lastMonth,
        useCurrent: false,
        autoclose: true,
        fontAwesome: true,
        orientation: "bottom",
        beforeShowMonth: function (date) {
            var formattedDate = moment(date).format('YYYY-MM');
            return $.inArray(formattedDate, monthsToDisable) < 0;
        }
    });
    $('#datepicker').datepicker("refresh");
    
    if (initialTime){
        $('#datepicker').datepicker('setDate', lastYear + '-' + lastMonth);
    }
    //
    
    
    
     $("#datepicker_start_date").datepicker("destroy"); 
     
     $("#datepicker_start_date").datepicker({
        format: "yyyy-mm",
        minViewMode: "months",
        startDate:  firstYear+ '-' + firstMonth,
        endDate: lastYear+ '-' + lastMonth,
        useCurrent: false,
        autoclose: true,
        fontAwesome: true,
        orientation: "bottom",
        beforeShowMonth: function (date) {
            var formattedDate = moment(date).format('YYYY-MM');
            return $.inArray(formattedDate, monthsToDisable) < 0;
        }
    });
    $('#datepicker_start_date').datepicker("refresh");
    $('#datepicker_start_date').datepicker('setDate', firstYear + '-' + firstMonth);   
    
    
    $("#datepicker_end_date").datepicker("destroy"); 
    
     $("#datepicker_end_date").datepicker({
        format: "yyyy-mm",
        minViewMode: "months",
        startDate:  firstYear+ '-' + firstMonth,
        endDate: lastYear+ '-' + lastMonth,
        useCurrent: false,
        autoclose: true,
        fontAwesome: true,
        orientation: "bottom",
        beforeShowMonth: function (date) {
            var formattedDate = moment(date).format('YYYY-MM');
            return $.inArray(formattedDate, monthsToDisable) < 0;
        }
    });
    $('#datepicker_end_date').datepicker("refresh");
    $('#datepicker_end_date').datepicker('setDate', lastYear + '-' + lastMonth);    
}

export function load_models_to_menu(models, d) {

    var select_models = document.getElementById('select_models');
    var modelsListArray = [];

    for (var m in models) {

        modelsListArray.push(
                [
                    models[m].order,
                    m,
                    models[m].name,
                    models[m].description,
                    models[m].type
                ]
                );
    }

    for (var i = 0 ; i < modelsListArray.length ; i++) {    
        let mn = modelsListArray[i][1];
        select_models.innerHTML = select_models.innerHTML +
                '<option value="' + mn + '">' + d["indicator"][mn].name + '</option>';
    }


}


export function getWorld_geo() {

    var result = "";
    $.ajax({
        url: './data/simplified_l0_v2.geojson?version=2',
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


export function getWorldSubNational_geo() {

    var result = "";
    $.ajax({
        url: './data/simplified_l1_v2_1_13.geojson?version=2',
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


export function getCountriesList(countries) {
    return countries;
}