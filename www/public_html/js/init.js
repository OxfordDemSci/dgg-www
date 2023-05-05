import * as _utils from './utils.js?version=6'

export function getDates(data) {
  
 
   var ymArray = [];
   
   for (var i = 0; i < data.length; i++) {
       
        ymArray.push(
                [
                    data[i].toString().substring(0, 4),
                    data[i].toString().substring(4, 6)
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

export function getDateSixMonthFromEnd(data) {

   let ym;
   if (data.length < 6){
       ym = data[0];
   }else{
       ym = data[data.length-6];
   }
   let ym_format = ym.toString().substring(0, 4)+ '-' + ym.toString().substring(4, 6); 
   return ym_format;
}

export function getCountriesList(countries) {
    return countries;
}


export function getCountries_teamplate() {

    var result = "";
    $.ajax({
        url: './data/countries.json?version=2',
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


export function load_countries_to_menu(countries) {

    var select_country = document.getElementById('select_country');
    var country_name;
    var country_alpha;
    
    for (var i = 0; i < countries.length; i++) {

        country_name = countries[i]["country"];
        country_alpha = countries[i]["iso2code"];
        
        select_country.innerHTML = select_country.innerHTML +
                    '<option value="' + country_alpha + '">' + country_name + '</option>';

    }
    
    // sort alphabetic    
    var sel = $('#select_country');
    var selected = sel.val(); // cache selected value, before reordering
    var opts_list = sel.find('option');
    opts_list.sort(function (a, b) {
        return $(a).text() > $(b).text() ? 1 : -1;
    });
    sel.html('').append(opts_list);
    sel.val(selected);

    // unselect any elements
    var elements = select_country.options;

    for (var i = 0; i < elements.length; i++) {
        elements[i].selected = false;
    }    


}

export function load_models_to_menu(models) {

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
   // modelsListArray = modelsListArray.sort((a, b) => a[0] - b[0]);

    //for (var i = modelsListArray.length - 1; i >= 0; i--) {
    for (var i = 0 ; i < modelsListArray.length ; i++) {    

        select_models.innerHTML = select_models.innerHTML +
                '<option value="' + modelsListArray[i][1] + '">' + modelsListArray[i][2] + '</option>';
    }
    
    // updated popover info for the indicatore in the menu
//    const popover = bootstrap.Popover.getOrCreateInstance('#lbIndicatorInfo', {"html":true});
//    popover.setContent({
//        '.popover-header': modelsListArray[modelsListArray.length - 1][2],
//        '.popover-body': modelsListArray[modelsListArray.length - 1][3]
//    });    


}


export function getWorld_geo() {

    var result = "";
    $.ajax({
        url: './data/world_med.geo.json?version=2',
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


export function loadDatesToMenu(firstMonth, firstYear, lastMonth, lastYear, monthsToDisable) {


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

    $('#datepicker').datepicker('setDate', lastYear + '-' + lastMonth);

}

//export function getLastSixMonthDate(firstMonth, firstYear, lastMonth, lastYear, monthsToDisable) {
//   // getting the date of last 6 month from lastMonth and lastYear
//   // cheecking if this date is not in monthsToDisable
//   // if it is in monthsToDisable then taken increament and looking for next month etc
//   
//    let icount=6;
//    let max_icount=18;
//    let lastYM;
//    let six_month_lastYM;
//    let six_month_lastYM_Date;
//   
//   do {
//        lastYM = new Date(lastYear+ '-' + lastMonth);
//        // getting last "icount" month from "lastYM"
//        six_month_lastYM = lastYM.setMonth(lastYM.getMonth() - icount);
//        six_month_lastYM_Date = moment(six_month_lastYM).format('YYYY-MM');
//        icount++;
//        
//        // avoiding infiniting loop if last 6 month in  monthsToDisable array 
//        // so the check will be don maximum max_icount times
//        // if did not pick last 6 month, the firstYear-firstMonth will be return
//        if (max_icount < icount) {
//            six_month_lastYM_Date=firstYear+ '-' + firstMonth;
//            break;
//        }        
//    }
//   while ($.inArray(six_month_lastYM_Date, monthsToDisable) > 0);
//    
//   return six_month_lastYM_Date;
//}


export function loadDatesToDownloadMenu(firstMonth, firstYear, lastMonth, lastYear, ymSixMonthFromEnd,  monthsToDisable) {
  
    //var LastSixMonthDate=getLastSixMonthDate(firstMonth, firstYear, lastMonth, lastYear, monthsToDisable).split("-");

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
            //alert(date);
            var formattedDate = moment(date).format('YYYY-MM');
            return $.inArray(formattedDate, monthsToDisable) < 0;
        }
    });

    $('#datepicker_start_date').datepicker('setDate', ymSixMonthFromEnd);
    
    
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
            //alert(date);
            var formattedDate = moment(date).format('YYYY-MM');
            return $.inArray(formattedDate, monthsToDisable) < 0;
        }
    });

    $('#datepicker_end_date').datepicker('setDate', lastYear + '-' + lastMonth);    

}
