$(document).ready(function () {
	console.log("draw.js loaded");

	
	if (typeof shots_array !== 'undefined') {

		var tooltip = $("#heatmap").opentip("Shown after 2 seconds", { delay: 2, style: 'glass' });

		var shot_array = data_array;
		var data = shots_array;
		var max = max_value;
		//alert("DATA = TRUE");
		console.log(max);
		var canvas = $("#heatmap")[0];
		var canvas_height = canvas.height;
		var canvas_width = canvas.width;
		var max_value2 = 0;
		for (var i = 0; i < data.length; i++) {
			data[i][0] = data[i][0]*canvas_width/120;
			data[i][1] = data[i][1]*canvas_height/60;
			if (data[i][2] > max_value2) {
				max_value2 = data[i][2];
			}
		}
		console.log(max_value2 / max);
		//console.log(data);
		var heat = simpleheat(canvas);
		heat.data(data);
		heat.max(max);
		//heat.gradient({0.00005: ['blue', 0.4], 0.0005: ['cyan', 0.55], 0.005: ['lime', 0.7], 0.05: ['yellow', 0.85], 0.50: ['red', 1]})
		//heat.gradient({0.00005: 'blue', 0.0005: 'cyan', 0.005: 'lime', 0.05: 'yellow', 0.50: 'red'})
		//heat.gradient({0.005: ['blue', 0.4], 0.0158: ['cyan', 0.55], 0.05: ['lime', 0.7], 0.158: ['yellow', 0.85], 0.50: ['red', 1]})
		var blob_radius = Math.floor(10 / 973 * canvas_width);
		var blob_blur = Math.floor(5 / 973 * canvas_width);

		heat.radius(blob_radius, blob_blur);
		heat.draw(0);

		$("#heatmap").on( "mousemove",
			function(e) {
				var parentOffset = $(this).offset(); 
				//or $(this).offset(); if you really just want the current element's offset
				var relX = e.pageX - parentOffset.left;
				var relY = e.pageY - parentOffset.top;

				var arrX = Math.floor(relX / canvas_width * 120);
				var arrY = Math.floor(relY / canvas_height * 60 );
				var val = shot_array[arrY][arrX];
				tooltip.setContent("Shots: " + val);
			});
	}

});