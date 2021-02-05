# Developed by Sana N. Mngadi
# Django Framework
# 
# Check REAME.md file for more information on the project

from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages

# Import the User models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Decorations
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

# Import the User models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Import settings
from django.conf import settings

# Get forms
from .forms import SigninForm, \
					SignupForm, \
					EmailCheckForm, \
					AccountSecurityForm, \
					ShopForm, \
					ProductForm, \
					ApiForm, \
					PayPalForm, \
					ZeusOrderForm, \
					ZeusOrderDetailsForm

# Shopify
import shopify
from shopify_app.decorators import shop_login_required

# Import Models
from .models import Products, Orders, CouponCodes

# Get custom decorations
from .utils.login_excluded import login_excluded

# Get custom form error checker
from .utils.form_error_catch import form_error_catcher

# Import PayPal API
from .utils.paypal_api_v2 import GetOrder, CapturePayPalOrder, RefundOrder

# Additional Database queries
from django.db.models import Q, Avg, Count

# Other imports
import requests
import json
import time
import os
import locale

# CUSTOM ERROR HANDLERS
#############################################################
def handler404(request, *args, **argv):
    return render(request, "lost-empire/site_templates/errors/404.html", status=404)

def handler403(request, *args, **argv):
    return render(request, "lost-empire/site_templates/errors/403.html", status=403)

def handler500(request, *args, **argv):
    return render(request, "lost-empire/site_templates/errors/500.html", status=500)

def csrf_failure(request, reason=""):
	return render(request, "lost-empire/site_templates/errors/403.html", status=403)
#############################################################

# Create your views here.

@shop_login_required
def index(request):
	""" Home page """

	if request.method == "GET":

		product_data = shopify.product.all()
		print(product_data)

		# Get the system discound
		system_discount = True if request.user.is_authenticated else False
		if system_discount:
			discount_per = 20

		# Get 100 products from the Data
		products = Products.objects.all().order_by("-date_made")[:100]

		# Get the diffrent categories
		tmp_list = []
		category_list = []
		for product in products:
			for category in product.category:
				for a in category["categories"]:
					if a not in tmp_list and product.hash_key not in category_list:
						category_list.append({
							"category": a,
							"product_id": product.hash_key,
							"image_0": (product.image_0.url).replace("&export=download", "") if product.image_0.url else None,
							"card_color": product.card_color
						})
						tmp_list.append(a)
						break

			# Add the discount price if available
			if system_discount:
				product.old_price = product.price
				product.price = "{:,.2f}".format(product.price * (100 - discount_per) / 100)

		html_content = {
			"products": products[:8],
			"categories": category_list[:4]
		}
		return render(request, "lost-empire/site_templates/index.html", html_content)
	else:
		return render(request, "lost-empire/site_templates/index.html")

def about(request):
	""" About page """

	if request.method == "GET":
		return render(request, "lost-empire/site_templates/about.html")
	else:
		return render(request, "lost-empire/site_templates/about.html")

@login_excluded("index")
def signin(request):
	""" Signin Page """

	if request.method == "POST":

		# Use the Signin Form created in forms.py
		form = SigninForm(request.POST)

		# Check if the inputs pass the validation check
		if form.is_valid():
			# Get the secret key
			secret_key = settings.RECAPTCHA_SECRET_KEY

			# captcha verification
			data = {
				'response': request.POST.get('g-recaptcha-response'),
				'secret': secret_key
			}
			resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
			result_json = resp.json()

			# Check if the user is a bot
			if result_json.get("success"):
				try:
					# Check if the User is in the Database
					user_tmp = User.objects.get(email=str(form.cleaned_data["email"]))
					user = authenticate(request, username=str(user_tmp.username), password=str(form.cleaned_data["pwd"]))
					# Compare the users password with the inputed one
					if user:

						# Login the user
						login(request, user)

						#messages.success(request, f"Sucessfully logged in {user.email}")
						return HttpResponseRedirect(reverse("index"))
					else:
						messages.error(request, "Email or Password is wrong... Try Again!", extra_tags="form_signin")
						return HttpResponseRedirect(reverse("signin"))
				except User.DoesNotExist:
					messages.error(request, "Email or Password is wrong... Try Again!", extra_tags="form_signin")
					return HttpResponseRedirect(reverse("signin"))
			else:
				messages.error(request, "Email or Password is wrong... Try Again!", extra_tags="form_signin")
				return HttpResponseRedirect(reverse("signin"))
		else:

			# Check if any errors were returned
			if form.errors.get_json_data():
				# Find the errors
				form_error_catcher(request, form=form, array_list=["email", "pwd"], extra_tags="form_signin")
			else:
				messages.error(request, "Signin form invalid with no errors given...", extra_tags="form_signin")
			
			return HttpResponseRedirect(reverse("signin"))
	elif request.method == "GET":

		html_content = {
			"site_key": settings.RECAPTCHA_SITE_KEY,
		}

		return render(request, "lost-empire/site_templates/signin.html", html_content)
	else:
		return render(request, "lost-empire/site_templates/signin.html")

