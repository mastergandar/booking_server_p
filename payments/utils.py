import base64
import datetime
import decimal
import hashlib
import json
from urllib import parse
from urllib.parse import urlparse

import requests
from django.db.models import Sum

from core.settings.common import M_PESA_AUTH_END, M_PESA_ONLINE_END, M_PESA_CONSUMER_KEY, M_PESA_CONSUMER_SECRET, \
    M_PESA_SHORT_CODE, M_PESA_KEY, M_PESA_B2C_END, M_PESA_BALANCE_END, ROBOKASSA_LOGIN, ROBOKASSA_PASSWORD1, \
    ROBOKASSA_PASSWORD2, ROBOKASSA_TEST_MODE, ROBOKASSA_CURRENCY, ROBOKASSA_LANGUAGE, ROBOKASSA_ENCODING, \
    ROBOKASSA_PAYMENT_URL, ROBOKASSA_SUCCESS_URL, ROBOKASSA_FAIL_URL, ROBOKASSA_RESULT_URL
from payments.models import Payments, Withdraw, CompanyBalance

session = requests.session()


class PaymentService:

    def __init__(self):
        self.headers = self.get_headers()
        self.sec_cred = "BAdd58r2fx+Erypbz4i5vHcA2lD3MhwaTQQpAejOZal5OKszHn/nPyq/j6oGTADhjwizBAi+BEJpSDl8l3I/eLpUG/CXW3Z/40JJFFmfBDpWRrzzfUtDpK5ptuI8i8SPzmR45U/vL9yoSRMafUZEVkuz6XYginjxHFURnGTPHh3MIkVb6RkdypOqNhT0uV4nGWJ1HgCeREcx5Zsgu9dXyIohRiWX3TgT2LZvXIx00FuU6nYncCzu4XcEYPCbjUIb4sOpuc1fbxzCTR4NIN0wR/tpAZzffb1N5T8VArJtzKiu1wQq/PWp1ukefgeXOAq8m3pY4UqxNuh/ZFm4LKUzeA=="

    @staticmethod
    def auth():
        session.auth = (M_PESA_CONSUMER_KEY, M_PESA_CONSUMER_SECRET)
        token_response = session.get(url=M_PESA_AUTH_END)
        print(token_response.content)
        token = json.loads(token_response.content)['access_token']
        print(token)
        return token

    def get_headers(self):
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.auth()}'}
        return headers

    def validate_request_type(self, url, request_type):
        if url == M_PESA_AUTH_END and not request_type == 'GET':
            return False
        elif url == M_PESA_ONLINE_END and not request_type == 'POST':
            return False
        return True

    def validate_data(self, url, data):
        valid_data = {
            "BusinessShortCode": str,
            "Password": str,
            "Timestamp": str,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": str,
            "PartyA": str,
            "PartyB": str,
            "PhoneNumber": str,
            "CallBackURL": str,
            "AccountReference": str,
            "TransactionDesc": str
        }
        b2c_valid_data = {
            "InitiatorName": str,  # The username of the M-Pesa B2C
            "SecurityCredential": str,  # This is the value obtained after encrypting the API initiator password
            "CommandID": "BusinessPayment",
            "Amount": str,
            "PartyA": str,
            "PartyB": str,
            "Remarks": str,
            "QueueTimeOutURL": str,
            "ResultURL": str,
            "Occasion": str
        }
        if url == M_PESA_AUTH_END:
            pass
        elif url == M_PESA_ONLINE_END and not data:
            for key, value in valid_data.items():
                if type(data[key]) is not value:
                    return False
        elif url == M_PESA_B2C_END and not data:
            for key, value in b2c_valid_data.items():
                if type(data[key]) is not value:
                    return False
        return True

    def validate_withdraw(self, withdraw_data):
        validate_data = {
            "InitiatorName":  "testapi",   # The username of the M-Pesa B2C
            "SecurityCredential": self.sec_cred,  # This is the value obtained after encrypting the API initiator password
            "CommandID": "AccountBalance",
            "PartyA": M_PESA_SHORT_CODE,
            "IdentifierType": 4,
            "Remarks": "Test",  # TODO: Change later
            "QueueTimeOutURL": str,
            "ResultURL": str,
        }
        income_sum = Payments.objects.all().aggregate(Sum('amount'))['amount__sum']
        outcome_sum = Withdraw.objects.all().aggregate(Sum('amount'))['amount__sum']
        response = self.request(M_PESA_BALANCE_END, 'POST', validate_data).content
        balance = json.loads(response)['Result']['Balance']
        if income_sum - outcome_sum != 0:
            return False
        return True

    def account_balance_update_call(self, data):
        response = self.request(M_PESA_BALANCE_END, 'POST', data).content
        return response

    @staticmethod
    def account_balance_update(request):
        balance = json.loads(request.content)['Result']['Balance']
        if CompanyBalance.objects.all().exists():
            CompanyBalance.objects.all().update(amount=balance)
        else:
            CompanyBalance.objects.create(amount=balance)

    def validate(self, url, request_type, data):
        if self.validate_request_type(url, request_type) and self.validate_data(url, data):
            return True
        return False

    def request(self, url, request_type, data):
        resp = None
        if request_type == 'POST':
            resp = requests.request("POST", url=url, headers=self.headers, data=json.dumps(data))
        elif request_type == 'GET':
            resp = requests.request("POST", url=url, headers=self.headers)
        return resp

    def make_pass(self, timestamp):
        password = base64.b64encode(bytes(M_PESA_SHORT_CODE + M_PESA_KEY + timestamp, 'utf-8')).decode()
        return password

    def online_payment(self, order_data):
        timestamp = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        """
        transaction_body = {
            "BusinessShortCode": M_PESA_SHORT_CODE,
            "Password": self.make_pass(timestamp),
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": "1",
            "PartyA": "254705912645",
            "PartyB": M_PESA_SHORT_CODE,
            "PhoneNumber": "254705912645",
            "CallBackURL": "https://mydomain.com/path",
            "AccountReference": "Test",
            "TransactionDesc": "Test"
        }
        """
        transaction_body = {
            "BusinessShortCode": M_PESA_SHORT_CODE,
            "Password": self.make_pass(timestamp),
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": order_data['amount'],
            "PartyA": order_data['party_a'],  # Same as PhoneNumber
            "PartyB": M_PESA_SHORT_CODE,
            "PhoneNumber": order_data['phone_number'],  # Same as PartyA
            "CallBackURL": order_data['call_back'],
            "AccountReference": order_data['reference'],
            "TransactionDesc": order_data['description']
        }
        is_valid = self.validate(M_PESA_ONLINE_END, "POST", transaction_body)
        if is_valid:
            resp = self.request(M_PESA_ONLINE_END, "POST", transaction_body)
            return resp

    def withdraw(self, withdraw_data):
        transaction_body = {
            "InitiatorName": "testapi",  # The username of the M-Pesa B2C
            "SecurityCredential": self.sec_cred,  # This is the value obtained after encrypting the API initiator password
            "CommandID": "BusinessPayment",
            "Amount": withdraw_data['amount'],
            "PartyA": M_PESA_SHORT_CODE,
            "PartyB": withdraw_data['party_a'],
            "Remarks": "",
            "QueueTimeOutURL": "",
            "ResultURL": "",
            "Occasion": "Roompesa withdraw"
        }
        is_valid = self.validate(M_PESA_B2C_END, "POST", transaction_body)
        if is_valid and self.validate_withdraw(withdraw_data):
            resp = self.request(M_PESA_B2C_END, "POST", transaction_body)
            return resp

    def save_callback(self, metadata, result_code):
        if metadata:
            date = datetime.datetime.strptime(metadata['TransactionDate'], "%Y%m%d%H%M%S")
            Payments.objects.create(
                # amount=metadata['Amount'],
                receipt_number=metadata['MpesaReceiptNumber'],
                transaction_date=date,
                # phone_number=metadata['PhoneNumber'],
                result_code=result_code
            )
        else:
            Payments.objects.create(
                result_code=result_code
            )

    def callback(self, data):
        callback = data['Body']['stkCallback']
        if callback['ResultCode'] == 0:
            metadata = callback['CallbackMetadata']['Item']
            self.save_callback(metadata, 0)
        else:
            self.save_callback(None, callback['ResultCode'])


