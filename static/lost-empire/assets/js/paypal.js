// JavaScript for PayPal Payment Method

// Get CSRF
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');

let subtotal = 0
let shipping = 4.12
let total_price = 0
let country = ""
let discount_per = 0
let discount_code = ""

// Variables for quantity
let cart_list = []

const cart_data = JSON.parse(localStorage.getItem("cart_list"))
for (let i = 0; i < cart_data.length; i++) {
  // Change the color of the text
  document.querySelector("#cart_status_heading").classList.toggle("text-light", false)
  document.querySelector("#cart_status_heading").classList.toggle("text-info", true)

  // Tell the user the cart items are loading
  document.querySelector("#cart_status_heading").innerHTML = "Loading products..."

  // Set a time out to avoid sending too many requests at once
  setTimeout(() => {
    // Get Product data from REST API
    $.get(`/api?data=product&q=${encodeURIComponent(cart_data[i].product_id)}&v=${encodeURIComponent(cart_data[i].variant_id)}`).done((data) => {
      if (data.STATUS) {
        const html_template = document.createElement("span")
        if (data.product.discount) {
          discount_html = `<span class="sale_price_item">${data.product.compare_at_price}</span>`
        } else {
          discount_html = ``
        }
        html_template.innerHTML = `
          <div class="row d-flex flex-row justify-content-around product-row-${cart_data[i].cart_id} cart-row-holders">
            <div class="col-12 col-sm-6 col-lg-5 col-xl-3 d-flex justify-content-center align-items-start align-content-start">
            <a class="d-flex flex-column justify-content-center align-items-center align-content-center" href="/product?q=${cart_data[i].product_id}">
              <img class="img-fluid cart_product_image card-color-${data.product.card_color}" src="${data.product.images[0]}" width="100%" />
            </a>
            </div>
            <div class="col-12 col-lg-7 col-xl-5">
                <a class="cart_product_link" href="/product?q=${cart_data[i].product_id}">
                    <h4 class="text-break text-light">${data.product.title}</h4>
                </a>
                <h6 class="text-break text-light">${cart_data[i].size}</h6>
                <h6 class="text-break text-light">
                  <i class="fas fa-euro-sign"></i>
                  <strong>${data.product.price}</strong>`+
                  discount_html
                +`</h6>
            </div>
            <div class="col-12 col-xl-4 d-flex flex-column justify-content-center align-items-center align-content-center col_cart_quantity_holder">
                <div class="text-center">
                  <button class="btn btn-dark border rounded minu-btn-quantity item_quantity_btn" id="decrease_quantity" type="button" data-cart_id="${cart_data[i].cart_id}">-</button><input type="text" class="input_counter q-counter-id-${cart_data[i].cart_id}" name="q_counter_id_${cart_data[i].cart_id}" value="${cart_data[i].quantity}" autocomplete="off" minlength="1" maxlength="3" data-cart_id="${cart_data[i].cart_id}" /><button class="btn btn-dark border rounded plus-btn-quantity item_quantity_btn" id="increase_quantity" type="button" data-cart_id="${cart_data[i].cart_id}">+</button></div>
                <div>
                    <p id="item_remove_btn" class="item_remove_btn" data-cart_id="${cart_data[i].cart_id}">Remove Item</p>
                </div>
            </div>
        </div>
        `
        document.querySelector("#hero_1_product_col").append(html_template)
        cart_list.push({
              cart_id: cart_data[i].cart_id,
              product_id: cart_data[i].product_id,
              variant_id: cart_data[i].variant_id,
              quantity: cart_data[i].quantity,
              size: cart_data[i].size,
              product_name: data.product.title,
              price: data.product.price,
              available_units: data.product.max_quantity,
              card_color: data.product.card_color,
              image_0: data.product.images[0].src,
            })
        
        // Enable the checkout button
        if ((cart_data.length - 1) <= i) {
          // Remove the loading products inticator
          document.querySelector("#cart_status_heading").innerHTML = ""

          // Enable the checkout button
          document.querySelector("#checkout_btn").disabled = false

          // Update the current price
          update_price()
    
          // Enable the controls for the Cart products displayed
          update_products()
        }
      }
    })
  }, (2000 * i))
}
//alert(cart_list)
// Control the Prices displayed
update_price = () => {

  // Variables for the PRICEs
  /* let subtotal_HTML = document.querySelector("#subtotal_price > strong")
  let shipping_HTML = document.querySelector("#shipping_price > strong") */
  let total_HTML = document.querySelector("#total_price > strong")

  // A tempurary holder for calculating the subtotal
  let _sum = 0

  // Calculate the total
  for (let i = 0; i < cart_list.length; i++) {

    // Check if there is a discount percentage
    if (discount_per > 0) {
      _sum += (cart_list[i].price * (100 - discount_per) / 100) * cart_list[i].quantity
    } else {
      _sum += cart_list[i].price * cart_list[i].quantity
    }
  }

  total_HTML.innerHTML = (_sum).toFixed(2)
}

