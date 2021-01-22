# URLs for App0
from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
	path("api", views.api_handler, name="api_handler"),
	path("about", views.about, name="about"),
	path("signin", views.signin, name="signin"),
	path("signout", views.signout, name="signout"),
	path("signup", views.signup, name="signup"),
	path("signupCheck", views.signupCheck, name="signupCheck"),
	path("shop", views.shop, name="shop"),
	path("product", views.product, name="product"),
	path("cart", views.cart, name="cart"),
	path("cart/pptc", views.paypalTransationComplete, name="paypalTransationComplete"),
	path("cart/tc", views.checkoutComplete, name="checkoutComplete"),
	path("account", views.account, name="account"),
	path("account/history", views.accountHistory, name="accountHistory"),
	path("account/security", views.accountSecurity, name="accountSecurity"),
	path("zeus/orders", views.ZeusOrders, name="ZeusOrders"),
	path("zeus/orders/order_details", views.ZeusOrderDetails, name="ZeusOrderDetails"),
	path("zeus/paypal_accounts", views.ZeusPaypalAccounts, name="ZeusPaypalAccounts"),
]