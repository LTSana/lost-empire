from django import forms
from django.core.validators import RegexValidator, validate_email
import emoji
import json

# Import PayPal API
from .utils.paypal_api import GetOrder

class SigninForm(forms.Form):
	""" Form for signing in """

	email = forms.EmailField(
		max_length=1600,
		min_length=1,
		label="E-mail address",
		required=True,
		error_messages={
			"required": "E-mail address is required! Please fill in the E-mail Address...",
			"max_length": "E-mail address is too long!",
			"min_length": "E-mail address is too short!",
			"invalid": "E-mail address is invalid! Make sure there isn't any special characters that can cause issues."
		},
		validators=[validate_email]
		)
	
	pwd = forms.CharField(
		max_length=64,
		min_length=8,
		label="Password",
		required=True,
		error_messages={
			"required": "Password is required!",
			"max_length": "Password is too long!",
			"min_length": "Password is too short!",
			"invalid": "Password is invalid!"
		}
		)

class SignupForm(forms.Form):
	""" Sign Up form to validated user input """

	first_name = forms.CharField(
		required=True,
		max_length=1600,
		min_length=1,
		help_text="First name needs to be longer then 1 char or less then 1600",
		label="First name",
		error_messages={
			"required": "First name is missing... Please add a First name.",
			"min_length": "First name is too short.. Please make it longer.",
			"max_length": "First name is too long... Please make it shorter.",
			"invalid": "First name cannot be used! Invalid charater/s."
		}
	)

	last_name = forms.CharField(
		required=True,
		max_length=1600,
		min_length=1,
		help_text="Last name needs to be longer then 1 char or less then 1600",
		label="Last name",
		error_messages={
			"required": "Last name is missing... Please add a Last name.",
			"min_length": "Last name is too short.. Please make it longer.",
			"max_length": "Last name is too long... Please make it shorter.",
			"invalid": "Last name cannot be used! Invalid charater/s."
		}
	)

	email = forms.EmailField(
		max_length=254,
		min_length=2,
		required=True,
		help_text="Email address needs to be longer then 2 and less then 254.",
		label="E-mail address",
		error_messages={
			"required": "E-mail address is missing... Please add a E-mail address.",
			"min_length": "E-mail address is too short.. Please make it longer.",
			"max_length": "E-mail address is too long... Please make it shorter.",
			"invalid": "E-mail address cannot be used! Try another one."
		},
		validators=[validate_email]
	)

	pwd = forms.CharField(
		max_length=128,
		min_length=8,
		required=True,
		help_text="Password needs to be 8 or 128 characters long",
		label="Password",
		error_messages={
			"require": "Password is missing... Please provide a strong password!",
			"min_length": "Password is too short! Please make your password 8 - 128 characters long.",
			"max_length": "Password is too long! Please make your password 8 - 128 characters long.",
			"invalid": "Password is invalid! Try a different one..."
		},
		widget=forms.PasswordInput(),
	)

	cpwd = forms.CharField(
		max_length=128,
		min_length=8,
		required=True,
		help_text="Confirm Password needs to be 8 or 128 characters long",
		label="Confirm Password",
		error_messages={
			"require": "Confirm Password is missing... Please provide a strong password!",
			"min_length": "Confirm Password is too short! Please make your password 8 - 128 characters long.",
			"max_length": "Confirm Password is too long! Please make your password 8 - 128 characters long.",
			"invalid": "Confirm Password is invalid! Try a different one..."
		},
		widget=forms.PasswordInput(),
	)

	def clean(self):

		cleaned_data = super(SignupForm, self).clean()
		new_password = cleaned_data.get("pwd")
		confirm_password = cleaned_data.get("cpwd")

		if new_password != confirm_password:
			self.add_error("cpwd", "Password and Confirm Password do not match!")

		# Make sure the aren't any emojis in the password
		if emoji.emoji_count(new_password):
			self.add_error("pwd", "Your password cannot contain any emojis. 💥BOOOM!!!...")

		return cleaned_data

class EmailCheckForm(forms.Form):
	""" Used for the sign up email check """

	email = forms.EmailField(
		max_length=254,
		min_length=2,
		required=True,
		help_text="Email address needs to be longer then 2 and less then 254.",
		label="E-mail address",
		error_messages={
			"required": "EMPTY BOX",
			"min_length": "TOO SHORT",
			"max_length": "TOO LONG",
			"invalid": "INVALID"
		},
		validators=[validate_email]
	)

