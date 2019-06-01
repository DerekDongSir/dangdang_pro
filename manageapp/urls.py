from django.urls import path
from manageapp import views
app_name ='manageapp'
urlpatterns = [
    path('index/',views.index,name='index'),
    path('booklist/',views.booklist,name='booklist'),
    path('delete_book/',views.delete_book,name="delete_book"),
    path('mass_delete/',views.mass_delete,name='mass_delete'),
    path('add_book/',views.add_book,name='add_book'),
    path('add_book_logic/',views.add_book_logic,name='add_book_logic'),
    path('add_book_type/',views.add_book_type,name='add_book_type'),
    path('add_book_type_logic/',views.add_book_type_logic,name='add_book_type_logic'),
    path('add_parent_type/',views.add_parent_type,name='add_parent_type'),
    path('add_parent_type_logic/',views.add_parent_type_logic,name='add_parent_type_logic'),
    path('book_id/',views.book_id,name='book_id'),
    path('location/',views.location,name='location'),
    path('add_location/',views.add_location,name='add_location'),
    path('add_location_logic/',views.add_location_logic,name='add_location_logic'),
    path('catogray_num-pie/',views.catogray_num_pie,name='catogray_num_pie'),# 图书数量大饼图
]