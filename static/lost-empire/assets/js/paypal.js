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

let _cart = JSON.parse(localStorage.getItem("cart_list"))

//const product_data = null
//const request = new XMLHttpRequest()
//request.open("GET", "/api?data=products")
//const data = new FormData()
//data.append("csrfmiddlewaretoken", csrftoken)
//data.append("cart_list", _cart)
//request.send(data)


// Variables for quantity
let cart_list = []

for (let i = 0; i < _cart.length; i++) {
  cart_list.push({
    cart_id: _cart[i].cart_id,
    product_id: _cart[i].product_id,
    quantity: _cart[i].quantity,
    size: _cart[i].size,
    product_name: "Blue-G",
    price: 12.54,
    available_units: 684
  })
}

for(let i = 0; i < cart_list.length; i++) {
  const html_template = document.createElement("span")
  html_template.innerHTML = `
    <div class="row d-flex flex-row justify-content-around product-row-${cart_list[i].cart_id}">
      <div class="col-12 col-sm-6 col-lg-5 col-xl-3 d-flex justify-content-center align-items-start align-content-start">
      <img class="img-fluid cart_product_image" src="extras/Jacket-Design.png" width="100%" />
      </div>
      <div class="col-12 col-lg-7 col-xl-5">
          <a class="cart_product_link" href="/product.html?q=${cart_list[i].product_id}">
              <h4 class="text-break text-light">${cart_list[i].product_name}</h4>
          </a>
          <h6 class="text-break text-light">${cart_list[i].size}</h6>
          <h6 class="text-break text-light">
            <i class="fas fa-euro-sign"></i>
            <strong>12.54</strong>
          </h6>
      </div>
      <div class="col-12 col-xl-4 d-flex flex-column justify-content-center align-items-center align-content-center col_cart_quantity_holder">
          <div class="text-center">
            <button class="btn btn-dark border rounded minu-btn-quantity item_quantity_btn" id="decrease_quantity" type="button" data-cart_id="${cart_list[i].cart_id}">-</button><input type="text" class="input_counter q-counter-id-${cart_list[i].cart_id}" name="q_counter_id_${cart_list[i].cart_id}" value="${cart_list[i].quantity}" autocomplete="off" minlength="1" maxlength="3" data-cart_id="${cart_list[i].cart_id}" /><button class="btn btn-dark border rounded plus-btn-quantity item_quantity_btn" id="increase_quantity" type="button" data-cart_id="${cart_list[i].cart_id}">+</button></div>
          <div>
              <p id="item_remove_btn" class="item_remove_btn" data-cart_id="${cart_list[i].cart_id}">Remove Item</p>
          </div>
      </div>
  </div>
  `
  document.querySelector("#hero_1_product_col").append(html_template)
}

// Control the Prices displayed
update_price = () => {

  // Variables for the PRICEs
  let subtotal_HTML = document.querySelector("#subtotal_price > strong")
  let shipping_HTML = document.querySelector("#shipping_price > strong")
  let total_HTML = document.querySelector("#total_price > strong")

  // A tempurary holder for calculating the subtotal
  let _sum = 0

  // Calculate the total
  for (let i = 0; i < cart_list.length; i++) {
    _sum += cart_list[i].price * cart_list[i].quantity
  }

  // Add the sum of all the cart products to subtotal
  subtotal = _sum

  // If there's no subtotal remove shipping costs
  if (subtotal <= 0) {
    shipping = 0
  } else {
    shipping = 4.12
  }

  // Calculate the quatity of each item and it's price
  subtotal_HTML.innerHTML = (subtotal).toFixed(2)

  // Get the location of the shipping and calculate the price
  shipping_HTML.innerHTML = (shipping).toFixed(2)

  // Add everything to the total price
  total_price = subtotal + shipping
  total_HTML.innerHTML = (total_price).toFixed(2)
}

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
      if (!cart_list[i].cart_id === parseInt(button.dataset.cart_id)) {
        _tmp_list.push(...cart_list[i])
      }
    }

    cart_list = _tmp_list

    localStorage.removeItem("cart_list") // Remove the current Cart list
    localStorage.setItem("cart_list", JSON.stringify(cart_list)) // Add new Cart list

    // Remove from the UI
    document.querySelector(`.product-row-${button.dataset.cart_id}`).remove()

    // Update the current price
    update_price()
	}
})

setTimeout(() => {
  paypal.Buttons({
    style: {
      shape: 'pill',
      color: 'black',
      layout: 'vertical',
      label: 'checkout',  
    },
      createOrder: function(data, actions) {
        let price0 = (total_price).toFixed(2)
  
        // This function sets up the details of the transaction, including the amount and line item details.
        return actions.order.create({
          purchase_units: [{
            amount: {
              value: price0
            }
          }]
        });
      },
      onApprove: function(data, actions) {
        // This function captures the funds from the transaction.
        
        // Authorize the transaction
        actions.order.authorize().then(function(authorization) {
  
          // Get the authorization id
          var authorizationID = authorization.purchase_units[0]
            .payments.authorizations[0].id
          
          alert(`AuthorizationID: ${authorizationID}`)
  
          location.replace("/transactions/complete.html")
        })
      }
    }).render('#paypal-button-container');
    //This function displays Smart Payment Buttons on your web page.
}, 700)

setTimeout(() => {
  // Initialize the prices
  update_price()
}, 500)
