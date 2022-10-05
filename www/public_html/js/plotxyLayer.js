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

export function updateData(c, d, iso2code, model) {
    

    document.getElementById('plotxy_title').innerText = model.replace(/_/g, " ") ;
    
    var labels = [];
    var dataArray = [];
    
    for (var k in d.data[iso2code]) {
        labels.push(k);
        dataArray.push(d.data[iso2code][k][model]);
    }
    
//    const labels = [
//    '2000-01',
//    '2000-02',
//    '2000-03',
//    '2000-04',
//    '2000-05',
//    '2000-06',
//    '2000-07',
//    '2000-11',
//    '2001-01',
//    '2002-01',
//    '2003-01',
//    '2004-01'
//  ];
//
  const data = {
    labels: labels,
    datasets: [{
      label: '',
      backgroundColor: 'rgb(255, 99, 132)',
      borderColor: 'rgb(255, 99, 132)',
      data: dataArray
    }]
  };
//    
  c.data = data;
  c.update();

}
