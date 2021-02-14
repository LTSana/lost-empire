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

// Used to control the Global Alert (STARTER GUIDE)
if (!localStorage.getItem("ShowGlobalAlert_v2")) {

	// Display the alert to the UI
	const GlobalAlert = document.createElement("span")
	GlobalAlert.innerHTML = `<section class="global-alert">
    <div class="container-fluid">
        <div class="row justify-content-center align-items-center">
            <div class="col-11 col-sm-11 col-md-11 col-lg-11 col-xl-10 global-alert-col">
                <h2 class="text-center"><strong>START GUIDE</strong></h2>
                <p class="text-break global-alert-p">Hi there, welcome to <strong>Lost Empire</strong><br />This is a <strong>LIVE DEMO</strong>. I&#39;ve changed the original purpose of <strong>Lost Empire</strong> to work with a <strong>Shopify build</strong> version of it.<br /><br />This website is a E-Commerce ESPORTS merchandize store.<br />The Teams &amp; merchandize on this website are not associated with <strong>Lost Empire</strong>. We are just using it for example purposes, if you wish to have them removed please contact me.<br /><br />You can Sign Up for an account.<br /><br />If you are interested in the source code visit:<br /><a href="https://github.com/LTSana/lost-empire" target="_blank" rel="noopener">GitHub/LTSana/lost-empire</a><br /><br /><strong>-- To have access to the Shopify Checkout Page --</strong><br /><strong>Store Password: crield</strong><br /><br /><strong>Only use these credentials for checkout.</strong><br /><br />Any transactions on this website or Shopify are not real &amp; uses a sandbox testing ground.<br />The merchandize is not real.<br /><br /><strong>** SUPPORT BY DONATING **</strong><br />If you like my work and would like to donate just visit my GitHub website at this link bellow for guidance on how you can.<br /><a href="https://ltsana.github.io/#hero_5" target="_blank" no="noopener"><strong>DONATE HERE</strong></a><br /><br />This website uses cookies, we use them to keep track of your cart items, we store your sessions in them, and we use it for analytic purposes. <br />By using this website you accept the Cookie monster and the Cookies on this website.</p><button class="btn btn-primary dsa-btn global-alert-btn" type="button">DON&#39;T SHOW AGAIN!</button><button class="btn btn-primary close-btn global-alert-btn" type="button">CLOSE</button>
            </div>
        </div>
    </div>
</section>`
	document.querySelector("body").append(GlobalAlert)
	document.querySelector("body").style.overflowY = "hidden"

	// Remove the global alert forever till the cookies are cleared
	document.querySelector(".dsa-btn").onclick = () => {
		localStorage.setItem("ShowGlobalAlert_v2", true)
		document.querySelector(".global-alert").remove()
		document.querySelector("body").style.overflowY = "scroll"
	}

	// Just remove the global alert for the page
	document.querySelector(".close-btn").onclick = () => {
		document.querySelector(".global-alert").remove()
		document.querySelector("body").style.overflowY = "scroll"
	}
}
