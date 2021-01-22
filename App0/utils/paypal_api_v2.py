# PayPals SDK v2
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCaptureRequest, OrdersGetRequest
from paypalcheckoutsdk.payments import CapturesRefundRequest

# Paypal Refund function
from paypalrestsdk import Sale

# Import settings.py
from django.conf import settings

# Other impports
import json

# Creating Access Token for Sandbox
client_id = settings.PAYPAL_CLIENT_ID
client_secret = settings.PAYPAL_CLIENT_SECRET

# Creating an environment
environment = SandboxEnvironment(client_id=client_id, client_secret=client_secret)
client = PayPalHttpClient(environment)

# Here, OrdersCaptureRequest() creates a POST request to /v2/checkout/orders
# Replace APPROVED-ORDER-ID with the actual approved order id.
def CapturePayPalOrder(paypal_order_id):
	
	request = OrdersCaptureRequest(paypal_order_id)

	try:
		# Call API with your client and get a response for your call
		response = client.execute(request)

		# If call returns body in response, you can get the deserialized version from the result attribute of the response
		order = response.result.id
		return order
	except IOError as ioe:
		if isinstance(ioe, HttpError):
			# Something went wrong server-side
			print(ioe.status_code)
			print(ioe.headers)
			print(ioe)
		else:
			# Something went wrong client side
			print(ioe)

def GetOrder(order_id):
	"""You can use this function to retrieve an order by passing order ID as an argument"""   
	"""Method to get order"""
	request = OrdersGetRequest(order_id)
	response = client.execute(request)
	return response.result.__dict__["_dict"]

def RefundOrder(capture_id, refund_amount=0, currency_code="EUR"):
	"""Use the following function to refund an capture.
		Pass a valid capture ID as an argument."""
	sale = Sale.find(capture_id)

	refund = sale.refund({
	"amount": {
		"total": refund_amount,
		"currency": currency_code
	}
	})

	if refund.success():
		print("Refund[%s] Success" % (refund.id))
		return True # Return True if the Refund was successfull
	else:
		print(refund.error)
		return False # Return False if the Refund failed
