import * as _ImageFromRGB from './createImageFromRGBdata.js?version=1'

const zeroPad = (num, places) => String(num).padStart(places, '0')

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

export function loadLagent(title, colors, breaks) {

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

