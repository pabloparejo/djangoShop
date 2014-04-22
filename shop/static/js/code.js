var $add_btn		= $('.add-to-cart'),
	base_url 		= "http://query.yahooapis.com/v1/public/yql?",
	$cart 			= $('#cart-box'),
	$cart_btn 		= $('#cart a'),
	$close_cart		= $('#close-cart'),
	$content 		= $('#content'),
	positionCoords	= {},
	$ls				= localStorage;
	path 			= location.pathname.split('/')[1],
	$cart_product	= $(".cart-product").first(),
	$search			= $('#search-bar'),
	$search_btn 	= $("#search a");


function setActive(){
	$('.active').removeClass();
	if (!path){
		path = 'home';
	}
	$('#' + path + ' a').addClass('active');

	if (path == "checkout"){
		$cart_btn.addClass('active')
	}
}

function toggleBtnActive(btn){
	if (btn.hasClass('active')) {
		setActive();
	}else{
		$('.active').removeClass();
		btn.addClass('active');
	}
}

// -------- COOKIES -------- //

function setCookie(cname,cvalue,exdays){
    var d = new Date();
    d.setTime(d.getTime()+(exdays*24*60*60*1000));
    var expires = "expires="+d.toGMTString();
    document.cookie = cname+"="+cvalue+"; "+expires+ ";path=/;";
}

// -------- DAJAX ICE -------- //

$('.switchForm-btn').click(DajaxSwitchForm);

function DajaxSwitchForm(e){
	e.preventDefault();
	Dajaxice.userprofiles.switchForm(switchFormFields);
}

function switchFormFields(data){

	clone = $('.sign').clone();
	clone.find('.form-title').text(data.title);
	clone.find('.submit-btn').attr('value', data.title);
	clone.find('.form-content').html(data.content);
	clone.find('.switchForm-btn').text($('.form-title').text());
	$('.sign').slideUp();
	$('#content').prepend(clone);
	clone.hide();
	clone.slideDown();
	setCookie('form', data.cookie, 7);
	$('.switchForm-btn').click(DajaxSwitchForm);
	setTimeout(function(){
		$('.sign').last().remove();
	}, 500);

}


// -------- CART -------- //
if ($ls.getItem('cart')){
	if ($ls.getItem('cart').length > 2){
		// ls['cart'] is plain text. If length < 2 => ls['cart'] == []
		$('.empty-flag').addClass('hide');
		$cart.children('.delete').remove();
		$cart.removeClass('is_empty');
		var cartLS = JSON.parse($ls.getItem('cart'));
		for (product in cartLS){
			appendProductToCart(cartLS[product]);
		}
	}
}

if ($cart.hasClass('is_empty')){
	$('.checkout-page .submit-btn').addClass('inactive');
}

function saveProduct(product){
	if ($ls.getItem('cart')){
		var found = false
		var cartLS = JSON.parse($ls.getItem('cart'));
		for (i in cartLS){
			if (product.id == cartLS[i].id){
				cartLS[i] = product;
				found = true;
			}
		}
		if (!found){
			cartLS.push(product);
		}
		$ls['cart'] = JSON.stringify(cartLS);
	}else{
		$ls['cart'] = "[" + JSON.stringify(product) + "]";
	}	
}

function itemFromId(p_id){
	var product 	= $('#' + p_id),
		p_title 	= product.children('.product-title').children('a'),
		price 		= product.children('div').children('.price');

	var item = {id			: p_id,
				title		: p_title.html(),
				title_url	: p_title.attr('href'),
				price		: price.html(),
				quantity	: 1};
	return item;
}

function appendProductToCart(product){
	clone = $cart_product.clone();
	clone.attr('id', product.id)
	clone.children('.quantity').text(product.quantity)
	clone.children('a.title').attr('href', product.title_url)
	clone.children('a.title').text(product.title)
	clone.children('.price').text(product.price);
	clone.children('.delete-btn').attr('id', product.id);
	clone.removeClass('hide');
	clone.removeClass('delete');
	$('.empty-flag').addClass('hide');
	$cart.append(clone);
	$('.delete-btn').click(deleteProduct);
}

function getItemFromLS(p_id){
	var cartLS = JSON.parse($ls.getItem('cart'))
	for (i in cartLS){
		if (p_id == cartLS[i].id){
			return cartLS[i];
		}
	}
	return "";
}