class RobokassaPaymentService:
    def __init__(self):
        self.merchant_login = ROBOKASSA_LOGIN
        self.merchant_password1 = ROBOKASSA_PASSWORD1
        self.merchant_password2 = ROBOKASSA_PASSWORD2
        self.merchant_test_mode = ROBOKASSA_TEST_MODE
        self.merchant_currency = ROBOKASSA_CURRENCY
        self.merchant_language = ROBOKASSA_LANGUAGE
        self.merchant_encoding = ROBOKASSA_ENCODING
        self.merchant_payment_url = ROBOKASSA_PAYMENT_URL
        self.merchant_success_url = ROBOKASSA_SUCCESS_URL
        self.merchant_fail_url = ROBOKASSA_FAIL_URL
        self.merchant_result_url = ROBOKASSA_RESULT_URL

    def calculate_signature(*args) -> str:
        """Create signature MD5"""
        return hashlib.md5(':'.join(str(arg) for arg in args).encode()).hexdigest()

    @staticmethod
    def parse_response(request: str) -> dict:
        """
        :param request: Link.
        :return: Dictionary.
        """
        params = {}

        for item in urlparse(request).query.split('&'):
            key, value = item.split('=')
            params[key] = value
        return params

    def check_signature_result(
            self,
            order_number: int,  # invoice number
            received_sum: decimal,  # cost of goods, RU
            received_signature: hex,  # SignatureValue
            password: str  # Merchant password
    ) -> bool:
        signature = self.calculate_signature(received_sum, order_number, password)
        if signature.lower() == received_signature.lower():
            return True
        return False

    # Формирование URL переадресации пользователя на оплату.

    def generate_payment_link(
            self,
            cost: decimal,  # Cost of goods, RU
            number: int,  # Invoice number
            description: str,  # Description of the purchase
            is_test=0,
    ) -> str:
        """URL for redirection of the customer to the service"""
        signature = self.calculate_signature(
            self.merchant_login,
            cost,
            number,
            self.merchant_password1
        )

        data = {
            'MerchantLogin': self.merchant_login,
            'OutSum': cost,
            'InvId': number,
            'Description': description,
            'SignatureValue': signature,
            'IsTest': is_test
        }
        return f'{self.merchant_payment_url}?{parse.urlencode(data)}'

    # Получение уведомления об исполнении операции (ResultURL).
    def result_payment(self, request: str) -> str:
        """Verification of notification (ResultURL).
        :param request: HTTP parameters.
        """
        param_request = self.parse_response(request)
        cost = param_request['OutSum']
        number = param_request['InvId']
        signature = param_request['SignatureValue']

        if self.check_signature_result(number, cost, signature, self.merchant_password2):
            return f'OK{param_request["InvId"]}'
        return "bad sign"

    # Проверка параметров в скрипте завершения операции (SuccessURL).

    def check_success_payment(self, request: str) -> str:
        """ Verification of operation parameters ("cashier check") in SuccessURL script.
        :param request: HTTP parameters
        """
        param_request = self.parse_response(request)
        cost = param_request['OutSum']
        number = param_request['InvId']
        signature = param_request['SignatureValue']

        if self.check_signature_result(number, cost, signature, self.merchant_password1):
            return "Thank you for using our service"
        return "bad sign"

    def check_fail_payment(self, request: str) -> str:
        """ Verification of operation parameters ("cashier check") in FailURL script.
        :param request: HTTP parameters
        """
        param_request = self.parse_response(request)
        cost = param_request['OutSum']
        number = param_request['InvId']
        signature = param_request['SignatureValue']

        if self.check_signature_result(number, cost, signature, self.merchant_password1):
            return "Thank you for using our service"
        return "bad sign"

    """    
    def get_payment_url(self, out_sum, inv_id):
        return f'https://auth.robokassa.ru/Merchant/Index.aspx?MrchLogin={self.merchant_login}&' \
               f'OutSum={out_sum}&InvId={inv_id}&Desc={inv_id}&SignatureValue={self.calculate_signature(out_sum, inv_id)}&' \
               f'IncCurrLabel={self.merchant_currency}&Culture={self.merchant_language}&Encoding={self.merchant_encoding}'

    def check_payment(self, out_sum, inv_id, signature):
        return signature == self.calculate_signature(out_sum, inv_id)

    def save_payment(self, out_sum, inv_id, signature):
        if self.check_payment(out_sum, inv_id, signature):
            Payments.objects.create(
                amount=out_sum,
                receipt_number=inv_id,
                result_code=0
            )
        else:
            Payments.objects.create(
                amount=out_sum,
                receipt_number=inv_id,
                result_code=1
            )

    def get_success_url(self, out_sum, inv_id, signature):
        return f'{self.merchant_success_url}?InvId={inv_id}&SignatureValue={signature}&' \
                f'OutSum={out_sum}&Culture={self.merchant_language}&Encoding={self.merchant_encoding}'
    """

