from django.urls import path

from websocketing.consumers import ReportConsumer

urlpatterns = [
    path('ws/<str:report_id>', ReportConsumer.as_asgi()),
    # path('ws/notify/<str:user_token>', NotifyConsumer.as_asgi()),
]
