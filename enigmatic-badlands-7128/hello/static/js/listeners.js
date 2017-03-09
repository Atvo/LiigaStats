$(document).ready(function () {
	init_listeners();
	resize_canvas();

	/*var data = [
	[1, 1, 0.5],
	[40, 1, 0.5],
	[1, 60, 0.2],
	[20, 1, 0.7],
	[1, 3, 0.5],
	]
	var canvas = $("#heatmap")[0];
	console.log(canvas);
	var heat = simpleheat(canvas);
	heat.data(data);
	heat.draw();
*/
});

var init_listeners = function() {

	init_filter_listener();
	init_submit_listener();
	init_datatable();

}

var init_filter_listener = function() {
	$( ".shot_filter" ).on( "change", function( event ) {
		event.preventDefault();

		var url_str = "update_filters/";
		var season = $("#season_filter").val()
		var team = $("#shooting_team_filter").val()
		var shooter = $("#shooter_filter").val()
		var outcome = $("#outcome_filter").val()

		var advanced_filters = $("#advanced_filters_chx").is(':checked')
		if ($("#goal_chx").length) {
			console.log("checkbox found")
		}

		var goal_checked = $("#goal_chx").is(':checked')
		var save_checked = $("#save_chx").is(':checked')
		var miss_checked = $("#miss_chx").is(':checked')
		var block_checked = $("#block_chx").is(':checked')

		if ($("#even_chx").length) {
			even_checked = $("#even_chx").is(':checked')
		}
		else {
			even_checked = true
		}
		if ($("#pp_chx").length) {
			pp_checked = $("#pp_chx").is(':checked')
		}
		else {
			pp_checked = true
		}
		if ($("#sh_chx").length) {
			sh_checked = $("#sh_chx").is(':checked')
		}
		else {
			sh_checked = true
		}

		var team_against = "All"
		var goalie = "All"
		var first_assist = "All"
		var second_assist = "All"
		var blocker = "All"

		if (advanced_filters == true) {

			if ($("#team_against_filter").length) {
				team_against = $("#team_against_filter").val()
			}

			if ($("#goalie_filter").length) {
				goalie = $("#goalie_filter").val()
			}
			if (goal_checked == true) {
				if ($("#first_assist_filter").length) {
					first_assist = $("#first_assist_filter").val()
				}

				if ($("#first_assist_filter").length) {
					first_assist = $("#first_assist_filter").val()
				}
				if ($("#second_assist_filter").length) {
					second_assist = $("#second_assist_filter").val()
				}
			}
			if (block_checked == true) {
				if ($("#blocker_filter").length) {
					blocker = $("#blocker_filter").val()
				}
			}
			//ToDo: Check checkbox existence for team strengths
		}
		console.log(goal_checked);
		$.post(url_str,
		{
			season: season,
			team: team,
			shooter: shooter,
			advanced_filters: advanced_filters,
			goal_checked: goal_checked,
			save_checked: save_checked,
			miss_checked: miss_checked,
			block_checked: block_checked,
			even_checked: even_checked,
			pp_checked: pp_checked,
			sh_checked: sh_checked,
			team_against: team_against,
			goalie: goalie,
			first_assist: first_assist,
			second_assist: second_assist,
			blocker: blocker,
		},
		function(data,status){
			var message = data;
			var form = $("#shot_filter_form")
			form.replaceWith(message);
			init_filter_listener();
			init_submit_listener();
		});
	});
}

var init_submit_listener = function() {
	$( "#shot_filter_form" ).submit(function( event ) {
		event.preventDefault();
		console.log("submit");

		var url_str = "update_table/";
		var season = $("#season_filter").val()
		var team = $("#shooting_team_filter").val()
		var shooter = $("#shooter_filter").val()
		var outcome = $("#outcome_filter").val()

		var advanced_filters = $("#advanced_filters_chx").is(':checked')
		var goal_checked = $("#goal_chx").is(':checked')
		var save_checked = $("#save_chx").is(':checked')
		var miss_checked = $("#miss_chx").is(':checked')
		var block_checked = $("#block_chx").is(':checked')
		
		if ($("#even_chx").length) {
			even_checked = $("#even_chx").is(':checked')
		}
		else {
			even_checked = true
		}
		if ($("#pp_chx").length) {
			pp_checked = $("#pp_chx").is(':checked')
		}
		else {
			pp_checked = true
		}
		if ($("#sh_chx").length) {
			sh_checked = $("#sh_chx").is(':checked')
		}
		else {
			sh_checked = true
		}

		var team_against = "All"
		var goalie = "All"
		var first_assist = "All"
		var second_assist = "All"
		var blocker = "All"

		if (advanced_filters == true) {
			team_against = $("#team_against_filter").val()
			goalie = $("#goalie_filter").val()
			if (goal_checked == true) {
				first_assist = $("#first_assist_filter").val()
				second_assist = $("#second_assist_filter").val()
			}
			if (block_checked == true) {
				blocker = $("#blocker_filter").val()
			}
		}
		var heatmap_container_width = $("#heatmap_container").width();
		//ToDo: Start spinner
		show_loading_gif();
		console.log(even_checked);

		$.post(url_str,
		{
			season: season,
			team: team,
			shooter: shooter,
			advanced_filters: advanced_filters,
			goal_checked: goal_checked,
			save_checked: save_checked,
			miss_checked: miss_checked,
			block_checked: block_checked,
			even_checked: even_checked,
			pp_checked: pp_checked,
			sh_checked: sh_checked,
			team_against: team_against,
			goalie: goalie,
			first_assist: first_assist,
			second_assist: second_assist,
			blocker: blocker,
			heatmap_container_width, heatmap_container_width,
		},
		function(data,status){
			var message = data;
			var table = $("#stats_table")
			//var table = $("#heatmap_container");
			table.replaceWith(message);
			init_submit_listener();
			init_datatable();
			$('#table_id').DataTable();
			//ToDo: Stop spinner
	  		$("#loading_gif").hide()
		});
	});	
}

var init_datatable = function() {
	var t = $('#table_id').DataTable( {
        "columnDefs": [ {
            "searchable": false,
            "orderable": false,
            "targets": 0,
        } ],
        "lengthChange": false,
        "order": [[ 1, 'asc' ]]
    } );
	t.on( 'order.dt search.dt', function () {
        t.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        } );
    } ).draw();
}

var show_loading_gif = function () {
	var window_width = $("#stats_table").width();
	var window_height = $( window ).height();
	var gif_width = $("#loading_gif").width();
	var x = window_width / 2 - gif_width / 2;
	$("#loading_gif").css({top: 30, left: x});
	$("#loading_gif").show()
}

var resize_canvas = function () {
	console.log("resize_canvas");
	var canvas = $("#heatmap");
	var ctx = canvas.get(0).getContext("2d");
	var container = $("#heatmap_container");
	console.log("width: " + $(container).width())
	console.log("height: " + $(container).height())
	canvas.attr('width', $(container).width() ); //max width
	canvas.attr('height', $(container).height() ); //max height
}
