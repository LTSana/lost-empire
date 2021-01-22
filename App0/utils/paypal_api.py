from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from django.conf import settings

import sys, json

class PayPalClient:
	def __init__(self):
		self.client_id = settings.PAYPAL_CLIENT_ID
		self.client_secret = settings.PAYPAL_CLIENT_SECRET

		"""Set up and return PayPal Python SDK environment with PayPal access credentials.
		   This sample uses SandboxEnvironment. In production, use LiveEnvironment."""

		self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)

		""" Returns PayPal HTTP client instance with environment that has access
			credentials context. Use this instance to invoke PayPal APIs, provided the
			credentials have access. """
		self.client = PayPalHttpClient(self.environment)

	def object_to_json(self, json_data):
		"""
		Function to print all json data in an organized readable manner
		"""

		print(json_data)
		result = {}
		if sys.version_info[0] < 3:
			itr = json_data.__dict__.iteritems()
		else:
			itr = json_data.__dict__.items()
		for key,value in itr:
			# Skip internal attributes.
			if key.startswith("__"):
				continue
			result[key] = self.array_to_json_array(value) if isinstance(value, list) else\
						self.object_to_json(value) if not self.is_primittive(value) else\
						 value
		return result;
	def array_to_json_array(self, json_array):
		result =[]
		if isinstance(json_array, list):
			for item in json_array:
				result.append(self.object_to_json(item) if  not self.is_primittive(item) \
							  else self.array_to_json_array(item) if isinstance(item, list) else item)
		return result;

	def is_primittive(self, data):
		return isinstance(data, str) or isinstance(data, unicode) or isinstance(data, int)


# 1. Import the PayPal SDK client that was created in `Set up Server-Side SDK`.
#from sample import PayPalClient
from paypalcheckoutsdk.payments import CapturesRefundRequest
import json

class RefundOrderV1(PayPalClient):

	#2. Set up your server to receive a call from the client
	"""Use the following function to refund an capture.
		Pass a valid capture ID as an argument."""
	def refund_order(self, capture_id, debug=False, refund=0):
		request = CapturesRefundRequest(capture_id)
		request.prefer("return=representation")
		request.request_body(self.build_request_body(refund))
		#3. Call PayPal to refund an capture
		response = self.client.execute(request)
		if debug:
			print(f"Status Code: {response.status_code}")
			print(f"Status: {response.result.status}")
			print(f"Order ID: {response.result.id}")
			print(f"Links: ")
			for link in response.result.links:
				print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
			json_data = self.object_to_json(response.result)
			print(f"json_data: {json.dumps(json_data,indent=4)}")
		return response

	"""Request body for building a partial refund request.
		For full refund, pass the empty body.
		For more details, refer to the Payments API refund captured payment reference."""
	@staticmethod
	def build_request_body(refund=0):
		return \
		{
			"amount": {
			"value": refund,
			"currency_code": "USD"
			}
		}

"""This driver function invokes the refund capture function.
   Replace the Capture Id with a valid capture ID. """

# Get the Order
from paypalcheckoutsdk.orders import OrdersGetRequest
#from .models import u_orders

class GetOrder(PayPalClient):

	#2. Set up your server to receive a call from the client
	"""You can use this function to retrieve an order by passing order ID as an argument"""   
	def get_order(self, order_id):
		"""Method to get order"""
		request = OrdersGetRequest(order_id)
		#3. Call PayPal to get the transaction
		response = self.client.execute(request)
		#print(json.dumps(str(response.result.__dict__["_dict"]), indent=4).replace("},", "},\n"))
		#print("Purcase Units")
		#print(json.loads(json.dumps(str(response.result.purchase_units[0].__dict__), indent=4)))
		#4. Save the transaction in your database. Implement logic to save transaction to your database for future reference.
		#print(f'Status Code: {response.status_code}')
		#print(f'Status: {response.result.status}')
		#print(f'Order ID: {response.result.id}')
		#print(f'Intent: {response.result.intent}')
		#print('Links:')
		#for link in response.result.links:
		#	print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
		#print('Gross Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code,
		#					response.result.purchase_units[0].amount.value))
		return response.result.__dict__["_dict"]

"""This driver function invokes the get_order function with
   order ID to retrieve sample order details. """
#if __name__ == '__main__':
#	GetOrder().get_order('4MN163138R741484E')

# Used to authorize the payment
from paypalcheckoutsdk.payments import AuthorizationsCaptureRequest
import json

class CaptureAuthorization(PayPalClient):

  #2. Set up your server to receive a call from the client
  """Use this function to capture an approved authorization.
     Pass a valid authorization ID as an argument to this function."""
  def capture_auth(self, authorization_id, debug=False):
    """Method to capture order using authorization_id"""
    request = AuthorizationsCaptureRequest(authorization_id)
    request.request_body(self.build_request_body())
    # 3. Call PayPal to capture an authorization.
    response = self.client.execute(request)
    #print(json.dumps(str(response.result.__dict__), indent=4).replace("},", "},\n"))
    # 4. Save the capture ID to your database for future reference.
    if debug:
      print(f'Status Code: {response.status_code}')
      print(f'Status: {response.result.status}')
      print(f'Capture ID: {response.result.id}')
      print('Links: ')
      for link in response.result.links:
        print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
      json_data = str(response.result.__dict__)
      print(f"json_data: {json.dumps(json_data,indent=4)}")
    return response

  """Sample request body to Capture Authorization."""
  @staticmethod
  def build_request_body():
    return {}


"""This driver function invokes the capture order function with
   a valid authorization ID to capture. Replace the auth_id value with
   a valid authorization ID"""
#if __name__ == "__main__":
#  auth_id = "2BR41489XA899643C"
#  CaptureAuthorization().capture_auth(auth_id, debug=True)
