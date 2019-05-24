from django.urls import path
from orderapp import views
app_name = 'orderapp'
urlpatterns = [
    path('cart_page/',views.cart_page,name='cart_page'),
    path('add_to_cart/',views.add_to_cart,name='add_to_cart'),
    path('remove_from_cart/',views.remove_from_cart,name='remove_from_cart'),
    path('book_num_adjust/',views.book_num_adjust,name='book_num_adjust'),
    path('all_operation/',views.all_operation,name='all_operation'),
    path('indent/',views.indent,name='indent'),
    path('get_delivery_info/',views.get_delivery_info,name='get_delivery_info'),
    path('get_location_info/',views.get_location_info,name='get_locaton_info'),
    path('get_city/',views.get_city,name='get_city'),
    path('get_town/',views.get_town,name='get_town'),
    path('check_address/',views.check_address,name='check_address'),
    path('location_info/',views.location_info,name='location_info'),
    path('indent_ok/',views.indent_ok,name='indent_ok'),
]