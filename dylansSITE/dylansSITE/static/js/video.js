(function(){
	var 	canvas = document.getElementById('canvas'),
		context = canvas.getContext('2d'),
		video = document.getElementById('video'),
		snap = document.getElementById('snap'),
		vendorUrl = window.URL ||  window.webkitURL;

	navigator.getMedia = 	navigator.getUserMedia ||
				navigator.webkitGetUserMedia ||
				navigator.mozGetUserMedia ||
				navigator.msGetUserMedia;

	navigator.getMedia({
		video: true,
		audio: false
	}, function(stream) {
		video.src = vendorUrl.createObjectURL(stream);
		video.play();
	}, function(error) {
		// an error occured
		// error.code
	});

	//video.addEventListener('play', function(){
		//draw(this, context, 400, 300);
	//}, false);
	
	snap.addEventListener('click', function(){
		context.drawImage(video, 0, 0, 400, 300);
	}, false);
	

	function draw(video, context, width, height){
		context.drawImage(video, 0, 0, width, height);
		setTimeout(draw, 10, video, context, width, height);
		
	}	
		
	
})();