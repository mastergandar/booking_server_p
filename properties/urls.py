from django.urls import path
from rest_framework import routers

from properties.views import PropertiesListView, PropertiesListCreateView, PropertyUpdateRetrieveDeleteView, \
    PropertyCancelView, PropertyOrderView, PropertiesRecommendationView, AmenitiesListView, AmenitiesRetrieveView, \
    PropertyOccupationView, PropertiesArchiveView, PropertiesPromotionView

app_name = 'Properties api'

router = routers.SimpleRouter()

urlpatterns = [
    path('', PropertiesListView.as_view(), name='properties_list'),
    path('my', PropertiesListCreateView.as_view(), name='my_properties_list_create'),
    path('amenities', AmenitiesListView.as_view(), name='amenities_list'),
    path('my_orders', PropertyOrderView.as_view(), name='my_orders'),
    path('occupations', PropertyOccupationView.as_view(), name='occupations'),
    path('promotion', PropertiesPromotionView.as_view(), name='promotion'),
    path('<int:pk>', PropertyUpdateRetrieveDeleteView.as_view(), name='property_retrieve_update_delete'),
    path('<int:pk>/order', PropertyOrderView.as_view(), name='property_order'),
    path('<int:pk>/cancel', PropertyCancelView.as_view(), name='property_cancel'),
    path('<int:pk>/archive', PropertiesArchiveView.as_view(), name='property_archive'),
    path('<int:pk>/recomendation', PropertiesRecommendationView.as_view(), name='properties_recommendation'),
    path('amenities/<int:pk>', AmenitiesRetrieveView.as_view(), name='amenities_retrieve'),
]

urlpatterns += router.urls
