from django.urls import path

# from . import views
from .views import add_item, category_data, date_catg_wise_data, date_wise_data, overview, update_item

urlpatterns = [
    path('', overview, name='overview'),
    path('category_data/', category_data, name='category_data'),
    path('date_wise/', date_wise_data, name='date_wise'),
    path('dt_catg/', date_catg_wise_data, name='date_catg_wise'),
    path('add-item/', add_item, name='add-item'),
    path('update-item/', update_item, name='update-item')

]