@login_required
def signout(request):
	""" Sign out the user """

	if request.method == "GET":

		# Log the user out of the session
		logout(request)
		messages.success(request, "Signed out successfully.", extra_tags="form_signin")

		return HttpResponseRedirect(reverse("signin"))
	
	else:

		# Check if the user is logged in and log them out
		if request.user.is_authenticated:
			logout(request)
			messages.success(request, "Signed out successfully.", extra_tags="form_signin")
		
		return HttpResponseRedirect(reverse("sigin"))

@login_excluded("index")
def signup(request):
	""" Singup for users """

	if request.method == "POST":

		# Use the Signup Form created in forms.py
		form = SignupForm(request.POST)

		# Check if the inputs pass the validation check
		if form.is_valid():

			# Get the secret key
			secret_key = settings.RECAPTCHA_SECRET_KEY

			# captcha verification
			data = {
				'response': request.POST.get('g-recaptcha-response'),
				'secret': secret_key
			}
			resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
			result_json = resp.json()

			# Check if the user is a bot
			if result_json.get("success"):
				
				# Check if the password and confirm password match
				if str(form.cleaned_data["pwd"]) == str(form.cleaned_data["cpwd"]):
					
					# Check if the email address is in use already
					try:
						user = User.objects.get(email=form.cleaned_data["email"])
						if user:
							messages.warning(request, "That e-mail address is already being used!", extra_tags="form_signup")
							return HttpResponseRedirect(reverse("signin"))
					except User.DoesNotExist:
						print("Email is cleared...")
					
					# The usernames will be stored as numbers
					# This is to avoid creating a abstract User Model and keep the original Django User Model
					username_generator = 1
					while True:
						try:
							user = User.objects.get(username=f"{username_generator}")
							username_generator += 1
						except User.DoesNotExist:
							break

					# Create user in the Database
					User.objects.create_user(
						username=str(username_generator),
						first_name=str(form.cleaned_data["first_name"]),
						last_name=str(form.cleaned_data["last_name"]),
						email=str(form.cleaned_data["email"]),
						password=str(form.cleaned_data["cpwd"]) # Passwords will be automatically hashed by Django's hasher (Check settings.py for Hasher type)
					).save()

					## Get the HTML template of the email
					#with open(os.getcwd()+"/templates/lost-empire/email_templates/register.html") as f:
					#	email_html = f.read()
					#f.close()

					## Get the TEXT template of the email
					#with open(os.getcwd()+"/templates/lost-empire/email_templates/register.txt") as f:
					#	email_text = f.read()
					#f.close()

					## Send an email to the new user
					#try:
					#	send_mail(
					#		subject="Welcome to Teeker",
					#		message=email_text.replace("{{fullname}}", form.cleaned_data['firstname'] +" "+ form.cleaned_data['lastname']),
					#		from_email=settings.MAIL_SENDER,
					#		recipient_list=[form.cleaned_data["email"]],
					#		fail_silently=False,
					#		html_message=email_html.replace("{{fullname}}", form.cleaned_data['firstname'] +" "+ form.cleaned_data['lastname'])
					#		)
					#except BadHeaderError:
					#	print("--- Failed to send welcome email! ---")

					# Attempt to automatically login the user
					user_tmp = User.objects.get(email=str(form.cleaned_data["email"]))
					ready_user = authenticate(request, username=str(user_tmp.username), password=str(form.cleaned_data["pwd"]))

					if ready_user:
						login(request, ready_user)
						#messages.success(request, "Successfully Sign up! Welcome to Lost Empire.")
						return HttpResponseRedirect(reverse("index"))
					else:
						messages.warning(request, "Signed Up successfully! But failed to log in automatically.", extra_tags="form_signin")
						return HttpResponseRedirect(reverse("signin"))
				else:
					messages.warning(request, "Password and confirm password do not match each other!", extra_tags="form_signup")
					return HttpResponseRedirect(reverse("signin"))

			else:
				messages.error(request, "reCAPTCHA has picked up bot behaviour... Try Again!", extra_tags="form_signup")
				return HttpResponseRedirect(reverse("signin"))
		else:

			# Check if any errors were returned
			if form.errors.get_json_data():
				
				# Find the errors
				form_error_catcher(request, form=form, array_list=["first_name", "last_name", "email", "pwd", "cpwd"], extra_tags="form_signup")
			else:
				messages.error(request, "Signin form invalid with no errors given...", extra_tags="form_signup")
			
			return HttpResponseRedirect(reverse("signin"))

