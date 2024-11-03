$(document).ready(function () {


var isResizing = false,
    lastDownX = 0;
    
var container_table = document.getElementsByClassName('leaflet-control-bar-bottom leaflet-control-bar')[0];
var btnDrag = document.getElementById('drag');
  

if ('ontouchstart' in window) {
   
    btnDrag.addEventListener('touchstart', function(){ isResizing = true;  });
    btnDrag.addEventListener('touchleave', function(){ isResizing = false; });
    btnDrag.addEventListener('touchcancel', function(){ isResizing = false; });
    document.addEventListener('touchleave', function(){ isResizing = false; });
    document.addEventListener('touchend', function(){ isResizing = false; });
   
    document.addEventListener('touchmove', touchHandler, false);

    function touchHandler(e) {
        if (!isResizing) 
            return;
        
        var x = e.touches[0].clientX;
        var y = e.touches[0].clientY;

        const container_tbl = $("#tblBottom");
        var container_scrollHead = document.getElementsByClassName('dataTables_scrollHead')[0];
        var container_filter = document.getElementsByClassName('dataTables_filter')[0];
        
        const height_tbl = $('#topNavbarDiv').outerHeight() + $('#map').height() - container_scrollHead.offsetHeight - container_filter.offsetHeight - y;
        var offsetRight =  $('#map').height() + $('#topNavbarDiv').outerHeight()   - y ;
        
        $('#tblBottom').DataTable(
            {
                paging: true,
                bInfo: false,
                scrollY: height_tbl,
                bDestroy: true,
                deferRender:    true,
                scroller:       true,
                "responsive": true,
                "sScrollX": "100%",
                "scrollCollapse": true  
            }
        );       

        container_table.setAttribute("style","height:"+offsetRight+"px");        
    }   
   
   
}else{
    
    $(function () {
        var container = $('#container'),
        handle = $('#drag');
        var container_table = document.getElementsByClassName('leaflet-control-bar-bottom leaflet-control-bar')[0];
    
        handle.on('mousedown', function (e) {
            isResizing = true;
        });


        $(document).on('mousemove', function (e) {
        if (!isResizing) 
            return;
       
        const container_tbl = $("#tblBottom");
        var container_scrollHead = document.getElementsByClassName('dataTables_scrollHead')[0];
        var container_filter = document.getElementsByClassName('dataTables_filter')[0];
        
        var offsetRight =  $('#map').height() + $('#topNavbarDiv').outerHeight()   - (e.clientY ) ;
        
        const height_tbl = $('#topNavbarDiv').outerHeight() + $('#map').height() - container_scrollHead.offsetHeight - container_filter.offsetHeight - (e.clientY )-20; 
        $('#tblBottom').DataTable(
            {
                paging: true,
                bInfo: false,
                scrollY: height_tbl,
                bDestroy: true,
                deferRender:    true,
                scroller:       true,  
                sScrollX: true
            }
        );       
         
        container_table.setAttribute("style","height:"+offsetRight+"px");
        }).on('mouseup', function (e) {
            isResizing = false;
        });
    });     
   
   
}

});