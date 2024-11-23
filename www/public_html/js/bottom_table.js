import * as _utils from './utils.js?version=0.22'
import * as _init from './init.js?version=0.3'

function sort_subnational_child_rows(iso, data, _GroundTruth, modelsList, countriesListSubnational) {
    
    
    var _PredictedError = document.getElementById('chPredictedError');
    let PredictedType="predicted";
    
    if(_PredictedError.checked) {
        PredictedType="predicted_error";
    }     

//if  (!(_utils.isContains(countriesList, k))) continue;

    var tb_updated = '';
    if (iso in data) { /** will return true if exist */
        for (var k in data[iso]) {
            var country_data = data[iso][k];
            
            let _regionName='';
            
            if  ((_utils.isContains(countriesListSubnational, k))){
                _regionName = countriesListSubnational.find(x => x["admin_id"] === k)["region_name"].substring(0, 25);
            }
            
            tb_updated = tb_updated + '<tr style="background-color: #dfd5d5"><td ></td><td ></td><td>' + _regionName + '  </td>';
            for (var km in modelsList) {
                if (_GroundTruth){
                    tb_updated = tb_updated + '<td>' + _utils.roundToTwo(country_data[km]) + '</td>';
                }else{
//                    tb_updated = tb_updated + '<td>' + _utils.roundToTwo(country_data[km][PredictedType]) + '</td>';
                    
                    if(_PredictedError.checked) {
                        tb_updated = tb_updated + `
                                <td>` + _utils.roundToTwo(country_data[km]["predicted"]) + ` &nbsp;&nbsp; (<i> ` + _utils.roundToTwo(country_data[km]["predicted_error"]) +  `</i>)</td>`;
                    }else{
                        tb_updated = tb_updated + `
                                <td>` + _utils.roundToTwo(country_data[km]["predicted"]) +`</td>`;
                    }                       
                }
                
                
            }
            tb_updated = tb_updated + '</tr>';
        }
    }
    return(tb_updated);
}