@login_excluded("index")
def signupCheck(request):
	""" Check the email address that's about to be used. """

	if request.method == "POST":

		# Use the EmailCheck Form created in forms.py
		form = EmailCheckForm(request.POST)

		if form.is_valid():

			if form.cleaned_data["email"]:

				# Check if the email can be used
				try:
					user = User.objects.get(email=form.cleaned_data["email"])
					
					if user:
						return JsonResponse({"STATUS": True, "EMAIL": "usable_false", "MESSAGE": "TAKEN"})
					else:
						return JsonResponse({"STATUS": True, "EMAIL": "usable_true", "MESSAGE": "GOOD"})
				except User.DoesNotExist:
					return JsonResponse({"STATUS": True, "EMAIL": "usable_true", "MESSAGE": "GOOD"})

			else:
				return JsonResponse({"STATUS": False})
		else:

			# Check if any error messages where returned
			if form.errors.get_json_data():

				try:
					# Check if the email is the error message
					if form.errors.get_json_data()["email"]:

						# Check the code error that was given
						if form.errors.get_json_data()["email"][0]["code"] == "min_length":
							return JsonResponse({"STATUS": True, "EMAIL": "min_length", "MESSAGE": form.errors.get_json_data()["email"][0]["message"]})
						elif form.errors.get_json_data()["email"][0]["code"] == "max_length":
							return JsonResponse({"STATUS": True, "EMAIL": "max_length", "MESSAGE": form.errors.get_json_data()["email"][0]["message"]})
						elif form.errors.get_json_data()["email"][0]["code"] == "invalid":
							return JsonResponse({"STATUS": True, "EMAIL": "invalid", "MESSAGE": form.errors.get_json_data()["email"][0]["message"]})
					else:
						return JsonResponse({"STATUS": True, "EMAIL": "invalid", "MESSAGE": form.errors.get_json_data()["email"][0]["message"]})
				except KeyError:
					print("E-mail address wasn't checked...")

				return JsonResponse({"STATUS": False})
			else:
				return JsonResponse({"STATUS": False})

def cart(request):
	""" Cart Page """

	if request.method == "GET":
		# Open the Country JSON file to give the user country codes to select from in the form
		with open(os.getcwd()+"/country_codes/country_JSON_v1.json") as f:
			country_data = json.load(f)
		f.close()

		html_content = {
			"country_data": country_data,
			"paypal_client_id": settings.PAYPAL_CLIENT_ID,
		}
		return render(request, "lost-empire/site_templates/cart.html", html_content)

