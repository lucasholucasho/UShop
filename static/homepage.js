var userLatitude, userLongitude, shoppingProduct;
var locationEmpty = true;
var textEmpty = true;
$(document).ready(function() {
	disableSearchButtonsWhenPageLoads();
	enableShoppingSearchButtonWhenInputEntered();
	setSearchVariables();
});

navigator.geolocation.watchPosition(function(position) {
	userLatitude = position.coords.latitude;
	userLongitude = position.coords.longitude;
	locationEmpty = false;
	$("#nearbyUberProducts").prop("disabled", locationEmpty);
	$('#nearbyShoppingProducts').prop('disabled', locationEmpty || textEmpty);
	setColorOfSearchButton();
});

var disableSearchButtonsWhenPageLoads = function () {
	$("#nearbyUberProducts").prop("disabled", true);	
	$("#nearbyShoppingProducts").prop("disabled", true);
}

var enableShoppingSearchButtonWhenInputEntered = function () {
	$('input:text').keyup(function () {
	   textEmpty = false;
	   $('input:text').each(function(){
	   	  if($(this).val()==""){
	         textEmpty = true;      
	      }
	  	  shoppingProduct = $(this).val();
	   });
	   $('#nearbyShoppingProducts').prop('disabled', locationEmpty || textEmpty);
	   setColorOfSearchButton();
	});
}

var setColorOfSearchButton = function () {
	if ($('#nearbyShoppingProducts').prop('disabled') == true)
	{
       $('#nearbyShoppingProducts').css('background-color', "#71BC78");
	}
	else
	{
	   $('#nearbyShoppingProducts').css('background-color', "green");
	}
}

var setSearchVariables = function () {
	$("#nearbyShoppingProducts").click(function(shoppingProduct) {
	  	shoppingProduct = $('#productName').val();
	});
}