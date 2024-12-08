export function display(s) {
  var x = document.getElementById("plotxy_div_id");
  
  if (s === "show"){
        x.style.display = "block";
        //$('#plotxy_div_id').show();
  } else if (s === "hide") {
        x.style.display = "none";
        //$('#plotxy_div_id').hide();
  }else{
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }      
  }
}

const zeroPad = (num, places) => String(num).padStart(places, '0');

export function updateData(c, d,  model, modelsList, _prSubNational) {
    
    var _PredictedError = document.getElementById('chPredictedError');
    let PredictedType="predicted";
    
    if(_PredictedError.checked) {
        PredictedType="predicted_error";
    }  

//    var country_name;
//    var country_alpha;
//
//    for (var i = 0; i < countriesList.length; i++) {
//
//        country_name = countriesList[i]["country"];
//        country_alpha = countriesList[i]["iso2code"];
//
//        if (country_alpha === iso2code) {
//            document.getElementById('plotxy_title').innerText = country_name;
//        }
//
//    }

 
    var labels = [];
    var dataArray = [];
    var ym;

    if (_prSubNational) {
        Object.keys(d).forEach(function (key) {
            ym = key.toString();
            labels.push(ym);
            dataArray.push(d[key][model][PredictedType]);
        });
    } else {
        Object.keys(d).reverse().forEach(function (key) {
            ym = key.toString();
            labels.push(ym);
            dataArray.push(d[key][model][PredictedType]);
        });
    }
    
//    for (var k in d) {
//        console.log(k);
//        ym = k.toString();
//        labels.push(ym);
//        dataArray.push(d[k][model][PredictedType]);
//    }
    
var min = (Math.min(...dataArray)),
    max = (Math.max(...dataArray));    

    const data = {
        labels: labels,
        datasets: [{
                label: '',
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: dataArray
            }]
    };


    const options = {
        scales: {
            x: {
                ticks: {
                    maxRotation: 60,
                    minRotation: 60
                }
            },
            y: {
                suggestedMin: min,
                suggestedMax: max
            }
        },
        plugins: {
            legend: {
                display: false,
                text: model
            }, 
            title: {
                display: true,
                text: modelsList["indicator"][model].name,
                position: "left",
                font: {
                    weight: 600
                },
                padding: {
                    bottom: 10,
                    left: 100
                }
            }
        }
    };

    c.options = options;
    c.data = data;
    c.update();

}

