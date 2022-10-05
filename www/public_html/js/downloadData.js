export function isBeforeDate(date1, date2) {
  return date1 < date2;
}

export function json2csv(djson, countriesList) {

//    var models = [];
//    var dates = [];
//
//    // getting first country in the data
//    var fCountry = Object.keys(djson)[0];
//    var fCountries = Object.keys(djson);
//
//    // getting the list of models
//    for (var k in djson[fCountry][d_time]) {
//        models.push(k);
//    }
//
//    var csv = "iso," + models.join(',') + '\r\n';
//
//    for (var k = 0; k < fCountries.length; k++) {
//        var iso = fCountries[k];
//        csv = csv + iso;
//        for (var i = 0; i < models.length; i++) {
//
//            csv = csv + ' , ' + djson[iso][d_time][models[i]];
//
//        }
//        csv = csv + '\r\n';
//    }

    var models = [];
    var fCountries = Object.keys(djson.data)[0];
    var fYear = Object.keys(djson.data[fCountries])[0];

    for (var k in djson.data[fCountries][fYear]) {
        models.push(k);
    }
    var csv = "iso2code, country, Date, " + models.join(', ') + '\r\n';

    Object.keys(djson.data).forEach(iso => {
        //console.log(iso);
        for (var y in djson.data[iso]) {
            //console.log(y, " ");
            var country_name = countriesList.find(x => x["iso2code"] === iso)["country"];
            csv = csv + '' + iso + ', ' + country_name + ', ' + y;
            for (var i = 0; i < models.length; i++) {
                csv = csv + ', ' + djson.data[iso][y][models[i]];
            }
            csv = csv + '\r\n';
        }
    });

    return(csv);

}

// download scv file d=data t=date fname=file name
export function downloadCSV(d, DateStart, DateEnd, countriesList) {

    var scv2download = json2csv(d, countriesList);
    var fname_download = "Digital_Gender_Gaps_" + DateStart + "_"+DateEnd+".csv";

    var dataStr = "data:text/csv;charset=utf-8," + encodeURIComponent((scv2download));
    var dlAnchorElem = document.getElementById('downloadAnchorElem');
    dlAnchorElem.setAttribute("href", dataStr);
    dlAnchorElem.setAttribute("download", fname_download);
    dlAnchorElem.click();    

}

