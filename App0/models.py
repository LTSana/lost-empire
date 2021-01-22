from django.db import models
import uuid

# Google Storage
from gdstorage.storage import GoogleDriveStorage

# Define Google Drive Storage
gd_storage = GoogleDriveStorage()

class Products(models.Model):
	""" Model for the products """

	available = models.BooleanField(default=True)
	name = models.CharField(max_length=128, null=False)
	price = models.FloatField(default=0)
	description = models.TextField(max_length=2000, null=False)
	available_sizes = models.JSONField(null=True, blank=True, default=list)
	category = models.JSONField(null=True, blank=True, default=list)
	brand = models.CharField(max_length=9999, null=False)
	image_0 = models.ImageField(storage=gd_storage, upload_to="lost-empire/")
	image_1 = models.ImageField(storage=gd_storage, upload_to="lost-empire/", null=True, blank=True)
	hash_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	card_color = models.CharField(choices=(("black","black"), ("white","white"), ("gray","gray")), default="black", max_length=20)
	date_made = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"""
		Name: {self.name} 
		Brand: {self.brand} 
		Hash Key: {self.hash_key}
		"""

class Orders(models.Model):
	""" Model for Orders """

	hash_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	order_status = models.CharField(choices=(("WAITING", "WAITING"), ("COMPLETED", "COMPLETED"), ("DENIED", "DENIED")), default="WAITING", max_length=9)
	paypal_auth = models.CharField(max_length=999, null=True, blank=True, help_text="PayPal's Authorization ID to capture the funds. (We currently don't need this)")
	paypal_order_id = models.CharField(max_length=999, null=False, help_text="PayPal Order ID to get the JSON data from PayPal.")
	paypal_data = models.JSONField(null=False)
	cart_data = models.JSONField(null=False)
	country = models.CharField(max_length=1600, null=False, help_text="The Country the products will be shipped to.")
	subtotal = models.FloatField(default=0, null=False)
	shipping_cost = models.FloatField(default=0, null=False, help_text="Shipping cost is determined by the countries Continent.")
	shipping_company = models.CharField(max_length=1600, null=True, blank=True, help_text="The company that will be shipping the products.")
	tracker_id = models.CharField(max_length=1600, null=True, blank=True, help_text="The tracker code given by the shipping company.")
	registered_user = models.BooleanField(default=False, null=True, blank=True)
	user_pk = models.PositiveIntegerField(null=True, blank=True)
	denied_msg = models.CharField(max_length=1600, null=True, blank=True)
	refund_amount = models.FloatField(null=True, blank=True)
	discount_per = models.JSONField(null=True, blank=True, default=dict)
	date_made = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"""
		Paypal Authorization ID: {self.paypal_auth}
		Paypal Order ID: {self.paypal_order_id}
		Country Ship to: {self.country}
		Subtotal: {self.subtotal}
		Shipping Cost: {self.shipping_cost}
		Total Price: {self.subtotal + self.shipping_cost}
		"""

class CouponCodes(models.Model):
	""" Model for Coupon codes """

	code = models.CharField(max_length=20, null=False)
	percentage = models.PositiveIntegerField()

	def __str__(self):
		return f"""
		Code: {self.code}
		Percentage: {self.percentage}
		"""
