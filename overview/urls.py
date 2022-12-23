from django.urls import path

# from . import views
from .views import category_data, overview

urlpatterns = [
    path('', overview, name='overview'),
    path('category_data/', category_data, name='category_data'),
]