def paypalTransationComplete(request):
	""" Confirms the order and approves Payment """

	if request.method == "POST":

		# Get the system discound
		system_discount = True if request.user.is_authenticated else False
		if system_discount:
			discount_per = 20

		form = PayPalForm(request.POST)

		if form.is_valid():

			# Check if a counpon was used (discount_per_db is the coupon discount)
			discount_per_db = 0
			if form.cleaned_data.get("coupon_code"):
				try:
					discount_per_db += CouponCodes.objects.get(code=form.cleaned_data.get("coupon_code")).percentage
				except CouponCodes.DoesNotExist:
					print("Coupon code does not exist.")

			# Get the Order Data from PayPal
			paypal_order_data = GetOrder(form.cleaned_data.get("order_id"))

			subtotal = 0
			# Get the price of each Product and add them to the subtotal
			for cart in json.loads(form.cleaned_data.get("cart_data")):
				try:
					product = Products.objects.get(hash_key=cart["product_id"])
					subtotal += ((product.price * (100 - discount_per) / 100) * (100 - discount_per_db) / 100 if system_discount else product.price * (100 - discount_per_db) / 100) * cart["quantity"]
				except Products.DoesNotExist:
					return JsonResponse({"STATUS": True, "TC": False, "error_message": f"Please remove product at position: {cart['cart_id']} in your cart."})

			# Open the Country JSON file to give the user country codes to select from in the form
			with open(os.getcwd()+"/country_codes/country_JSON_v1.json") as f:
				country_data = json.load(f)
			f.close()
			
			shipping = 0
			# Look for the Continet that will be shipped to and charge by continet
			for country in country_data:
				if form.cleaned_data.get("country") == country["Country_Name"]:
					if country["Continent"] in ["EU", "NA"]:
						shipping = 21.34
					else:
						shipping = 23.48

			# Make sure the prices of the products and shipping match the price paid on paypal match
			if '{:,.2f}'.format(subtotal + shipping) != '{:,.2f}'.format(float(paypal_order_data["purchase_units"][0]["amount"]["value"])):
				return JsonResponse({"STATUS": True, "TC": False, "error_message": "The prices have changed. Sorry try again."})

			# Create the order in the Database before Capturing the funds
			database_order_data = Orders.objects.create(
				paypal_auth=form.cleaned_data.get("AuthorizationID"),
				paypal_order_id=form.cleaned_data.get("order_id"),
				paypal_data=GetOrder(form.cleaned_data.get("order_id")),
				cart_data=json.loads(form.cleaned_data.get("cart_data")),
				country=form.cleaned_data.get("country"),
				subtotal=subtotal,
				shipping_cost=shipping,
				registered_user= True if request.user.is_authenticated else False,
				user_pk= request.user.pk if request.user.is_authenticated else None,
				discount_per={"user_discount": discount_per if system_discount else 0, "coupon_discount": discount_per_db},
			)

			# Authorize the transaction after placing it in the Database
			#CaptureAuthorization().capture_auth(form.cleaned_data.get("AuthorizationID"))

			CapturePayPalOrder(form.cleaned_data.get("order_id"))

			# Update the PayPal Data to the CAPTURED one which contains more detail
			database_order_data.paypal_data = GetOrder(form.cleaned_data.get("order_id"))
			database_order_data.save()

			return JsonResponse({"STATUS": True, "TC": True, "order_id": database_order_data.hash_key})
		else:

			# Cannot use the custom form error catcher here because of the Json response
			for _inputs in ["AuthorizationID", "cart_data", "order_id", "country", "coupon_code"]:
				try:
					# Check if the error return has the '_inputs' details of why it's invalid
					if form.errors.get_json_data()[_inputs] and form.errors.get_json_data()[_inputs][0]["code"] in ["required", "max_length", "min_length", "invalid"]:
						return JsonResponse({"STATUS": True, "TC": False, "error_message": form.errors.get_json_data()[_inputs][0]["message"]})
					elif form.errors.get_json_data()[_inputs]:
						return JsonResponse({"STATUS": True, "TC": False, "error_message": form.errors.get_json_data()[_inputs][0]["message"]})
				except KeyError:
					print(f"Form validation error '{_inputs}' cannot be found!")

			return JsonResponse({"STATUS": True, "TC": False, "error_message": "Something wen't wrong. Try again!"})

def checkoutComplete(request):
	""" Show this page for when the transaction is complete """

	if request.method == "GET":

		html_content = {
			"order_id": request.GET.get('order'),
			"error_message": request.GET.get('er'),
		}
		return render(request, "lost-empire/site_templates/transactions/complete.html", html_content)

@login_required
def account(request):
	""" Account Page """

	if request.method == "GET":
		return render(request, "lost-empire/site_templates/account/account.html")

@login_required
def accountHistory(request):
	""" Account History page """

	if request.method == "GET":

		# Get all the orders that the User is associated with
		history_data = Orders.objects.all().filter(user_pk__contains=request.user.pk).order_by("-date_made")
		
		# Calculate all the totals for each order
		for history in history_data:
			history.total = "{:,.2f}".format(float(history.subtotal) + float(history.shipping_cost))
			history.subtotal = "{:,.2f}".format(history.subtotal)

			# Get the Price and Discount for the products
			for cart in history.cart_data:
				try:
					product = Products.objects.get(hash_key=cart["product_id"])
					cart["price"] = product.price
					cart["discount_per"] = history.discount_per
					cart["d_price"] = "{:,.2f}".format((product.price * (100 - history.discount_per["user_discount"]) / 100) * (100 - history.discount_per["coupon_discount"]) / 100 if history.discount_per else product.price * (100 - history.discount_per["coupon_discount"]) / 100)
				except Products.DoesNotExist:
					cart["price"] = "N/A"

		html_content = {
			"history_data": history_data,
		}
		return render(request, "lost-empire/site_templates/account/history.html", html_content)

@login_required
def accountSecurity(request):
	""" Account Security page """

	if request.method == "GET":
		return render(request, "lost-empire/site_templates/account/security.html")
	
	elif request.method == "POST":

		form = AccountSecurityForm(request.POST)

		if form.is_valid():
			user = User.objects.get(pk=request.user.pk)
			
			# Check if the old password is the current password
			if user.check_password(form.cleaned_data["opwd"]):
				user.set_password(form.cleaned_data["npwd"])
				user.save()
				messages.success(request, "Successfully changed your password!", extra_tags="form_signin")

			else:
				messages.error(request, "Old password is wrong! Try again.")

			return HttpResponseRedirect(reverse("accountSecurity"))
		else:

			# Check if any errors were returned
			if form.errors.get_json_data():

				# Find the errors
				form_error_catcher(request, form=form, array_list=["opwd", "npwd", "cpwd"])

			else:
				messages.error(request, "Security (Password Change) form invalid with no errors given...")
			
			return HttpResponseRedirect(reverse("accountSecurity"))