class AccountSecurityForm(forms.Form):
	""" Used for changing the account password in account security"""

	opwd = forms.CharField(
		max_length=128,
		min_length=8,
		required=True,
		help_text="Password needs to be 8 or 128 characters long",
		label="Password",
		error_messages={
			"require": "Password is missing... Please provide a strong password!",
			"min_length": "Password is too short! Please make your password 8 - 128 characters long.",
			"max_length": "Password is too long! Please make your password 8 - 128 characters long.",
			"invalid": "Password is invalid! Try a different one..."
		},
		widget=forms.PasswordInput()
	)

	npwd = forms.CharField(
		max_length=128,
		min_length=8,
		required=True,
		help_text="Password needs to be 8 or 128 characters long",
		label="Password",
		error_messages={
			"require": "Password is missing... Please provide a strong password!",
			"min_length": "Password is too short! Please make your password 8 - 128 characters long.",
			"max_length": "Password is too long! Please make your password 8 - 128 characters long.",
			"invalid": "Password is invalid! Try a different one..."
		},
		widget=forms.PasswordInput()
	)

	cpwd = forms.CharField(
		max_length=128,
		min_length=8,
		required=True,
		help_text="Password needs to be 8 or 128 characters long",
		label="Password",
		error_messages={
			"require": "Password is missing... Please provide a strong password!",
			"min_length": "Password is too short! Please make your password 8 - 128 characters long.",
			"max_length": "Password is too long! Please make your password 8 - 128 characters long.",
			"invalid": "Password is invalid! Try a different one..."
		},
		widget=forms.PasswordInput()
	)

	def clean(self):

		cleaned_data = super(AccountSecurityForm, self).clean()
		old_password = cleaned_data.get("opwd")
		new_password = cleaned_data.get("npwd")
		confirm_password = cleaned_data.get("cpwd")

		# Check if the new password and confirm password match
		if new_password != confirm_password:
			self.add_error("cpwd", "New Password and Confirm Password do not match!")

		# Make sure the new password and old password aren't the same
		if new_password == old_password:
			self.add_error("npwd", "Your new password is the same as the old one. We won't change it. Try a different password.")

		# Make sure the aren't any emojis in the password
		if emoji.emoji_count(new_password):
			self.add_error("npwd", "Your password cannot contain any emojis.")

		return cleaned_data

class ShopForm(forms.Form):
	""" Used for the shop """

	search = forms.CharField(
		required=False,
		max_length=1600,
		help_text="Search needs to be less then 1600 characters",
		label="Search",
		error_messages={
			"required": "Search is missing...",
			"max_length": "Search is too long... Please make it shorter.",
			"invalid": "Search cannot be used! Invalid charater/s."
		}
	)
	
	size = forms.CharField(
		required=False,
		help_text="Size list from the Shop filter",
		label="Size"
	)

	category = forms.CharField(
		required=False,
		help_text="Category list from the Shop filter",
		label="Category"
	)

	brand = forms.CharField(
		required=False,
		help_text="Brand list from the Shop filter",
		label="Brand"
	)

	page = forms.IntegerField(
		required=False,
		help_text="Brand list from the Shop filter",
		label="Brand"
	)

	def clean(self):
		cleaned_data = super(ShopForm, self).clean()
		size = cleaned_data.get("size")
		category = cleaned_data.get("category")
		brand = cleaned_data.get("brand")
		page = cleaned_data.get("page")
		
		# Check if the size list is available and check to see if we can convert it to a list from a string using 'json'
		if size:
			try:
				json.loads(size)
			except json.JSONDecodeError:
				self.add_error("size", "The size list is broken.")

		# Check if the category list is available and check to see if we can convert it to a list from a string using 'json'
		if category:
			try:
				json.loads(category)
			except json.JSONDecodeError:
				self.add_error("category", "The category list is broken.")

		# Check if the brand list is available and check to see if we can convert it to a list from a string using 'json'
		if brand:
			try:
				json.loads(brand)
			except json.JSONDecodeError:
				self.add_error("brand", "The brand list is broken.")

		# Check if the page number is a int
		if page and not isinstance(page, int):
			self.add_error("page", "The page number is not valid integer.")

		return cleaned_data

class ProductForm(forms.Form):
	""" Used to validate the Hash Key provided by the URL """

	q = forms.UUIDField()

	def clean(self):
		cleaned_data = super(ProductForm, self).clean()
		q = cleaned_data.get("q")

		return cleaned_data

class ApiForm(forms.Form):
	""" Used to validate the data from the form """

	data = forms.CharField(
		required=True,
		max_length=128,
		help_text="Data is to tell the server what data it's looking for",
		label="Data",
		error_messages={
			"required": "Please provide 'data' type you looking for.",
			"max_length": "Data is too long to be valid.",
			"invalid": "Data is invalid."
		}
	)

	q = forms.UUIDField(required=False)

	code = forms.CharField(
		required=False,
		max_length=128,
		label="Coupon Code",
		error_messages={
			"invalid": "Coupon Code invalid. Please try another one",
			"max_length": "Coupon Code is too long to be a valid code. Please try another one."
		}
	)

