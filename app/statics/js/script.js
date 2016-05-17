$(document).ready(function(){
	$(":file").filestyle({icon: false});

	$("#train-info").fadeIn(3000);
	$("#loading").fadeIn(3000);
	
	$.ajax({
		url: '/train'
	})
	.done(function(){
		$("#train-info").fadeOut(2500);
		$("#loading").fadeIn(2500);
		$("#train-success").fadeIn(3000);
		$("#run").fadeIn(3000);
	});
});
