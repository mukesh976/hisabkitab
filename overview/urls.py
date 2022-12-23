from django.urls import path

# from . import views
from .views import category_data, date_catg_wise_data, date_wise_data, overview

urlpatterns = [
    path('', overview, name='overview'),
    path('category_data/', category_data, name='category_data'),
    path('date_wise/', date_wise_data, name='date_wise'),
    path('dt_catg/', date_catg_wise_data, name='date_catg_wise'),
]