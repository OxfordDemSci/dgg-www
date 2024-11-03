export function updateInfoBox(model, vl, iso, year, source ) {

  document.getElementById('infoBox_title_model').innerHTML = model + ':&nbsp;' + vl;
  document.getElementById('infoBox_title_iso').innerHTML = iso;
  document.getElementById('infoBox_title_survey_year').innerHTML = 'Survey year:&nbsp; '+ year;
  document.getElementById('infoBox_title_source').innerHTML = 'Source :&nbsp;' + source;
  
}

export function display(s) {
  var x = document.getElementById("infoBox_div_id");
  
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