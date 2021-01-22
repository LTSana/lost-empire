// JavaScript for Sign In page

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

document.addEventListener("DOMContentLoaded", () => {

	// Toggles for Signin/Signup/Forgot Password forms

	// Toggle Signing Up
	document.querySelector("#signup_toggle").onclick = () => {
		document.querySelector("#signin_form").classList.toggle("d-none", true)
		document.querySelector("#signup_form").classList.toggle("d-none", false)
	}
	
	// Toggle to close the Signup form and toggle Sign In
	document.querySelector("#signin_toggle").onclick = () => {
		document.querySelector("#signin_form").classList.toggle("d-none", false)
		document.querySelector("#signup_form").classList.toggle("d-none", true)
	}

	// Toggle forgot Password
	document.querySelector("#forgot_toggle").onclick = () => {
		document.querySelector("#signin_form").classList.toggle("d-none", true)
		document.querySelector("#forgotpwd_form").classList.toggle("d-none", false)
	}

	// Toggle close forgot Password and toggle Sign In
	document.querySelector("#signin_toggle-2").onclick = () => {
		document.querySelector("#signin_form").classList.toggle("d-none", false)
		document.querySelector("#forgotpwd_form").classList.toggle("d-none", true)
	}

	// Check email address
	document.querySelector("#email_field").onchange = () => {
		const request = new XMLHttpRequest()
		request.open("POST", "/signupCheck")
		const data = new FormData()
		data.append("csrfmiddlewaretoken", csrftoken)
		data.append("register_check", true)
		data.append("email", document.querySelector("#email_field").value)
		request.send(data)
		request.onreadystatechange = () => {
			if (request.readyState === 4 && request.status === 200) {
				if (JSON.parse(request.response)["STATUS"]) {
					
					if (JSON.parse(request.response)["EMAIL"] === "usable_true") {
						// If the email is usable notify the user
						document.querySelector(".email_status_check").innerHTML = JSON.parse(request.response)["MESSAGE"]
						document.querySelector(".email_status_check").style.color = "green"
						document.querySelector(".email_status_check").classList.toggle("text-danger", false)
						document.querySelector("#email_field").style.borderColor = "green"

					} else if (JSON.parse(request.response)["EMAIL"] === "usable_false") {
						// If the email is usable notify the user
						document.querySelector(".email_status_check").innerHTML = JSON.parse(request.response)["MESSAGE"]
						document.querySelector(".email_status_check").classList.toggle("text-danger", true)
						document.querySelector("#email_field").style.borderColor = "red"

					} else if (JSON.parse(request.response)["EMAIL"]) {
						// If the server sends back any error messages
						document.querySelector(".email_status_check").innerHTML = JSON.parse(request.response)["MESSAGE"]
						document.querySelector(".email_status_check").classList.toggle("text-danger", true)
						document.querySelector("#email_field").style.borderColor = "red"

					}
				}
			}
		}
	}
})

// Toggle Password visibility
document.querySelector("#pwd_visible_toggle").onclick = () => {
	if (document.querySelector("#input_fields_pwd").type === "password") {
		document.querySelector("#input_fields_pwd").type = "text"
		document.querySelector("#pwd_visible_toggle").classList.toggle("fa-eye", true)
		document.querySelector("#pwd_visible_toggle").classList.toggle("fa-eye-slash", false)
	} else {
		document.querySelector("#input_fields_pwd").type = "password"
		document.querySelector("#pwd_visible_toggle").classList.toggle("fa-eye", false)
		document.querySelector("#pwd_visible_toggle").classList.toggle("fa-eye-slash", true)
	}
}

document.querySelector("#cpwd_visible_toggle").onclick = () => {
	if (document.querySelector("#input_fields_cpwd").type === "password") {
		document.querySelector("#input_fields_cpwd").type = "text"
		document.querySelector("#cpwd_visible_toggle").classList.toggle("fa-eye", true)
		document.querySelector("#cpwd_visible_toggle").classList.toggle("fa-eye-slash", false)
	} else {
		document.querySelector("#input_fields_cpwd").type = "password"
		document.querySelector("#cpwd_visible_toggle").classList.toggle("fa-eye", false)
		document.querySelector("#cpwd_visible_toggle").classList.toggle("fa-eye-slash", true)
	}
}

grecaptcha.ready(function() {

	// reCAPTCHA for Signin form
	$('#signin_form').submit(function(e){
		var form = this;
		e.preventDefault()
		grecaptcha.execute(document.querySelector("#site_key").value, {action: 'signin'}).then(function(token) {
			$('#recaptcha').val(token)
			form.submit()
		});
	})

	// reCAPTCHA for Signup form
	$('#signup_form').submit(function(e){
		var form = this;
		e.preventDefault()
		grecaptcha.execute(document.querySelector("#site_key-1").value, {action: 'signup'}).then(function(token) {
			$('#recaptcha-1').val(token)
			form.submit()
		});
	})

	// reCAPTCHA for forgot form
	$('#forgotpwd_form').submit(function(e){
		var form = this;
		e.preventDefault()
		grecaptcha.execute(document.querySelector("#site_key-2").value, {action: '#forgotpwd'}).then(function(token) {
			$('#recaptcha-2').val(token)
			form.submit()
		});
	})
});
