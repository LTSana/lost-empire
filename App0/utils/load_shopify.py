# Used to to load Shopify API
from django.http import HttpResponseRedirect
from django.urls import reverse

from functools import wraps

# Import settings
from django.conf import settings

# Shopify
import shopify
from shopify_app.decorators import shop_login_required

def load_shopify(function):
	@wraps(function)
	def wrap(request, *args, **kwargs):
		shop_url = f"https://{settings.SHOPIFY_API_KEY_STORE}:{settings.SHOPIFY_API_PASSWORD_STORE}@{settings.SHOPIFY_SHOP}.myshopify.com/admin/api/2021-01"
		shopify.ShopifyResource.set_site(shop_url)
		return function(request, *args, **kwargs)
	return wrap
