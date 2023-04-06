from django.urls import path
from rest_framework import routers

from social.views import ReviewCreateView, ReviewsListView, ReviewUpdateRetrieveView, ReportCreateView, \
    ReportRetrieveUpdateView, ReportsListView, FavoriteListCreateView, FavoriteRetrieveDestroyView, \
    ReportMessagesListView

app_name = 'Social api'

router = routers.SimpleRouter()

urlpatterns = [
    path('create', ReviewCreateView.as_view(), name='review_create'),
    path('report_create', ReportCreateView.as_view(), name='report_create'),
    path('favorite', FavoriteListCreateView.as_view(), name='favorite_list_create'),
    path('favorite/<int:pk>', FavoriteRetrieveDestroyView.as_view(), name='favorite_retrieve_destroy'),
    path('<int:pk>', ReviewUpdateRetrieveView.as_view(), name='review_retrieve_update'),
    path('report/<int:pk>', ReportRetrieveUpdateView.as_view(), name='report_retrieve_update'),
    path('report/<int:pk>/messages', ReportMessagesListView.as_view(), name='report_messages_list'),
    path('<str:content_type>', ReviewsListView.as_view(), name='review_list'),
    path('report/<str:content_type>', ReportsListView.as_view(), name='report_list'),
]

urlpatterns += router.urls
