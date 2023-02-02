from django.urls import path

# from . import views
from .views import add_item, category_data, date_catg_wise_data,date_wise_data, overview,count_itm,update_item,cunt_itm_latest_date,date_max_itm_price,latest_date,Particular_date_data
urlpatterns = [
    path('', overview, name='overview'),
    path('category_data/', category_data, name='category_data'),
    path('date_wise/', date_wise_data, name='date_wise'),
    path('dt_catg/', date_catg_wise_data, name='date_catg_wise'),
    path('add-item/', add_item, name='add-item'),
    path('update-item/', update_item, name='update-item'),
    path('cont_itm_price/',count_itm,name='count_itm'),
    path('cont_itm_latst_date/',cunt_itm_latest_date,name='cunt_itm_latest_date'),
    path('date_max_itm_price/',date_max_itm_price,name='date_max_itm_price'),
    path('lat_dat/',latest_date,name='latest_date'),
    path('partic_det_data/',Particular_date_data,name='Particular_date_data'),

]