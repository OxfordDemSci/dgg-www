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

function round_value(value, precision) {
    var multiplier = Math.pow(10, precision || 0);
    return Math.round(value * multiplier) / multiplier;
}

export function percentage(percent, total) {
    return ((percent/ 100) * total);
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
        Object.keys(d).forEach(function (key) {
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
        let pointRadius=Math.round(Number(document.getElementById("chPointRadius").value));
        if ($("#chPointPlot").is(":checked")) {
              pointRadius=document.getElementById("chPointRadius").value;
        } else {
              pointRadius=0;
        }
        
        let lineBorderWidth=Math.round(Number(document.getElementById("chLineStrokeWidth").value));
        let lineShowLine=true; 
        if (lineBorderWidth === 0) {
              lineShowLine=false;
        }       
        
    
var min = (Math.min(...dataArray)),
    max = (Math.max(...dataArray));
    
    let min_f = percentage(15, min);
    let max_f = percentage(15, max);
    

    min=round_value(min-min_f,2); 
    max=round_value(max+max_f,2);
    
    if (max > 1) {
        max = 1;
    }

    const skipped = (ctx, value) => ctx.p0.skip || ctx.p1.skip ? value : undefined;

    const data = {
        labels: labels,
        datasets: [{
                label: '',
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: dataArray,
                pointStyle: 'circle',
                pointRadius: pointRadius,
                pointHoverRadius: Math.round(pointRadius*2),
                segment: {
                    borderColor: ctx => skipped(ctx, 'rgb(255, 99, 132)')
                    //borderDash: ctx => skipped(ctx, [4, 4]),
                  },
                spanGaps: true,
                borderWidth: lineBorderWidth,
                showLine: lineShowLine, // show line in scatter plot
                fill: false // only show line                    
            }]
    };


    const options = {
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'year',
                    displayFormats: {
                            year: 'yyyy-01'
                        }                    
                },
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

