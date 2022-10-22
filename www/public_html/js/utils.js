import * as _ImageFromRGB from './createImageFromRGBdata.js?version=1'

const zeroPad = (num, places) => String(num).padStart(places, '0');

// m - selected model, d- modeil list
export function updateModelInfoonPanel(m, d) {

    var titleModelName = document.getElementById('titleModelName');
    //titleModelName.innerHTML = d[m].name;

    var titleModelDescription = document.getElementById('titleModelDescription');
    //titleModelDescription.innerHTML = d[m].description;

    // updated popover info for the indicatore in the menu
//    const popover = bootstrap.Popover.getOrCreateInstance('#lbIndicatorInfo', {"html": true});
//    popover.setContent({
//        '.popover-header': d[m].name,
//        '.popover-body': d[m].description
//    });
    
//  var titleModelName = document.getElementById('titleModelName');
//  titleModelName.innerHTML = d[m].name;

  var titleModelDescription = document.getElementById('titleModelDescription');
  titleModelDescription.innerHTML = d[m].description;
    


}

export function hilightRowTable(iso2code, countriesList, scroll=true) {

    var country_name;
    var country_alpha;
    var country_name_selected;
    for (var i = 0; i < countriesList.length; i++) {

        country_name = countriesList[i]["country"];
        country_alpha = countriesList[i]["iso2code"];

        if (country_alpha === iso2code) {
            country_name_selected = country_name;
        }

    }
    
    var container_scrollHead = document.getElementsByClassName('dataTables_scrollHead')[0];
    var container_filter = document.getElementsByClassName('dataTables_filter')[0];   
    
    var offsetRight =  $('#table_bottom').outerHeight() -  container_scrollHead.offsetHeight -  container_filter.offsetHeight -  $('#iconTableMaximize').outerHeight() - 30;


//    $("#tblBottom").dataTable().fnDestroy();

    var scrollPos = $(".dataTables_scrollBody").scrollTop();
    
    var table = $('#tblBottom').DataTable({
        "fnRowCallback": function (nRow, aData, iDisplayIndex) {

            if (aData[0] === iso2code) {
                $(nRow).css('background-color', '#D7D4D4');
            } else {
                $(nRow).css('background-color', '');
            }
        },
                paging: true,
                bInfo: false,
                scrollY: offsetRight,
                bDestroy: true,
                deferRender:    true,
                scroller:       true,  
                sScrollX: true,
                columnDefs: [
                {
                    target: 0,
                    visible: false,
                    searchable: true
                }
                ]
    });



    if (scroll){
        table.rows().data().map((row, index) => {
            if (row[0] === iso2code) {
                table.scroller().scrollToRow(index-1);
            }
        });
    }else{
        $(".dataTables_scrollBody").scrollTop(scrollPos);
    }


}




export function getSelectedParameters() {

    var year = $("#datepicker").data('datepicker').getFormattedDate('yyyy');
    var month = $("#datepicker").data('datepicker').getFormattedDate('mm');
    var model = document.getElementById("select_models").value;

    return([year, month, model]);
}


export function removeOptions(selectElement) {
    var i, L = selectElement.options.length - 1;
    for (i = L; i >= 0; i--) {
        selectElement.remove(i);
    }
}


export function isEmpty(value) {
    return (value == null || value.length === 0);
}

export function onlyUnique(value, index, self) {
    return self.indexOf(value) === index;
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
    document.getElementById("progressMenuTable").style.display = 'contents';
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

export function toMonthName(monthNumber) {
    const date = new Date();
    date.setMonth(monthNumber - 1);

    return date.toLocaleString('en-US', {
        month: 'long'
    });
}

function hexToRGB(hexStr) {
    var col = {};
    col.r = parseInt(hexStr.substr(1, 2), 16);
    col.g = parseInt(hexStr.substr(3, 2), 16);
    col.b = parseInt(hexStr.substr(5, 2), 16);
    return col;
}

export function loadLagent_deprecated(title, colors, breaks) {

    var html = '<div style="width:100px">' + title + '</div>';
    
    html += '<ul style="list-style-type: none;margin-top: 10px;padding-inline-start: 10px;">';
    for (var i = 0, len = colors.length; i < len; i++) {
        var rgb = hexToRGB(colors[i]);
        var mCanvas = _ImageFromRGB.createImageFromRGBdata(rgb.r, rgb.g, rgb.b, 20, 20);

        html += '<li><img width="20px" height="20px" src="' + mCanvas.toDataURL() + '"><span>&#32;&#32;&#32;&#32;	&nbsp;&nbsp;' + breaks[i] + '</span></li>';
    }
    html += '</ul>';
    document.getElementById('legend_data_info').innerHTML = html;

}


export function loadLagent2(title, colors, breaks, subtitles) {

    var html = '<div style="width:120px">' + title + '</div>';
    var subtitlesArray = Array(colors.length).fill('');
    subtitlesArray[0] = subtitles[0];
    subtitlesArray[colors.length-1] = subtitles[1];

    html += '<ul style="list-style-type: none;margin-top: 10px;padding-inline-start: 10px;">';
    for (var i = 0, len = colors.length; i < len; i++) {
        var rgb = hexToRGB(colors[i]);
        var mCanvas = _ImageFromRGB.createImageFromRGBdata(rgb.r, rgb.g, rgb.b, 20, 20);

        html += '<li><img width="20px" height="20px" src="' + mCanvas.toDataURL() + '"><span>&#32;&#32;&#32;&#32;	&nbsp;&nbsp;' + subtitlesArray[i] + '</span></li>';
    }
    html += '</ul>';
    document.getElementById('legend_data_info').innerHTML = html;

}


export function loadLagent(title, colors, breaks, subtitles) {

    var html = '<div style="width:100px">' + title + '</div>';
    
    var subtitlesArray = Array(colors.length).fill('');
    subtitlesArray[0] = subtitles[0];
    subtitlesArray[colors.length-1] = subtitles[1];    
    
    html += '<div style="width:100px"><b>' + subtitles[0] + '</b></div>';
    
    html += '<ul style="list-style-type: none;margin-top: 2px;margin-bottom: 2px;padding-inline-start: 10px;">';
    for (var i = 0, len = colors.length; i < len; i++) {
        var rgb = hexToRGB(colors[i]);
        var mCanvas = _ImageFromRGB.createImageFromRGBdata(rgb.r, rgb.g, rgb.b, 20, 20);

        html += '<li><img width="20px" height="20px" src="' + mCanvas.toDataURL() + '"><span>&#32;&#32;&#32;&#32;	&nbsp;&nbsp;' + breaks[i] + '</span></li>';
    }
    html += '</ul>';
    html += '<div style="width:100px"><b>' + subtitles[1] + '</b></div>';
    document.getElementById('legend_data_info').innerHTML = html;

}
