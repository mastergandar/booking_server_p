from django.urls import path
from rest_framework import routers

from file_manager.views import LinkedImagesListCreateView, LinkedImagesRetrieveView

app_name = 'Properties api'

router = routers.SimpleRouter()

urlpatterns = [
    path('image', LinkedImagesListCreateView.as_view(), name='image_list_create'),
    path('image/<int:pk>', LinkedImagesRetrieveView.as_view(), name='image_retrieve_update'),
]

urlpatterns += router.urls
