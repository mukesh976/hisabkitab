from django.urls import path

# from . import views
from .views import add_item, category_data, date_catg_wise_data,date_wise_data, overview,count_itm,update_item,cunt_itm_price,date_max_itm_price,latest_date,Particular_date_data,filter_catg,find_items_today
urlpatterns = [
    path('', overview, name='overview'),
    path('category-data/', category_data, name='category-data'),
    path('date-wise/', date_wise_data, name='date-wise'),
    path('dt-catg/', date_catg_wise_data, name='date-catg-wise'),
    path('add-item/', add_item, name='add-item'),
    path('update-item/', update_item, name='update-item'),
    path('cont-itm-price/',count_itm,name='count-itm'),
    path('cont-itm/',cunt_itm_price,name='cunt-itm-latest-date'),
    path('date-max-itm-price/',date_max_itm_price,name='date-max-itm-price'),
    path('lat-dat/',latest_date,name='latest-date'),
    path('partic-det-data/',Particular_date_data,name='Particular-date-data'),
    path('filter-catg/',filter_catg,name='filter-catg'),
    #path('find-items-today/',find_items_today,name='find_items_today')


]