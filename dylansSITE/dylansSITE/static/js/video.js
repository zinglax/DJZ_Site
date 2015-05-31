(function(){
	var 	//canvas = document.getElementById('canvas'),
		//context = canvas.getContext('2d'),
		video = document.getElementById('video'),
		snap = document.getElementById('snap'),
		vendorUrl = window.URL ||  window.webkitURL;
		height = window.height
		width = window.width
		half_height = Math.floor(height/2)
		half_width = Math.floor(width/2)
		

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


	
	// To Repeat video
	//video.addEventListener('play', function(){
		//draw(this, context, window.screen.width, window.screen.height);
	//}, false);
	
	//// Detect screen size	
	alert(Math.floor(window.screen.width/2)+"x"+Math.floor(window.screen.height/2));	
	//alert(window.screen.width+"x"+window.screen.height);	
	
	//video.setAttribute("heigth", Math.floor(window.screen.height/2).toString());	
	//canvas.setAttribute("heigth", Math.floor(window.screen.height/2).toString());	
	//video.setAttribute("width", Math.floor(window.screen.width/2).toString);
	//canvas.setAttribute("width", Math.floor(window.screen.width/2).toString);
	
	//video.height = Math.floor(window.screen.height/2)
	//video.width = Math.floor(window.screen.width/2)
	//canvas.height = window.screen.height
	//canvas.width = window.screen.width
	//canvas.height = 0
	//canvas.widht = 0
	//canvas.height = Math.floor(window.screen.height/2)
	//canvas.width = Math.floor(window.screen.width/2)
	//canvas.width = window.screen.width	
		
	
	////To take photo
	//snap.addEventListener('click', function(){
		//context.drawImage(video, 0	, 0, half_width, half_height);
	//}, false);
	

	function draw(video, context, width, height){
		context.drawImage(video, 0, 0, width, height);
		setTimeout(draw, 10, video, context, width, height);
		
	}	
		
	
})();