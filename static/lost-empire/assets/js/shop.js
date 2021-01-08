
// Controls the Margin Top from Nav bar for Hero 1
//let navbox = document.querySelector(".navigation-clean-search")
//let box = document.querySelector("#hero_0")
//box.style.marginBottom = "60px"

document.addEventListener("DOMContentLoaded", () => {

	// Hide the filter options if the screen size is too small
	if (screen.width <= 767) {

		// Filter Size
		document.querySelector("#filter_size_option_list").classList.toggle("d-none", true)
		document.querySelector("#toggle_filter_size_icon").classList.toggle("fa-plus-square", true)
		document.querySelector("#toggle_filter_size_icon").classList.toggle("fa-minus-square", false)

		// Filter Type
		document.querySelector("#filter_type_option_list").classList.toggle("d-none", true)
		document.querySelector("#toggle_filter_type_icon").classList.toggle("fa-plus-square", true)
		document.querySelector("#toggle_filter_type_icon").classList.toggle("fa-minus-square", false)

		// Filter Brands
		document.querySelector("#filter_brand_option_list").classList.toggle("d-none", true)
		document.querySelector("#toggle_filter_brand_icon").classList.toggle("fa-plus-square", true)
		document.querySelector("#toggle_filter_brand_icon").classList.toggle("fa-minus-square", false)
	}

	// Filter Size
	document.querySelector("#toggle_filter_size").onclick = () => {
		if (document.querySelector("#filter_size_option_list").classList.toggle("d-none")) {
			document.querySelector("#filter_size_option_list").classList.toggle("d-none", true)
			document.querySelector("#toggle_filter_size_icon").classList.toggle("fa-plus-square", true)
			document.querySelector("#toggle_filter_size_icon").classList.toggle("fa-minus-square", false)
		} else {
			document.querySelector("#filter_size_option_list").classList.toggle("d-none", false)
			document.querySelector("#toggle_filter_size_icon").classList.toggle("fa-plus-square", false)
			document.querySelector("#toggle_filter_size_icon").classList.toggle("fa-minus-square", true)
		}
	}

	// Filter Type
	document.querySelector("#toggle_filter_type").onclick = () => {
		if (document.querySelector("#filter_type_option_list").classList.toggle("d-none")) {
			document.querySelector("#filter_type_option_list").classList.toggle("d-none", true)
			document.querySelector("#toggle_filter_type_icon").classList.toggle("fa-plus-square", true)
			document.querySelector("#toggle_filter_type_icon").classList.toggle("fa-minus-square", false)
		} else {
			document.querySelector("#filter_type_option_list").classList.toggle("d-none", false)
			document.querySelector("#toggle_filter_type_icon").classList.toggle("fa-plus-square", false)
			document.querySelector("#toggle_filter_type_icon").classList.toggle("fa-minus-square", true)
		}
	}

	// Filter Brands
	document.querySelector("#toggle_filter_brand").onclick = () => {
		if (document.querySelector("#filter_brand_option_list").classList.toggle("d-none")) {
			document.querySelector("#filter_brand_option_list").classList.toggle("d-none", true)
			document.querySelector("#toggle_filter_brand_icon").classList.toggle("fa-plus-square", true)
			document.querySelector("#toggle_filter_brand_icon").classList.toggle("fa-minus-square", false)
		} else {
			document.querySelector("#filter_brand_option_list").classList.toggle("d-none", false)
			document.querySelector("#toggle_filter_brand_icon").classList.toggle("fa-plus-square", false)
			document.querySelector("#toggle_filter_brand_icon").classList.toggle("fa-minus-square", true)
		}
	}

	// Checkbox module system for all the checkboxes
	checkbox_system = (checkbox, filter_option) => {
		checkbox.onclick = () => {
			// Check if the box is checkec or not
			if (checkbox.checked) {

				// Get the URL's parameters
				const queryString = window.location.search
				const URLParam = new URLSearchParams(queryString)

				try {
					// Convert the Size parameter and convert it into a list we can use
					let _list = JSON.parse(URLParam.get(`${filter_option}`))

					// Add new size to the list
					_list.push(checkbox.dataset[filter_option])

					// Convert the list to a string for the URL
					URLParam.set(`${filter_option}`, JSON.stringify(_list))
					URLParam.toString() // Make it URL friendly

					// Redirect to those parameters given
					location.href = `?${URLParam}`
				} catch(err) {
					// Reset List
					let _list = []

					// Add new size to the list
					_list.push(checkbox.dataset[filter_option])

					// Convert the list to a string for the URL
					URLParam.set(`${filter_option}`, JSON.stringify(_list))
					URLParam.toString() // Make it URL friendly

					// Redirect to those parameters given
					location.href = `?${URLParam}`
				}

			} else {
				
				// Get the URL's parameters
				const queryString = window.location.search
				const URLParam = new URLSearchParams(queryString)

				// Convert the Size parameter and convert it into a list we can use
				let _list = JSON.parse(URLParam.get(`${filter_option}`))

				// Remove the size from the list
				const _tmp_list = []
				for (let i = 0; i < _list.length; i++) {
					if (_list[i] != checkbox.dataset[filter_option]) {
						_tmp_list.push(_list[i])
					}
				}
				_list = _tmp_list

				// Convert the list to a string for the URL
				URLParam.set(`${filter_option}`, JSON.stringify(_list))
				URLParam.toString() // Make it URL friendly

				// Redirect to those parameters given
				location.href = `?${URLParam}`
			}
		}

		// Mark the boxes as true if the in the list
		const _queryString = window.location.search
		let _URLParam = new URLSearchParams(_queryString)
		if (_URLParam.get(`${filter_option}`)) {

			// Catch Error if JSON gives an error when converting string to list
			try {
				const _current_URL = JSON.parse(_URLParam.get(`${filter_option}`))
				document.querySelector(`#filter_${filter_option}_counter`).innerHTML = _current_URL.length
				for (let i = 0; i < _current_URL.length; i++) {
					if (checkbox.dataset[filter_option] === _current_URL[i]) {
						checkbox.checked = true
					}
				}
			} catch(err) {
				// Get the URL's parameters
				const queryString = window.location.search
				const URLParam = new URLSearchParams(queryString)

				// Remove the size from the list
				let _list = []

				// Convert the list to a string for the URL
				URLParam.set(`${filter_option}`, JSON.stringify(_list))
				URLParam.toString() // Make it URL friendly

				// Redirect to those parameters given
				location.href = `?${URLParam}`
			}
		}
	}

	document.querySelectorAll(".checkbox-sizes").forEach(checkbox => {
		// Checkbox System for processing all checkboxes
		checkbox_system(checkbox, "size")
	})

	document.querySelectorAll(".checkbox-type").forEach(checkbox => {
		// Checkbox System for processing all checkboxes
		checkbox_system(checkbox, "type")
	})

	document.querySelectorAll(".checkbox-brand").forEach(checkbox => {
		// Checkbox System for processing all checkboxes
		checkbox_system(checkbox, "brand")
	})
})
