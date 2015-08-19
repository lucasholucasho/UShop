var userLatitude, userLongitude, finalLatitude, finalLongitude;
var userLocationEmpty = true;
var destinationLatitudeEmpty = true;
var destinationLongitudeEmpty = true;

$(document).ready(function() {
	disableHailUberButtonWhenPageLoads();
	populateLatLong();
});

navigator.geolocation.watchPosition(function(position) {
	userLatitude = position.coords.latitude;
	userLongitude = position.coords.longitude;
	userLocationEmpty = false;
	$("#callUber").prop("disabled", userLocationEmpty || destinationLatitudeEmpty || destinationLongitudeEmpty);
	setColorOfCallUberButton();
});

var disableHailUberButtonWhenPageLoads = function () {
	$("#callUber").prop("disabled",true);	
}

var populateLatLong = function() {
	$("#stores input:radio").click(function() {
	   latLongString = $(this).val();
	   var latLongStringSplit = latLongString.split(",");
	   var latitude = latLongStringSplit[0];
	   var longitude = latLongStringSplit[1];
	   $('#destinationLatitude').val(latitude);
	   $('#destinationLongitude').val(longitude);
	   finalLatitude = $('#destinationLatitude').val();
	   finalLongitude = $('#destinationLongitude').val();
	   destinationLatitudeEmpty = false;
	   destinationLongitudeEmpty = false;
	   $("#callUber").prop("disabled", userLocationEmpty || destinationLatitudeEmpty || destinationLongitudeEmpty);
	   setColorOfCallUberButton();
	});
}

var setColorOfCallUberButton = function () {
	if ($('#callUber').prop('disabled') == true)
	{
       $('#callUber').css('background-color', "#71BC78");
	}
	else
	{
	   $('#callUber').css('background-color', "green");
	}
}