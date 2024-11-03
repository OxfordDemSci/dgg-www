import * as _utils from './utils.js?version=0.75'

export function download_csv(api_url) {
            
    let param = _utils.getSelectedParametersDownload();    
    
    let start_date = param[0]+'-'+param[1];
    let end_date = param[2]+'-'+param[3];

    let uri = api_url + "/download_csv?level=" + param[4] + "&start_date=" + start_date + "&end_date=" + end_date;

    var to_date = new Date(end_date);
    var from_date = new Date(start_date);
    var delta = to_date - from_date;
    if(delta < 0){  
        console.log("End date should be more then start date");
        alert("End date should be more then start date");
        return;
    };

    let fname_downloaded = param[4] + "_" + start_date + "_" + end_date + ".csv";

    _utils.progressMenuOn();

    fetch(uri)
            .then(resp => resp.status === 200 ? resp.blob() : Promise.reject('something went wrong'))
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                // the filename you want
                a.download = fname_downloaded;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                $('#idMdDownload').modal('hide');
                _utils.progressMenuOff();
            })
            .catch(() => {
                _utils.progressMenuOff();
                alert('oh no!');
            });


}