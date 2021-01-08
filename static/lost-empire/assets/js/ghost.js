// JavaScript for the cart counter on NavBar

// Check if the Nav cart UI is available
if (document.querySelector("#navbar_cart_count")) {
	// Check if cart is empty (undefined)
	if (localStorage.getItem("cart_list") == "undefined") {
		localStorage.removeItem("cart_list"); // Remove the LocalStorage item "cart_list"
	}

	// If the cart has items display the number of items in the cart
	if (localStorage.getItem("cart_list")) {
		const number_of_items = JSON.parse(localStorage.getItem("cart_list")).length;
		if (number_of_items <= 0 ) {
			document.querySelector("#navbar_cart_count").innerHTML = 0;
		} else {
			document.querySelector("#navbar_cart_count").innerHTML = number_of_items;
		}
	} else {
		document.querySelector("#navbar_cart_count").innerHTML = 0;
	}
}
