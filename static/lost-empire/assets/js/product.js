// JavaScript for Product page to add products to the cart

document.addEventListener("DOMContentLoaded", () => {

	// For product size selection
	if (document.querySelectorAll(".product_size_btn")) {
		document.querySelectorAll(".product_size_btn").forEach(button => {
			button.onclick = () => {
	
				// Set the selected Size to active
				button.classList.toggle("active", true)
	
				// Set the others to deactive if they where active
				document.querySelectorAll(".product_size_btn").forEach(_button => {
					if (button.dataset.size != _button.dataset.size) {
						_button.classList.toggle("active", false)
					}
				})
	
				document.querySelector(".add_to_cart_btn").classList.toggle("disabled", false)
				document.querySelector(".add_to_cart_btn").disabled = false
			}
		})
	}

	// For adding product to the cart
	document.querySelector(".add_to_cart_btn").onclick = () => {
		
		// Set to false unless there is a size selected
		_prodcut_size_selected = false

		document.querySelectorAll(".product_size_btn").forEach(button => {
			// Set to true if there is are any sizes to select from
			_prodcut_size_selected = true

			// Check which Size button is selected
			if (button.classList.contains("active")) {
				
				// Check if the Size is available
				if (button.dataset.size) {

					// Get the products ID
					let product_id = document.querySelector("#product_ID").value
					
					// Check and make sure that the product ID is present
					if (product_id) {
						// Check if the cart list already exists in the local storage
						if (localStorage.getItem("cart_list")) {

							let new_product = true
							let _i = 0
							const cart_list = JSON.parse(localStorage.getItem("cart_list"))

							// Check if the product is already in the cart and has the same size
							for (let i = 0; i < cart_list.length; i++) {
								if (cart_list[i].product_id === product_id && cart_list[i].size === button.dataset.size) {
									cart_list[i].quantity += 1
									new_product = false
								}
								_i++
							}

							// If the product isn't in the cart add it to it
							if (new_product) {
								cart_list.push({
									cart_id: _i,
									product_id: product_id,
									quantity: 1,
									size: button.dataset.size,
									variant_id: button.dataset.variant_id,
								})
							}

							// Update the local Storage cart
							localStorage.setItem("cart_list", JSON.stringify(cart_list))

						} else {
							let cart_list = [{
								cart_id: 0,
								product_id: product_id,
								quantity: 1,
								size: button.dataset.size,
								variant_id: button.dataset.variant_id,
							}]
							
							// Initialize cart list
							localStorage.setItem("cart_list", JSON.stringify(cart_list))
						}
						location.href = "/cart"
					}
				} else {
					alert("Please select a size to add to cart.")
				}
			}
		})

		// If there aren't any sizes for this Item
		if (!_prodcut_size_selected) {
			// Get the products ID
			let product_id = document.querySelector("#product_ID").value
			let variant_id = document.querySelector(".product_size_btn").dataset.variant_id
					
			// Check and make sure that the product ID is present
			if (product_id) {
				// Check if the cart list already exists in the local storage
				if (localStorage.getItem("cart_list")) {

					let new_product = true
					let _i = 0
					const cart_list = JSON.parse(localStorage.getItem("cart_list"))

					// Check if the product is already in the cart and has the same size
					for (let i = 0; i < cart_list.length; i++) {
						if (cart_list[i].product_id === product_id) {
							cart_list[i].quantity += 1
							new_product = false
						}
						_i++
					}

					// If the product isn't in the cart add it to it
					if (new_product) {
						cart_list.push({
							cart_id: _i,
							product_id: product_id,
							quantity: 1,
							size: "n/a",
							variant_id: variant_id,
						})
					}

					// Update the local Storage cart
					localStorage.setItem("cart_list", JSON.stringify(cart_list))

				} else {
					let cart_list = [{
						cart_id: 0,
						product_id: product_id,
						quantity: 1,
						size: "n/a",
						variant_id: variant_id,
					}]
					
					// Initialize cart list
					localStorage.setItem("cart_list", JSON.stringify(cart_list))
				}
				location.href = "/cart"
			}
		}
	}

	// For switching big product image to the mini image selected
	document.querySelectorAll(".mini_product_image").forEach(image_holder => {
		image_holder.onclick = () => {
			document.querySelector(".big_product_image").src = image_holder.src
			document.querySelectorAll(".mini_product_image").forEach(image_holder2 => {
				image_holder2.classList.toggle("active", false)
			})
			image_holder.classList.toggle("active", true)
		}
	})
})
