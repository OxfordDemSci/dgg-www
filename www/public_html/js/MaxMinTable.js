$(document).ready(function () {

    $("#lbTableMaximize").click(function () {

        var container_table = document.getElementsByClassName('leaflet-control-bar-bottom leaflet-control-bar')[0];

        const container_tbl = $("#tblBottom");
        var container_scrollHead = document.getElementsByClassName('dataTables_scrollHead')[0];
        var container_filter = document.getElementsByClassName('dataTables_filter')[0];
        var height_tbl;
        var height_container_table;

        if ($("#iconTableMaximize").hasClass("fa-window-minimize")) {
            
            var heightScreen = $(window).height()*40/100;
            console.log(heightScreen);

            height_tbl = heightScreen - container_scrollHead.offsetHeight - container_filter.offsetHeight - $('#iconTableMaximize').outerHeight();
            height_container_table = heightScreen + $('#lbTableMaximize').outerHeight() + container_filter.offsetHeightm + $('#iconTableMaximize').outerHeight();
            container_table.setAttribute("style", "height:" + height_container_table + "px");


        } else {
            height_tbl = $('#map').height() - $('#topNavbarDiv').outerHeight() - container_scrollHead.offsetHeight - container_filter.offsetHeight - $('#iconTableMaximize').outerHeight();
            height_container_table = $('#map').height() - $('#topNavbarDiv').outerHeight() + $('#iconTableMaximize').outerHeight() + container_filter.offsetHeight;
            container_table.setAttribute("style", "height:" + height_container_table + "px");
        }

        $('#tblBottom').DataTable(
                {
                    paging: true,
                    bInfo: false,
                    scrollY: height_tbl,
                    bDestroy: true,
                    deferRender: true,
                    scroller: true,
                    sScrollX: true,
                    columnDefs: [
                    {
                        target: 0,
                        visible: false,
                        searchable: true
                    }
                    ]
                }
        );

        $(".fa-window-maximize").toggleClass("fa-window-minimize");

    });

});