def shop(request):
	""" Shop page """

	if request.method == "GET":

		# Control the page nation
		number_of_products = 50 # The number of products to show

		# Get the system discound
		system_discount = True if request.user.is_authenticated else False
		if system_discount:
			discount_per = 20

		# Validate all the inputs from the browser
		form = ShopForm(request.GET)
		
		if form.is_valid():

			if (len(json.loads(form.cleaned_data.get("size"))) if form.cleaned_data.get("size") else 0) <= 0 and (len(json.loads(form.cleaned_data.get("category"))) if form.cleaned_data.get("category") else 0) <= 0 and (len(json.loads(form.cleaned_data.get("brand"))) if form.cleaned_data.get("brand") else 0) <= 0 and not form.cleaned_data.get("page"):
				
				# Get all the products
				products = Products.objects.all().exclude(available=False).order_by("-date_made")

				if form.cleaned_data.get('search'):
					# Get all the products that match search
					products = Products.objects.all().exclude(available=False).filter(
						Q(name__icontains=form.cleaned_data.get('search')) |
						Q(brand__icontains=form.cleaned_data.get('search')) |
						Q(category__icontains=[{"categories": [form.cleaned_data.get('search')]}])
						).order_by("-date_made")
				else:
					# Get all the products
					products = Products.objects.all().exclude(available=False).order_by("-date_made")

				# Get all the filter options
				available_size_list = []
				available_category_list = []
				available_brand_list = []
				for product in products:

					# Get all the available sizes
					for size in product.available_sizes:
						for a in size["sizes"]:
							if a not in available_size_list:
								if a == "ONE SIZE FITS ALL":
									if "XS" in available_size_list:
										available_size_list.insert(0,a)
									else:
										available_size_list.insert(0,a)
								elif a == "XS":
									if "ONE SIZE FITS ALL" in available_size_list:
										available_size_list.insert(1,a)
									else:
										available_size_list.insert(0,a)
								else:
									available_size_list.append(a)
					
					# Get all the available categories
					for category in product.category:
						for a in category["categories"]:
							if a not in available_category_list:
								available_category_list.append(a)

					# Get all the available brands
					if product.brand not in available_brand_list:
						available_brand_list.append(product.brand)
					
					# Add the discount price
					if system_discount:
						product.old_price = product.price
						product.price = "{:,.2f}".format(product.price * (100 - discount_per) / 100)

				# Get the previous page
				previous_page = 0

				# Check if the user can go to the next page
				next_page = 1 if len(products[1 * number_of_products:]) > 0 else 0

				# Check how many pages forward the user can go before not having any content
				for a in range(1, 5):
					if len(products[a*number_of_products:]) <= 0:
						break								
				pages_forwards = range(1, a)

				# Set the params for pagination
				pagination_data = {
						"current_page": 0, 
						"previous_page": previous_page, 
						"next_page": next_page,
						"pages_forwards": pages_forwards,
						}

				# Set the HTML content
				html_content = {
					"total_products": len(Products.objects.all().exclude(available=False)),
					"products": products[:number_of_products],
					"page_numbers": pagination_data,
					"available_size_list": available_size_list,
					"available_category_list": available_category_list,
					"available_brand_list": available_brand_list,
				}

			else:

				# Get all the products
				products = []

				# Store all Products except non availables
				data = Products.objects.all().exclude(available=False).order_by("-date_made")

				# Look for Sizes that match query
				data_0 = None
				if form.cleaned_data.get("size"):
					data_0 = data.filter(available_sizes__contains=[{"sizes": json.loads(form.cleaned_data.get('size'))}])

				# Look for brands that match query
				data_1 = None
				if form.cleaned_data.get("brand"):
					for brand in json.loads(form.cleaned_data.get("brand")):
						data_1 = (data_0 if data_0 else data).filter(brand__contains=brand)

				# Look for Category that match query
				data_2 = None
				if form.cleaned_data.get("category"):
					data_2 = (data_1 if data_1 else (data_0 if data_0 else data)).filter(category__contains=[{"categories": json.loads(form.cleaned_data.get('category'))}])

				# Figure out which filter has data in it starting from the top to bottom
				if data and not (data_0 or data_1 or data_2):
					products = data
				elif data_0 and not (data_1 or data_2):
					products = data_0
				elif data_1 and not (data_2):
					products = data_1
				elif data_2:
					products = data_2

				# Get all the filter options
				available_size_list = []
				available_category_list = []
				available_brand_list = []
				for product in products:

					# Get all the available sizes
					for size in product.available_sizes:
						for a in size["sizes"]:
							if a not in available_size_list:
								if a == "ONE SIZE FITS ALL":
									if "XS" in available_size_list:
										available_size_list.insert(0,a)
									else:
										available_size_list.insert(0,a)
								elif a == "XS":
									if "ONE SIZE FITS ALL" in available_size_list:
										available_size_list.insert(1,a)
									else:
										available_size_list.insert(0,a)
								else:
									available_size_list.append(a)
					
					# Get all the available categories
					for category in product.category:
						for a in category["categories"]:
							if a not in available_category_list:
								available_category_list.append(a)

					# Get all the available brands
					if product.brand not in available_brand_list:
						available_brand_list.append(product.brand)

					if system_discount:
						product.old_price = product.price
						product.price = "{:,.2f}".format(product.price * (100 - discount_per) / 100)

				# Get the number of the page and multiple it by the number of products allowed in each page
				try:
					page_start = form.cleaned_data["page"] * number_of_products
				except TypeError:
					return HttpResponseRedirect(reverse("shop"))

				# Get the previous page
				previous_page = form.cleaned_data["page"] - 1 if form.cleaned_data["page"] - 1 > 0 else 0

				# Get the number of pages back the user can go
				pages_backwards = range((form.cleaned_data["page"] - 3) if (form.cleaned_data["page"] - 3) > 0 else 0, form.cleaned_data["page"])
				
				# Check if the user can go to the next page
				next_page = form.cleaned_data["page"] + 1 if len(products[(form.cleaned_data["page"] + 1) * number_of_products:]) > 0 else 0

				# Check how many pages forward the user can go before not having any content
				for a in range((form.cleaned_data["page"]+1), (form.cleaned_data["page"]+5)):
					if len(products[a*number_of_products:]) <= 0:
						break								
				pages_forwards = range((form.cleaned_data["page"]+1), a)

				# Set the params for pagination
				pagination_data = {
						"current_page": form.cleaned_data["page"], 
						"previous_page": previous_page, 
						"next_page": next_page,
						"pages_backwards": pages_backwards,
						"pages_forwards": pages_forwards,
						}

				# Set the HTML Content
				html_content = {
					"total_products": len(Products.objects.all().exclude(available=False)),
					"products": products[page_start:page_start + number_of_products],
					"page_numbers": pagination_data,
					"available_size_list": available_size_list,
					"available_category_list": available_category_list,
					"available_brand_list": available_brand_list,
				}

			# Render the page with the content
			return render(request, "lost-empire/site_templates/shop.html", html_content)	
		else:
			return render(request, "lost-empire/site_templates/shop.html")