function addItem(e){
    e.preventDefault();
	if ($cart.hasClass('is_empty')){
		$cart.removeClass('is_empty');
		$('.submit-btn').removeClass('inactive');
		var item = itemFromId(this.id);
		saveProduct(item);
		appendProductToCart(item);
		$cart.children(".delete").remove();
	}else{
		if ($cart.children("#"+this.id).length > 0 ){
			var prod = $cart.children("#"+this.id);
			var item = getItemFromLS(this.id);
			item.quantity += 1;
			saveProduct(item);
			prod.children('.quantity').text(item.quantity);
		}else{
			var item = itemFromId(this.id);
			saveProduct(item);
			appendProductToCart(item);
		}
	}
	$cart.slideDown();
	toggleBtnActive($cart_btn);
	$cart.children("#"+this.id).addClass("new");
	setTimeout(function(){
		$cart.slideUp();
		toggleBtnActive($cart_btn);
		$cart.children(".new").removeClass("new");
	}, 2400);
}


function searchToggle(){
	$cart.slideUp();
	toggleBtnActive($search_btn)
	$search.toggleClass('show');
	$search.slideToggle();
}

function cartToggle(){
	$search.slideUp();
	toggleBtnActive($cart_btn)
	$cart.toggleClass('show');
	$cart.slideToggle();
}

function deleteProduct(e){
	e.preventDefault();
	if ($ls.getItem('cart')){
		var found = false
		var cartLS = JSON.parse($ls.getItem('cart'));
		for (i in cartLS){
			if (this.id == cartLS[i].id){
				cartLS.splice(i, 1)
				found = true;
			}
		}
		$ls['cart'] = JSON.stringify(cartLS);
	}

	if (cartLS.length == 0) {
		$cart.addClass('is_empty');
		$('.empty-flag').removeClass('hide');
		$('.submit-btn').addClass('inactive');

		setTimeout(function(){
			$cart.slideUp();
		}, 1000);
	}

	$cart.children('#'+this.id).remove();


}


function clearCart(){
	$ls['cart'] = '';
	$cart.children('.cart-product').remove();
	$cart.addClass('is_empty');
	$('.empty-flag').removeClass('hide');
	$('.submit-btn').addClass('inactive');
}

// -------- LOCATION & YAHOO AJAX -------- //

function geoSuccess(position){
    var lat = position.coords.latitude;
    var lon = position.coords.longitude;

    positionCoords = position.coords

    obtenerGeoInfo(lat, lon);
}

function geoError(){
    console.log("Location denied");
}

function obtenerGeoInfo(lat, lon){

	var query = "SELECT * FROM geo.placefinder WHERE text='"+lat+", "+lon+"'";
	query += " AND gflags='R'";

	query = encodeURIComponent(query);

	var opts = {
		url: base_url + 'q=' + query,
		dataType : 'jsonp',
		jsonpCallback: 'geoInfoCallBack',
		data:{
			format:'json'
		}
	}

	$.ajax(opts)
}

function removeAutofilled(){
	this.className = "";
}

function geoInfoCallBack(data){
	var info 	= data.query.results.Result,
		city	= info.city,
		county 	= info.county,
		street	= info.street,
		post	= info.postal;

	$('#id_postal_code').attr('value', post).addClass('autofilled');
	$('#id_city').attr('value', county).addClass('autofilled');

	if (positionCoords.accuracy < 60){
		$('#id_street').attr('value', street).addClass('autofilled');
	}
	$('#id_postal_code').on('focus', removeAutofilled);
	$('#id_city').on('focus', removeAutofilled);
	$('#id_street').on('focus', removeAutofilled);
}

setActive();
$add_btn.click(addItem);
$cart_btn.click(cartToggle);
$close_cart.click(cartToggle);
$search_btn.click(searchToggle);

if (path == "checkout"){
	var geo = navigator.geolocation;
	options = {
	    enableHighAccuracy: true,
	    timeout: 5000,
	    maximumAge: 0
	};
	geo.getCurrentPosition(geoSuccess, geoError, options);

	cartJSONdata = $('.checkout-form').children().first().clone();
	cartJSONdata.attr('name', 'cartJSONdata');
	cartJSONdata.attr('value', $ls.getItem('cart'));

	$('.checkout-form').prepend(cartJSONdata);
}

if (path == "checkout-succes"){
	clearCart();
}

