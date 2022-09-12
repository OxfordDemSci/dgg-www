function onlyUnique(value, index, self) {
        return self.indexOf(value) === index;
}


export function load_countries_to_menu(countries) {

    $.getJSON("./data/countries.json?version=2", function () {
        if (window.mdebug === true)
            console.log("success loading geojson");
    })
            .done(function (data) {
                
                var select_country = document.getElementById('select_country');

                var country_name;
                var country_alpha;
                for (var i = 0; i < countries.length; i++) {
                        
                        country_alpha = countries[i];
                        
                        if ((country_alpha !== undefined) && (country_alpha !== null) && (country_alpha !== "")){ 
                             country_name = data.find(x => x["alpha-2"] === country_alpha)["name"];
                             
                            select_country.innerHTML = select_country.innerHTML +
                                  '<option value="' + country_alpha + '">' + country_name + '</option>';                               
                        }
                }  
   
                // sort alphabetic    
                var sel = $('#select_country');
                var selected = sel.val(); // cache selected value, before reordering
                var opts_list = sel.find('option');
                opts_list.sort(function(a, b) { return $(a).text() > $(b).text() ? 1 : -1; });
                sel.html('').append(opts_list);
                sel.val(selected);     
              
                // unselect any elements
                var elements = select_country.options;

                for(var i = 0; i < elements.length; i++){
                    elements[i].selected = false;
                }
                
         
                
            })
            .fail(function (e) {
                if (window.mdebug === true)
                    console.log(e);
            })
            .always(function () {
                if (window.mdebug === true)
                    console.log("complete loading geojson of countires");
            });


}

export function load_month_to_menu(ymArray, yr) {

    var monthArray = [];

    for (let i = 0; i < ymArray.length; i++) {
        var innerArrayLength = ymArray[i].length;
        for (let j = 0; j < ymArray[i].length; j++) {
            if (ymArray[i][j] === yr){
                monthArray.push( [ ymArray[i][1] ] );
            }    
        }
    }
    
    var monthArrayUnique = monthArray.filter(onlyUnique);
    var select_month = document.getElementById('select_month');
    
    const monthArrayUnique_sorted = monthArrayUnique.sort();
    
    for (let i = 0; i < monthArrayUnique_sorted.length; i++) {
                
         select_month.innerHTML = select_month.innerHTML +
                '<option value="' + monthArrayUnique_sorted[i] + '">' + monthArrayUnique_sorted[i] + '</option>';
    }
    
    

}


export function load_year_to_menu(ymArray) {
    
    // select all years from matrix
    var col0 = ymArray.map(d => d[0]);
    // keeping only unique
    var years = col0.filter(onlyUnique);

    const years_sorted=years.sort(function(a,b){
        if (a<b) return 1;
        if (a>b) return -1;
    });

    
    var select_year = document.getElementById('select_year');
    
    for (let i = 0; i < years_sorted.length; i++) {
        
         select_year.innerHTML = select_year.innerHTML +
                '<option value="' + years_sorted[i] + '">' + years_sorted[i] + '</option>';
    } 
    
    load_month_to_menu(ymArray, years_sorted[0]);

}


export function load_models_to_menu(models) {


    var select_models = document.getElementById('select_models');
    
    var model_name;
    for (let i = 0; i < models.length; i++) {
        
         model_name = models[i].replace(/_/g, " ");
         select_models.innerHTML = select_models.innerHTML +
                '<option value="' + models[i] + '">' + model_name + '</option>';
    } 

}


export function load_data_to_tb() {

    $.getJSON("./data/countries.json", function () {
        if (window.debug === true)
            console.log("success loading geojson");
    })
            .done(function (data) {
                
                var select_iso = document.getElementById('tb_container');
                var tb_updated;
tb_updated = `<div class="">
<table class="table" >
  <thead>
    <tr>
      <th scope="col"></th>
      <th scope="col">Country</th>
      <th scope="col">Ground truth internet gg</th>
      <th scope="col">Internet online model prediction</th>
      <th scope="col">Internet online offline model prediction</th>
      <th scope="col">Internet offline model prediction</th>
      <th scope="col">Ground truth mobile gg</th>
      <th scope="col">Mobile online model prediction</th>
      <th scope="col">Mobile online offline modelprediction</th>
      <th scope="col">Mobile offline model prediction</th>
    </tr>
  </thead>
  <tbody>`;


                for (var i = 0; i < data.length; i++) {
                   tb_updated = tb_updated + `
                            <tr>
                                <td class="fib" style="background-image: url(../img/flags/4x3/`+data[i]["alpha-2"]+`.svg);background-size: 75% 75%;"></td>
                                <td>`+data[i]["name"]+`</td>
                                <td>1</td>
                                <td>1</td>
                    <td>1</td>
                    <td>1</td>
                    <td>1</td>
                    <td>1</td>
                    <td>1</td>
                    <td>1</td>
                            </tr>`;
                    
                }   
                
tb_updated = tb_updated + `</tbody></table>`; 

select_iso.innerHTML = tb_updated;                
            })
            .fail(function (e) {
                if (window.mdebug === true)
                    console.log(e);
            })
            .always(function () {
                if (window.mdebug === true)
                    console.log("complete loading geojson of countires");
            });


}