$(document).ready(function(){

	console.log("iniciando");

	function getResults(){
		$.ajax({
			url: '/results',
			dataType: 'json'
		})
		.done(function(response){
			var out1 = response.out1
			var out2 = response.out2

			var layout1 = {
				height : 400,
				width : 500,
				title: " Proporción de la clasificación 1"
			};

			var layout2 = {
				height : 400,
				width : 500,
				title: " Proporción de la clasificación 2"
			};

			Plotly.newPlot('output1', out1, layout1);
			Plotly.newPlot('output2', out2, layout2);
		});
	};

	function getPreprocessing(){
		$.ajax({
			url: '/preprocessing',
			dataType: 'json'
		})
		.done(function(response){
			var histo_all_data = response.whole
			var histo_good_data = response.good
			var histo_bad_data = response.bad

			var layout1 = {
				height : 500,
				width : 1000,
				title: 'Palabras con mayor frecuencia en Train'
			};

			var layout2 = {
				height : 500,
				width : 1000,
				title: 'Palabras con mayor frecuencia en Reviews Buenos'
			};

			var layout3 = {
				height : 500,
				width : 1000,
				title: 'Palabras con mayor frecuencia en Reviews Malos'
			};

			Plotly.newPlot('histo-all', histo_all_data, layout1);
			Plotly.newPlot('histo-good', histo_good_data, layout2);
			Plotly.newPlot('histo-bad', histo_bad_data, layout3);

			getResults();
		});
	};


	function getExploratory(){
		$.ajax({
			url: '/exploratory',
			dataType: 'json'
		})
		.done(function(response){
			var text_data = response.texts
			var pie_data = response.pie

			var layout = {
			  height: 400,
			  width: 500,
			  title: 'Proporcion de las Clases en Train'
			};

			Plotly.newPlot('pie', pie_data, layout);

			$("#body-review-good").append("<p>"+text_data[0]+"</p>")
			$("#body-review-bad").append("<p>"+text_data[1]+"</p>")

			getPreprocessing();
		});
	};
	
	$(":file").filestyle({icon: false});

	$("#test-info").fadeIn(3000);
	$("#loading").fadeIn(3000);
	
	$.ajax({
		url: '/test_file'
	})
	.done(function(){
		$("#test-info").fadeOut(2500);
		$("#loading").fadeOut(2500);
		$("#test-success").fadeIn(3000);
		$("#test-success").fadeOut(3500);
		$("#pcontent").fadeIn(3500);

		getExploratory();
	});
 
});