def product(request):
	""" Product page """

	if request.method == "GET":

		form = ProductForm(request.GET)
		
		if form.is_valid():

			try:
				# Get the product using the Hash Key provided in the request
				product = Products.objects.get(hash_key=form.cleaned_data["q"])

				# Check if the user is logged in and give them a discount
				if request.user.is_authenticated:
					_discount = True
					discount_per = 20

				html_content = {
					"product": {
					"hash_key": product.hash_key,
					"image_0": product.image_0,
					"image_1": product.image_1,
					"available": product.available,
					"pk": product.pk,
					"name": product.name, 
					"price": "{:,.2f}".format(product.price * (100 - (discount_per if request.user.is_authenticated else 0)) / 100), 
					"old_price": "{:,.2f}".format(product.price),
					"discount": _discount if request.user.is_authenticated else 0,
					"description": product.description,
					"available_sizes": product.available_sizes[0]["sizes"],
					"card_color": product.card_color,
					}
				}
			except:
				html_content = {
					"product": {
						"name": "OUT OF STOCK!",
						"description": "OUT OF STOCK!"
					}
				}

		else:
			html_content = {
				"product": {
					"name": "OUT OF STOCK!",
					"description": "OUT OF STOCK!"
				}
			} 

		return render(request, "lost-empire/site_templates/product.html", html_content)

