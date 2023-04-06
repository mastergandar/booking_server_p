from django.urls import path
from rest_framework import routers

from payments.views import BalanceUpdateView, PaymentSuccessView, PaymentFailView, PaymentResultView
from properties.views import PropertiesListView, PropertiesListCreateView

app_name = 'Properties api'

router = routers.SimpleRouter()

urlpatterns = [
    path('balance_update', BalanceUpdateView.as_view(), name='balance_update'),
    path('success', PaymentSuccessView.as_view(), name='payment_success'),
    path('fail', PaymentFailView.as_view(), name='payment_fail'),
    path('result', PaymentResultView.as_view(), name='payment_result'),
]

urlpatterns += router.urls
