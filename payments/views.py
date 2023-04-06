from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from payments.utils import PaymentService, RobokassaPaymentService


class BalanceUpdateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        PaymentService().account_balance_update(request)


class PaymentSuccessView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return RobokassaPaymentService().check_success_payment(request)


class PaymentFailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return RobokassaPaymentService().check_fail_payment(request)


class PaymentResultView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return RobokassaPaymentService().result_payment(request)
