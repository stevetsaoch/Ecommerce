import sys
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from private_info import private_info

PrivateInfo = private_info()

class PayPalClient():
    def __init__(self):
        self.client_id = PrivateInfo.paypal_info(mode='sandbox_payment')['client_id']
        self.client_secret = PrivateInfo.paypal_info(mode='sandbox_payment')['client_secret']
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)
