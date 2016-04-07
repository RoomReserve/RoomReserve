$(document).ready(function() {
$('#datatables').DataTable(
	{
	// Disable sorting for 'Edit' button
	  "columnDefs": [ {
	      "targets": 5,
	      "orderable": false
	    } ]
	}
	);
} );



$(function() {
    $('.tooltip-wrapper').tooltip({position: "bottom"});
});



// panel collapse 
$(function ($) {
    $('.panel-heading span.clickable').on("click", function (e) {
        if ($(this).hasClass('panel-collapsed')) {
            // expand the panel
            $(this).parents('.panel').find('.panel-body').slideDown();
            $(this).removeClass('panel-collapsed');
            $(this).find('i').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
        }
        else {
            // collapse the panel
            $(this).parents('.panel').find('.panel-body').slideUp();
            $(this).addClass('panel-collapsed');
            $(this).find('i').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
        }
    });
});