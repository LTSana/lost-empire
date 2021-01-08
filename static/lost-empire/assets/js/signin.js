// JavaScript for Sign In page

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
})

// reCAPTCHA for Signin form
grecaptcha.ready(function() {
	$('#signin_form').submit(function(e){
		var form = this;
		e.preventDefault()
		grecaptcha.execute(document.querySelector("#site_key").value, {action: 'signin'}).then(function(token) {
			$('#recaptcha').val(token)
			form.submit()
		});
	})
});

// reCAPTCHA for Signup form
grecaptcha.ready(function() {
	$('#signup_form').submit(function(e){
		var form = this;
		e.preventDefault()
		grecaptcha.execute(document.querySelector("#site_key").value, {action: 'signup'}).then(function(token) {
			$('#recaptcha').val(token)
			form.submit()
		});
	})
});

// reCAPTCHA for forgot form
grecaptcha.ready(function() {
	$('#forgotpwd_form').submit(function(e){
		var form = this;
		e.preventDefault()
		grecaptcha.execute(document.querySelector("#site_key").value, {action: 'forgotpwd'}).then(function(token) {
			$('#recaptcha').val(token)
			form.submit()
		});
	})
});

