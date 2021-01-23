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
  // Set a time out to avoid sending too many requests at once
  setTimeout(() => {
    // Get Product data from REST API
    $.get(`/api?data=product&q=${encodeURIComponent(cart_data[i].product_id)}`).done((data) => {
      if (data.STATUS) {
        const html_template = document.createElement("span")
        if (data.product.discount) {
          discount_html = `<span class="sale_price_item">${data.product.old_price}</span>`
        } else {
          discount_html = ``
        }
        html_template.innerHTML = `
          <div class="row d-flex flex-row justify-content-around product-row-${cart_data[i].cart_id} cart-row-holders">
            <div class="col-12 col-sm-6 col-lg-5 col-xl-3 d-flex justify-content-center align-items-start align-content-start">
            <a class="d-flex flex-column justify-content-center align-items-center align-content-center" href="/product?q=${cart_data[i].hash_key}">
              <img class="img-fluid cart_product_image card-color-${data.product.card_color}" src="${data.product.image_0}" width="100%" />
            </a>
            </div>
            <div class="col-12 col-lg-7 col-xl-5">
                <a class="cart_product_link" href="/product?q=${cart_data[i].product_id}">
                    <h4 class="text-break text-light">${data.product.name}</h4>
                </a>
                <h6 class="text-break text-light">${cart_data[i].size}</h6>
                <h6 class="text-break text-light">
                  <i class="fas fa-euro-sign"></i>
                  <strong>${(data.product.price).toFixed(2)}</strong>`+
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
              quantity: cart_data[i].quantity,
              size: cart_data[i].size,
              product_name: data.product.name,
              price: data.product.price,
              available_units: 999,
              card_color: data.product.card_color,
              image_0: data.product.image_0,
            })
        
        // Update the current price
        update_price()
  
        // Enable the controls for the Cart products displayed
        update_products()
      }
    })
  }, (2000 * i))
}
//alert(cart_list)
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

    // Check if there is a discount percentage
    if (discount_per > 0) {
      _sum += (cart_list[i].price * (100 - discount_per) / 100) * cart_list[i].quantity
    } else {
      _sum += cart_list[i].price * cart_list[i].quantity
    }
  }

  // Add the sum of all the cart products to subtotal
  subtotal = _sum

  // If there's no subtotal remove shipping costs
  if (subtotal <= 0) {
    shipping = 0
    
    // If the total is 0 disable the PayPal butttons
    document.querySelector("#paypal-button-container").style.pointerEvents = "none";
    document.querySelector("#paypal-button-container").style.opacity = "0.5";

  } else {

    // Update the shipping price to the country that has been selected
    const country_selection = document.querySelector("#shipping_country").value
    if (country_selection) {
      
      country = document.querySelector(`#country-${country_selection}`).dataset.country
      const continent = document.querySelector(`#country-${country_selection}`).dataset.continent
      if (["EU", "NA"].includes(continent)) {
        // Update the shipping price
        shipping = 21.34
      } else {
        shipping = 23.48
      }
    }
  }

  // Calculate the quatity of each item and it's price
  subtotal_HTML.innerHTML = (subtotal).toFixed(2)

  // Get the location of the shipping and calculate the price
  shipping_HTML.innerHTML = (shipping).toFixed(2)

  // Add everything to the total price
  total_price = subtotal + shipping

  total_HTML.innerHTML = (total_price).toFixed(2)
}

// Apply coupon code
document.querySelector("#coupon_apply_btn").onclick = () => {
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
}

// Enable PayPal checkout when the CheckBox for the Privacy and Terms is checked
document.querySelector("#shipping_country").onchange = () => {
  if (document.querySelector("#shipping_country").value) {

    // Enable the PayPal buttons
    document.querySelector("#paypal-button-container").style.pointerEvents = "auto";
    document.querySelector("#paypal-button-container").style.opacity = "1";

    // Update the current price
    update_price()

  } else {
    document.querySelector("#paypal-button-container").style.pointerEvents = "none";
    document.querySelector("#paypal-button-container").style.opacity = "0.5";

    // Update the current price
    update_price()
  }
}

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

        // Prevent the user from leaving the page.
        window.onbeforeunload = () => {
          return "Don't leave. Your order is being processed.";
        };

        // Lock the cart
        document.querySelector("#hero_1_product_col").style.pointerEvents = "none";
        document.querySelector("#hero_1_product_col").style.opacity = "0.5";
  
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
        
        $.post("cart/pptc", {"csrfmiddlewaretoken": csrftoken, 
                              "order_id": data.orderID, 
                              "cart_data": localStorage.getItem("cart_list"),
                              "country": country,
                              "coupon_code": document.querySelector("#coupon_input").value
                            }).done(
            (data) => {
              
              // Used to deactivate the dont leave page warning
              window.onbeforeunload = () => {
                // blank function do nothing
              }

              // Check if the process went well
              if (data.STATUS) {
                if (data.TC) {
                  localStorage.removeItem("cart_list")
                  location.href = `/cart/tc?order=${data.order_id}`
                } else {
                  location.href = `/cart/tc?er=${data.error_message}`
                }
              } else {
                location.href = `/cart/tc?er=Failed with no error message`
              }
            }
          )
      },
      onError: err => {
        alert("An error in the payment happened. \nPlease re-try.")
        console.error('error from the onError callback', err);
      }
    }).render('#paypal-button-container');
    //This function displays Smart Payment Buttons on your web page.
}, 700)

setTimeout(() => {
  // Initialize the prices
  update_price()
}, 500)