// Apply coupon code
/* document.querySelector("#coupon_apply_btn").onclick = () => {
  coupon_code = document.querySelector("#coupon_input")

  let myRegEx  = /[^a-z\d]/i
  let isValid = !(myRegEx.test(coupon_code.value))

  if (isValid && coupon_code.value.length > 5) {
    document.querySelector("#coupon_apply_btn").classList.toggle("btn-primary", false)
    document.querySelector("#coupon_apply_btn").classList.toggle("btn-danger", false)
    document.querySelector("#coupon_apply_btn").classList.toggle("btn-warning", true)
    document.querySelector("#coupon_apply_btn").innerHTML = "APPLYING..."

    $.get(`/api?data=coupon&code=${document.querySelector("#coupon_input").value}`).done((data) => {
      if (data.STATUS && data.VALID) {
        discount_per = data.PERCENT
        setTimeout(() => {
          document.querySelector("#discount_per > strong").innerHTML = `${discount_per}%`
          document.querySelector("#coupon_apply_btn").classList.toggle("btn-success", true)
          document.querySelector("#coupon_apply_btn").classList.toggle("btn-warning", false)
          document.querySelector("#coupon_apply_btn").innerHTML = "GOOD"
          
          // Store the code
          discount_code = coupon_code.value
          
          // Update the current price
          update_price()
        }, 3000)
      } else {
        setTimeout(() => {
          document.querySelector("#discount_per > strong").innerHTML = `0%`
          document.querySelector("#coupon_apply_btn").classList.toggle("btn-danger", true)
          document.querySelector("#coupon_apply_btn").classList.toggle("btn-warning", false)
          document.querySelector("#coupon_apply_btn").innerHTML = "TRY AGAIN"
          
          // Store the code
          discount_code = ""
          
          // Update the current price
          update_price()
        }, 3000)
      }
    })
  } else {
    discount_per = 0
    document.querySelector("#discount_per > strong").innerHTML = `${discount_per}%`
    document.querySelector("#coupon_apply_btn").classList.toggle("btn-primary", false)
    document.querySelector("#coupon_apply_btn").classList.toggle("btn-danger", true)
    document.querySelector("#coupon_apply_btn").innerHTML = "TRY AGAIN"
    
    // Update the current price
    update_price()
  }
} */

update_products = () => {
  // Increase the product quantity being ordered
  document.querySelectorAll("#increase_quantity").forEach(button => {
    button.onclick = () => {
      let quantity_input = document.querySelector(`.q-counter-id-${button.dataset.cart_id}`)

      // Look for the product in the cart and change it's quantity
      for (let i = 0; i < cart_list.length; i++) {

        // Make sure not to go above 999 quantity
        if (cart_list[i].cart_id === parseInt(button.dataset.cart_id) && parseInt(cart_list[i].quantity) < cart_list[i].available_units) {
          cart_list[i].quantity += 1
          quantity_input.value = cart_list[i].quantity
        }
      }

      // Update the cart list
      localStorage.removeItem("cart_list")
      localStorage.setItem("cart_list", JSON.stringify(cart_list))
      
      // Update the current price
      update_price()
    }
  })

  // Decrease the product quantity being ordered
  document.querySelectorAll("#decrease_quantity").forEach(button => {
    button.onclick = () => {
      let quantity_input = document.querySelector(`.q-counter-id-${button.dataset.cart_id}`)

      // Look for the product in the cart and change it's quantity
      for (let i = 0; i < cart_list.length; i++) {

        // Make sure not to go bellow 1 quantity
        if (cart_list[i].cart_id === parseInt(button.dataset.cart_id) && parseInt(cart_list[i].quantity) > 1) {
          cart_list[i].quantity -= 1
          quantity_input.value = cart_list[i].quantity
        }
      }

      // Update the cart list
      localStorage.removeItem("cart_list")
      localStorage.setItem("cart_list", JSON.stringify(cart_list))

      // Update the current price
      update_price()
    }
  })

  // Update the quantity if the quantity value is changed directly
  document.querySelectorAll(".input_counter").forEach(inputField => {
    inputField.onchange = () => {
      let quantity_input = document.querySelector(`.q-counter-id-${inputField.dataset.cart_id}`)

      // Look for the product in the cart and change it's quantity
      for (let i = 0; i < cart_list.length; i++) {
        if (cart_list[i].cart_id === parseInt(inputField.dataset.cart_id)) {

          // Make sure the quantity is not lower than 1
          // And not more than the available units
          if (parseInt(quantity_input.value) < 1) {
            cart_list[i].quantity = 1
          } else if (parseInt(quantity_input.value) > cart_list[i].available_units) {
            cart_list[i].quantity = cart_list[i].available_units
          } else {
            cart_list[i].quantity = parseInt(quantity_input.value)
          }

          // Add the actual quantity to the input field
          quantity_input.value = cart_list[i].quantity

        }
      }

      // Update the cart list
      localStorage.removeItem("cart_list")
      localStorage.setItem("cart_list", JSON.stringify(cart_list))

      // Update the current price
      update_price()
    }
  })

  // Remove the product from the cart
  document.querySelectorAll(".item_remove_btn").forEach(button => {
    button.onclick = () => {
      const _tmp_list = []

      // Remove the product from the cart
      for (let i = 0; i < cart_list.length; i++) {
        if (cart_list[i].cart_id != parseInt(button.dataset.cart_id)) {
          _tmp_list.push({...cart_list[i]})
        }
      }

      // Update the cart list
      cart_list = _tmp_list

      localStorage.removeItem("cart_list") // Remove the current Cart list
      localStorage.setItem("cart_list", JSON.stringify(cart_list)) // Add new Cart list

      // Remove from the UI
      document.querySelector(`.product-row-${button.dataset.cart_id}`).remove()

      // Update the current price
      update_price()

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
    }
  })
}

// Check if the checkout button is present
if (document.querySelector("#checkout_btn")) {

  // Check if the Checkout button was pressed
  document.querySelector("#checkout_btn").onclick = () => {

    // Create the query for the cart
    let query = ""
    for (let i = 0; i < cart_list.length; i++) {
      query += `${cart_list[i].variant_id}:${cart_list[i].quantity},`
    }

    // Go to the checkout page on Shopify
    location.href = `http://lost-empire-2020.myshopify.com/cart/${query}`
  }
}

setTimeout(() => {
  // Initialize the prices
  update_price()
}, 500)