export function load_data_BottomTable(data, 
                                      data_sub, 
                                      _GroundTruth, 
                                      countriesList, 
                                      countriesListSubnational, 
                                      model_selected, 
                                      modelsList, 
                                      iso=null, 
                                      minPanel=true,
                                      scroll=false) {
                                          
                                   

    var _PredictedError = document.getElementById('chPredictedError');
    let PredictedType="predicted";
    
    if(_PredictedError.checked) {
        PredictedType="predicted_error";
    }     

    var tb_container = document.getElementById('tb_container');

    var models = [];

    // getting first country in the data
    var fCountry = Object.keys(data)[0];

    // getting the list of models
    for (var k in modelsList) {
        models.push(k);
    }


    var tb_updated = `<table id="tblBottom" data-order='[[ 2, "asc" ]]' class="table table-sm" style="width:100%">
    <colgroup>
    <col class=""></col>
    <col class=""></col>
    <col class=""></col>`;

    for (var i = 0; i < models.length; i++) {

        var model = models[i];
        
        if (model === model_selected) {
            tb_updated = tb_updated + '<col style="background-color: #D7D4D4"></col>';
        } else {
            tb_updated = tb_updated + '<col></col>';
        }
    }

    tb_updated = tb_updated + '</colgroup>';
    tb_updated = tb_updated + `<thead>
            <tr>
                <th class="no-sort"></th>
                <th class="no-sort"></th>
                <th class="no-sort"></th>
                <th>Country</th>`;

    for (var i = 0; i < models.length; i++) {
        
        if(_PredictedError.checked) {
            tb_updated = tb_updated + '<th scope="col" class="highlight">' + modelsList[models[i]]["name"] + ' (uncertainty)</th>';
        }else{
            tb_updated = tb_updated + '<th scope="col" class="highlight">' + modelsList[models[i]]["name"] + '</th>';
        }           
    };
    
    tb_updated = tb_updated + `</tr>
        </thead>
        <tbody>`;

    for (var k in data) {
       
       if (data_sub[k] === undefined || data_sub[k] === null) continue;
        
       if  (!(_utils.isContains(countriesList, k))) continue;

        var hilighted_country_style = '';
        
        if (_utils.isEmpty(iso)) {
            hilighted_country_style = '';
        } else {
            if (iso === k)
                hilighted_country_style = 'style="background-color: #D7D4D4"';
        }
    
        var country_name = countriesList.find(x => x["iso3code"] === k)["country"].substring(0, 25);

        tb_updated = tb_updated + `
                            <tr ` + hilighted_country_style + `>
                                <td>`+k+`</td>
                                <td class="text-end" style="cursor: pointer;"><span>+</span></td>
                                <td class="fib" style="background-image: url(./img/flags/gif/` + k.toLowerCase() + `.gif);background-size: 65% 65%;"></td>
                                <td style="cursor: pointer;">` + country_name + `</td>`;

        var country_date = data[k];

//        for (var m in country_date) {
//
//            tb_updated = tb_updated + `
//                                <td>` + _utils.roundToTwo(country_date[m]) + `</td>`;
//
//        }

        for (var k in modelsList) {
            
            if (_GroundTruth){
            tb_updated = tb_updated + `
                                <td>` + _utils.roundToTwo(country_date[k]) + `</td>`;
            }else{
                
                    if(_PredictedError.checked) {
                        tb_updated = tb_updated + `
                                <td>` + _utils.roundToTwo(country_date[k]["predicted"]) + ` &nbsp;&nbsp; (<i> ` + _utils.roundToTwo(country_date[k]["predicted_error"]) +  `</i>)</td>`;
                    }else{
                        tb_updated = tb_updated + `
                                <td>` + _utils.roundToTwo(country_date[k]["predicted"]) +`</td>`;
                    }   
            }
        }       
        
        
        tb_updated = tb_updated + `</tr>`;
    }
    tb_updated = tb_updated + `</tbody></table>`;


    tb_container.innerHTML = tb_updated;


    $('#tblBottom').dataTable({
                paging: true,
                bInfo: false,
                scrollY: 280,
                bDestroy: true,
                deferRender: true,
                scroller:   true,  
                sScrollX: true,
            initComplete: function () {
//            var api = this.api();
//            
//            api.$('td').click(function (row) {
//
//                var rowValuse = api.data()[row.delegateTarget._DT_CellIndex.row];
//                if (row.delegateTarget._DT_CellIndex.column === 2){
//
//                }
//            });
        }
    });
    
    
//     var heightScreen = $(window).height()*40/100;
//    
//    var container_scrollHead = document.getElementsByClassName('dataTables_scrollHead')[0];
//    var container_filter = document.getElementsByClassName('dataTables_filter')[0];   
//    
//    var offsetRight =  heightScreen -  container_scrollHead.offsetHeight -  container_filter.offsetHeight -  $('#iconTableMaximize').outerHeight() - 40;


    var container_table = document.getElementsByClassName('leaflet-control-bar-bottom leaflet-control-bar')[0];
    var container_scrollHead = document.getElementsByClassName('dataTables_scrollHead')[0];
    var container_filter = document.getElementsByClassName('dataTables_filter')[0];
    var height_tbl;
    var height_container_table;
        
    var offsetRight =  $('#table_bottom').outerHeight() -  container_scrollHead.offsetHeight -  container_filter.offsetHeight -  $('#iconTableMaximize').outerHeight() - 30;
    var scrollPos = $(".dataTables_scrollBody").scrollTop();
        
   
    
    if (minPanel === true) {

        var heightScreen = $(window).height() * 40 / 100;
        height_tbl = heightScreen - container_scrollHead.offsetHeight - container_filter.offsetHeight - $('#iconTableMaximize').outerHeight();
        height_container_table = heightScreen + $('#lbTableMaximize').outerHeight() + container_filter.offsetHeightm + $('#iconTableMaximize').outerHeight();
        container_table.setAttribute("style", "height:" + height_container_table + "px");

    } else {

        height_tbl = $('#map').height() - $('#topNavbarDiv').outerHeight() - container_scrollHead.offsetHeight - container_filter.offsetHeight - $('#iconTableMaximize').outerHeight();
        height_container_table = $('#map').height() - $('#topNavbarDiv').outerHeight() + $('#iconTableMaximize').outerHeight() + container_filter.offsetHeight;
        container_table.setAttribute("style", "height:" + height_container_table + "px");

    }    
    
  let table = new DataTable('#tblBottom', {
        "fnRowCallback": function (nRow, aData, iDisplayIndex) {

            if (aData[0] === iso) {
                $(nRow).css('background-color', '#D7D4D4');
            } else {
                $(nRow).css('background-color', '');
            }
        },      
                paging: true,
                bInfo: false,
                scrollY: height_tbl,
                bDestroy: true,
                deferRender: true,
                scroller:   true,  
                sScrollX: true,
                columnDefs: [
                {
                    target: 0,
                    visible: false,
                    searchable: true
                },
                {
                    target: 1,
                    visible: true,
                    searchable: true,
                    width: "2px"   
                },
                {
                    target: 2,
                    visible: true,
                    searchable: true,
                    width: "10px"   
                }
                ],
            initComplete: function () {
            var api = this.api();
            
            api.$('td').click(function (row) {

//                var rowValuse = api.data()[row.delegateTarget._DT_CellIndex.row];
//                if (row.delegateTarget._DT_CellIndex.column === 2){
//                  zoomToCountryTable(rowValuse[0], _layer, _map, countriesList);
//                }
//                
           
             
             
            });
        }
    });
    

    if (scroll){
        table.rows().data().map((row, index) => {
            if (row[0] === iso) {
                table.scroller().scrollToRow(index-1);
            }
        });
    }else{
        $(".dataTables_scrollBody").scrollTop(scrollPos);
    }    
    

table.rows().every(function (index) {
    var row = table.row( index );
    var data = row.data();
    this.child(
        $(
            sort_subnational_child_rows(data[0], data_sub, _GroundTruth, modelsList, countriesListSubnational)
        )
    ).hide();
});
   
    
    table.on('click', function (e) {
        let tr = e.target.closest('tr');
        let row = table.row(tr);
        
        var td = $(row).find('td:eq(0)');
        var tdP = $(tr).find("td").eq(0);
  
    if (row.child.isShown()) {
        // This row is already open - close it
        row.child.hide();
        
        tdP.children('span').text("+");
    }
    else {
        // Open this row
        row.child.show();
        tdP.children('span').text("-");
    }
    });
    
            // Add event listener for opening and closing details
//    $('#tblBottom tbody').on('click',function () {
//        alert("sda");
//        var tr = $(this).closest('tr');
//        var row = $('#tblBottom').row( tr );
// 
//        if ( row.child.isShown() ) {
//            // This row is already open - close it
//            row.child.hide();
//            tr.removeClass('shown');
//        }
//        else {
//            // Open this row
//            row.child( format("sd") ).show();
//            tr.addClass('shown');
//        }
//    } );

}
