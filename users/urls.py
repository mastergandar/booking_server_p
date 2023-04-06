from django.urls import path
from rest_framework import routers

from users.views import UserCreateView, UserMeRetrieveUpdateView, UserViewDestroyView, UserActivateView

app_name = 'Users api'

router = routers.SimpleRouter()


urlpatterns = [
    path('register', UserCreateView.as_view(), name='register'),
    path('register/<int:uid>/<str:token>', UserActivateView.as_view(), name='activate_account'),
    path('me', UserMeRetrieveUpdateView.as_view(), name='me'),
    path('<int:pk>', UserViewDestroyView.as_view(), name='user_view'),
]

urlpatterns += router.urls
