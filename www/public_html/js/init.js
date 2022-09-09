export function getInitSettings() {

    var result = "";
    $.ajax({
        url: 'http://127.0.0.1:5000/init',
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

export function getDates(data) {
    
   var ymArray = [];
     
   for (var i = 0; i < data.length; i++) {
       
        ymArray.push(
                [
                    data[i].toString().substring(0, 4),
                    data[i].toString().substring(5, 6)
                ]
                );

    }

    return ymArray;
}
