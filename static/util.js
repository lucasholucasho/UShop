function actionForShoppingProducts(shoppingProduct, latitude, longitude) {
    window.location.replace('/shoppingsearch/'+shoppingProduct+'/'+latitude+'/'+longitude);
}

function actionForHailingUber(start_latitude, start_longitude, end_latitude, end_longitude) {
	window.location.replace('/hailUber/'+start_latitude+'/'+start_longitude+'/'+end_latitude+'/'+end_longitude);
}

function redirect_to_demo(code) {
    window.location.replace('/demo');
}