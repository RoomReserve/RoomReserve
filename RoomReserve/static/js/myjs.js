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