class PayPalForm(forms.Form):
	""" Used to validate PayPals Data and Authentication inputs """

	AuthorizationID = forms.CharField(
		required=False,
		max_length=999,
		min_length=16,
		help_text="PayPals Authorization ID to confirm the payment",
		label="AuthorizationID",
		error_messages={
			"required": "AuthorizationID is required to confim payment.",
			"max_length": "AuthorizationID is too long to be valid.",
			"min_length": "AuthorizationID is too short to be valid.",
			"invalid": "AuthorizationID token is invalid."
		}
	)

	cart_data = forms.CharField(
		required=True,
		label="Cart_data",
		help_text="Cart Data is required and contains all the cart details for the order."
	)

	order_id = forms.CharField(
		required=True,
		max_length=999,
		min_length=16,
		help_text="PayPals Order ID to confirm the payment",
		label="Order_id",
		error_messages={
			"required": "Order ID is required to confim payment.",
			"max_length": "Order ID is too long to be valid.",
			"min_length": "Order ID is too short to be valid.",
			"invalid": "Order ID token is invalid."
		}
	)

	country = forms.CharField(
		required=True,
		max_length=999,
		min_length=2,
		help_text="Country to ship to is required.",
		label="Country",
		error_messages={
			"required": "Country to ship to is required.",
			"max_length": "Country name is too long to be valid.",
			"min_length": "Country name is too short to be valid.",
			"invalid": "Country name is invalid."
		}
	)

	coupon_code = forms.CharField(
		required=False,
		max_length=999,
		min_length=2,
		help_text="Coupon aren't required but must not contain any spaces or other characters beside alphabetical.",
		label="Coupon",
		error_messages={
			"max_length": "Coupon is too long to be valid.",
			"min_length": "Coupon is too short to be valid.",
			"invalid": "Coupon is invalid."
		},
		validators=[RegexValidator("[A-Za-z]", "Coupon code is invalid. It can only contain letters")]
	)

	def clean(self):

		cleaned_data = super(PayPalForm, self).clean()
		order_id = cleaned_data.get("order_id")
		cart_data = cleaned_data.get("cart_data")

		# Make sure the data paypal returns is a dictionary data structure
		if not isinstance(GetOrder().get_order(order_id), dict):
			self.add_error("order_id", "The paypal order returned invalid data.")

		# Check if the cart_data list is available and check to see if we can convert it to a list from a string using 'json'
		if cart_data:
			try:
				json.loads(cart_data)
			except json.JSONDecodeError:
				self.add_error("cart_data", "The cart data list is broken.")

		return cleaned_data

class ZeusOrderForm(forms.Form):
	""" Used to validate the search input for UUID """
	
	sort = forms.CharField(required=False)
	order_id = forms.UUIDField(required=False)

class ZeusOrderDetailsForm(forms.Form):
	""" Used to validate the Hash Key and for POST request """

	order = forms.UUIDField(required=True)
	shippingcompany = forms.CharField(
		required=False,
		max_length=1600,
		min_length=1,
		help_text="The name of the company that will ship the products",
		label="Shipping Company",
		error_messages={
			"max_length": "Company name is too big.",
			"min_length": "Company name is too short.",
			"invalid": "The comapny name is invalid. Please only use letters & numbers."
		}
	)
	trackercode = forms.CharField(
		required=False,
		max_length=1600,
		min_length=1,
		help_text="The tracker code provided by the shipping company",
		label="Tracker Code",
		error_messages={
			"max_length": "The tracker code is too big. Please provide a shorter one if possible or contact the Dev team.",
			"min_length": "The tracker code is too short to be a real tracker code. Please provide a real tracker code.",
			"invalid": "The tracker code is invalid. Please avoid special characters."
		}
	)
	deniedmessage = forms.CharField(
		required=False,
		max_length=1600,
		min_length=20,
		help_text="Message to inform the client why their order is being denied.",
		label="Denied Message",
		error_messages={
			"max_length": "Message is too long. Please shorten it to less than 1600 characters.",
			"min_length": "Message is too short. Please make it longer than 20 characters.",
			"invalid": "Message is invalid. Please use only letters & numbers."
		}
	)
	refund_order_checkbox = forms.BooleanField(
		required=False,
		error_messages={
			"invalid": "CheckBox for Refund is invalid. Please try again."
		}
	)