def api_handler(request):
	""" Handles any API request """

	if request.method == "GET":

		form = ApiForm(request.GET)

		if form.is_valid():

			if form.cleaned_data["data"] == "product":

				# Get the system discound
				system_discount = True if request.user.is_authenticated else False
				if system_discount:
					discount_per = 20

				if form.cleaned_data["q"]:
					try:
						product = Products.objects.get(hash_key=form.cleaned_data["q"])
						return JsonResponse({"STATUS": True, "product": {
																	"hash_key": product.hash_key,
																	"image_0": (product.image_0.url).replace("&export=download", "") if product.image_0.url else None,
																	"image_1": (product.image_1.url).replace("&export=download", "") if product.image_1.url else None,
																	"available": product.available,
																	"pk": product.pk,
																	"name": product.name, 
																	"price": product.price * (100 - discount_per) / 100 if system_discount else product.price, 
																	"discount": system_discount,
																	"old_price": "{:,.2f}".format(product.price),
																	"description": product.description,
																	"available_sizes": product.available_sizes[0]["sizes"],
																	"card_color": product.card_color,
																	}
												})
					except Products.DoesNotExist:
						return JsonResponse({"STATUS": True, "product": {}})
				return JsonResponse({"STATUS": False})
			
			# Check if the API is asking for a coupon code
			elif form.cleaned_data.get("data") == "coupon":

				# Check if the Coupon Code is valid and in the Database
				try:
					coupon_data = CouponCodes.objects.get(code=form.cleaned_data.get("code"))

					# Return the Percentage the coupon code has
					return JsonResponse({"STATUS": True, "VALID": True, "PERCENT": float(coupon_data.percentage)})
				except CouponCodes.DoesNotExist:
					return JsonResponse({"STATUS": True, "VALID": False, "PERCENT": 0})
			else:
				return JsonResponse({"STATUS": False})
		else:
			return JsonResponse({"STATUS": False, "error_message": form.errors.get_json_data()})

@login_required
def ZeusOrders(request):
	""" Zeus Orders """

	if request.method == "GET":

		form = ZeusOrderForm(request.GET)

		if form.is_valid():
			
			if form.cleaned_data.get("order_id"):
				order_data = Orders.objects.all().filter(hash_key__icontains=form.cleaned_data.get("order_id"))
			else:
				if form.cleaned_data.get("sort") == "r":
					order_data = Orders.objects.all()
				elif form.cleaned_data.get("sort").lower() in ["complete", "waiting", "denied"]:
					order_data = Orders.objects.all().order_by("-date_made").filter(order_status__contains=form.cleaned_data.get("sort").upper())
				elif form.cleaned_data.get("sort") == "no":
					order_data = Orders.objects.all().order_by("-date_made")
				elif form.cleaned_data.get("sort") == "on":
					order_data = Orders.objects.all().order_by("date_made")
				else:
					order_data = Orders.objects.all().order_by("-date_made")
			
			html_content = {
				"order_data": order_data,
			}

			return render(request, "lost-empire/site_templates/zeus/orders.html", html_content)
		else:

			# Handle errors if form is invalid
			form_error_catcher(request, form, ["r", "order_id"])

		# Load all the Orders
		order_data = Orders.objects.all().order_by("-date_made")

		html_content = {
			"order_data": order_data,
		}
		return render(request, "lost-empire/site_templates/zeus/orders.html", html_content)

