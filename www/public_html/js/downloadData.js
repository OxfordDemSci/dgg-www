export function isBeforeDate(date1, date2) {
  return date1 < date2;
}

export function json2csv(djson, countriesList, modelsList) {

    var models = [];
    var fCountries = Object.keys(djson.data)[0];
    var fYear = Object.keys(djson.data[fCountries])[0];


    for (var k in djson.data[fCountries][fYear]) {
        //models.push(modelsList[k].name);
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
export function downloadCSV(d, DateStart, DateEnd, countriesList, modelsList) {

    var scv2download = json2csv(d, countriesList, modelsList);
    var fname_download = "Digital_Gender_Gaps_" + DateStart + "_"+DateEnd+".csv";

    var dataStr = "data:text/csv;charset=utf-8," + encodeURIComponent((scv2download));
    var dlAnchorElem = document.getElementById('downloadAnchorElem');
    dlAnchorElem.setAttribute("href", dataStr);
    dlAnchorElem.setAttribute("download", fname_download);
    dlAnchorElem.click();    

}

