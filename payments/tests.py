import json

import pytest

from core.settings.common import M_PESA_SHORT_CODE
from payments.models import CompanyBalance
from payments.utils import PaymentService


"""@pytest.mark.django_db
def test_payment_service_auth():
    payment_auth = PaymentService()
    assert len(payment_auth.headers['Authorization'].split(' ')[1]) != 0


@pytest.mark.django_db
def test_payment_online():
    data = {
        "TransactionType": "CustomerPayBillOnline",
        "amount": "1",
        "party_a": "254705912645",  # Same as PhoneNumber
        "phone_number": "254705912645",  # Same as PartyA
        "call_back": "https://mydomain.com/path",
        "reference": "Test",
        "description": "Test"
    }
    service = PaymentService()
    response = service.online_payment(data)
    assert response.status_code == 200
    assert json.loads(response.content)['CustomerMessage'] == 'Success. Request accepted for processing'


@pytest.mark.django_db
def test_account_balance():
    sec_cred = "BAdd58r2fx+Erypbz4i5vHcA2lD3MhwaTQQpAejOZal5OKszHn/nPyq/j6oGTADhjwizBAi+BEJpSDl8l3I/eLpUG/CXW3Z/40JJFFmfBDpWRrzzfUtDpK5ptuI8i8SPzmR45U/vL9yoSRMafUZEVkuz6XYginjxHFURnGTPHh3MIkVb6RkdypOqNhT0uV4nGWJ1HgCeREcx5Zsgu9dXyIohRiWX3TgT2LZvXIx00FuU6nYncCzu4XcEYPCbjUIb4sOpuc1fbxzCTR4NIN0wR/tpAZzffb1N5T8VArJtzKiu1wQq/PWp1ukefgeXOAq8m3pY4UqxNuh/ZFm4LKUzeA=="
    data = {
            "InitiatorName":  "testapi",   # The username of the M-Pesa B2C
            "SecurityCredential": sec_cred,  # This is the value obtained after encrypting the API initiator password
            "CommandID": "AccountBalance",
            "PartyA": M_PESA_SHORT_CODE,
            "IdentifierType": 4,
            "Remarks": "Test",  # TODO: Change later
            "QueueTimeOutURL": "https://mydomain.com/path",
            "ResultURL": "https://localhost/payments/balance_update",
        }
    service = PaymentService()
    print(service.account_balance_update_call(data))
    CompanyBalance.objects.create(amount=0)
    CompanyBalance.objects.get(pk=1)
    print(CompanyBalance.objects.get(pk=1).amount)"""