@login_required
def ZeusOrderDetails(request):
	""" Zeus Order Details shows the order details """

	if request.method == "GET":
		
		form = ZeusOrderDetailsForm(request.GET)

		if form.is_valid():
			
			try:
				# Get the Data of the Order being viewed
				order_data = Orders.objects.get(hash_key=form.cleaned_data.get("order"))

				order_data.total = "{:,.2f}".format(float(order_data.subtotal) + float(order_data.shipping_cost))
				order_data.subtotal = "{:,.2f}".format(order_data.subtotal)
				order_data.shipping_cost = "{:,.2f}".format(order_data.shipping_cost)

				# Get the data needed for the cart product
				for a in range(len(order_data.cart_data)):
					try:
						product = Products.objects.get(hash_key=order_data.cart_data[a]["product_id"])
						order_data.cart_data[a]["image_0"] = (product.image_0.url).replace("&export=download", "") if product.image_0.url else None
						order_data.cart_data[a]["price"] = product.price
						order_data.cart_data[a]["discount_per"] = order_data.discount_per
						order_data.cart_data[a]["d_price"] = "{:,.2f}".format((product.price * (100 - order_data.discount_per["user_discount"]) / 100) * (100 - order_data.discount_per["coupon_discount"]) / 100 if order_data.discount_per else product.price * (100 - order_data.discount_per["coupon_discount"]) / 100)
						order_data.cart_data[a]["card_color"] = product.card_color
					except Products.DoesNotExist:
						order_data.cart_data[a]["price"] = "N/A"

				html_content = {
					"order_data": order_data
				}
				return render(request, "lost-empire/site_templates/zeus/orders/order_details.html", html_content)
			except Orders.DoesNotExist:
				messages.error(request, "Order is not available in the Database.")
				return HttpResponseRedirect(reverse("ZeusOrders"))
		else:
			# Handle errors if form is invalid
			form_error_catcher(request, form, ["order"])
			return HttpResponseRedirect(reverse("ZeusOrders"))
	
	elif request.method == "POST":

		# Validate the inputs
		form = ZeusOrderDetailsForm(request.POST)

		if form.is_valid():
			
			# Check if the order is being completed
			if request.GET.get("p") == "order_completed":
				
				# Shipping Company name is required even tho in forms.py is set to False
				if not form.cleaned_data.get("shippingcompany"):
					messages.warning(request, "Shipping company is required. Please provide the name of the shipping company.")
					return HttpResponseRedirect(f"/zeus/orders/order_details?order={form.cleaned_data.get('order')}")
				else:

					# Check if the order is still in the Database
					try:
						# Get the Data of that order
						order_data = Orders.objects.get(hash_key=form.cleaned_data.get("order"))

						# Set it to completed
						order_data.order_status = "COMPLETED"

						# Add the Shipping company name
						order_data.shipping_company = form.cleaned_data.get("shippingcompany")

						# Check if the tracker code/id is available
						if form.cleaned_data.get("trackercode"):
							# Add it to the orders data
							order_data.tracker_id = form.cleaned_data.get("trackercode")

						# Commit to the Database (Save the changes to the Database)
						order_data.save()

						messages.success(request, "Order has been completed.")
						return HttpResponseRedirect(f"/zeus/orders/order_details?order={form.cleaned_data.get('order')}")
					except Orders.DoesNotExist:
						message.error(request, "The order is no longer available in the Database. Most likely it has been removed")
						return HttpResponseRedirect(reverse("ZeusOrders"))
			
			# Check if the order is being denied
			elif request.GET.get("p") == "denied_order":
				
				# Check if the order is still in the Database
				try:
					# Get the Data of that order
					order_data = Orders.objects.get(hash_key=form.cleaned_data.get("order"))

					# Set it to denied
					order_data.order_status = "DENIED"

					# Add the Shipping company name
					if form.cleaned_data.get("deniedmessage"):
						order_data.denied_msg = form.cleaned_data.get("deniedmessage")
					else:
						messages.error(request, "A message of denial is required to successfully deny an order")
						return HttpResponseRedirect(f"/zeus/orders/order_details?order={form.cleaned_data.get('order')}")

					# Check if refund is enabled
					if form.cleaned_data.get("refund_order_checkbox"):
						order_data.refund_amount = order_data.paypal_data["purchase_units"][0]["payments"]["captures"][0]["amount"]["value"]
						refund_status = RefundOrder(order_data.paypal_data["purchase_units"][0]["payments"]["captures"][0]["id"], refund_amount="{:.2F}".format(float(order_data.paypal_data["purchase_units"][0]["payments"]["captures"][0]["amount"]["value"])), currency_code=order_data.paypal_data["purchase_units"][0]["payments"]["captures"][0]["amount"]["currency_code"])

						# Check if the ReFund was successful
						if not refund_status:
							messages.error(request, "Refund failed. Please go to the Merchant's PayPal Account and check the status of refund for this order.")
							return HttpResponseRedirect(f"/zeus/orders/order_details?order={form.cleaned_data.get('order')}")
					else:
						order_data.refund_amount = 0
						
					# Commit to the Database (Save the changes to the Database)
					order_data.save()

					messages.success(request, "Order has been denied.")
					return HttpResponseRedirect(f"/zeus/orders/order_details?order={form.cleaned_data.get('order')}")
				except Orders.DoesNotExist:
					message.error(request, "The order is no longer available in the Database. Most likely it has been removed")
					return HttpResponseRedirect(reverse("ZeusOrders"))
			
			# Else tell the user that the option p is missing
			else:
				messages.error(request, "Missing p option.")
				return HttpResponseRedirect(f"/zeus/orders/order_details?order={form.cleaned_data.get('order')}")
		else:
			# Handle errors if form is invalid
			form_error_catcher(request, form, ["shippingcompany", "trackercode", "deniedmessage"])
			return HttpResponseRedirect(f"/zeus/orders/order_details?order={form.cleaned_data.get('order')}")

@login_required
def ZeusPaypalAccounts(request):
	""" Zeus Paypal Account Credentials """

	if request.method == "GET":
		return render(request, "lost-empire/site_templates/zeus/paypal_accounts.html")
