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

export function updateData(c, d, iso2code, model, modelsList, countriesList) {

    var country_name;
    var country_alpha;

    for (var i = 0; i < countriesList.length; i++) {

        country_name = countriesList[i]["country"];
        country_alpha = countriesList[i]["iso2code"];

        if (country_alpha === iso2code) {
            document.getElementById('plotxy_title').innerText = country_name;
        }

    }

    var labels = [];
    var dataArray = [];
    var ym;
    for (var k in d.data[iso2code]) {
        ym = k.toString().substring(0, 4) + '-' + zeroPad(k.toString().substring(5, 6), 2);
        labels.push(ym);
        dataArray.push(d.data[iso2code][k][model]);
    }

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
                suggestedMin: 0.8,
                suggestedMax: 1.0
            }
        },
        plugins: {
            legend: {
                display: false,
                text: model
            }, 
            title: {
                display: true,
                text: modelsList[model].name,
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