from django.urls import path
from manageapp import views
app_name ='manageapp'
urlpatterns = [
    path('index/',views.index,name='index'),
    path('booklist/',views.booklist,name='booklist'),
    path('add_book/',views.add_book,name='add_book'),
    path('add_book_type/',views.add_book_type,name='add_book_type'),
    path('add_book_type_logic/',views.add_book_type_logic,name='add_book_type_logic'),
    path('add_parent_type/',views.add_parent_type,name='add_parent_type'),
    path('book_id/',views.book_id,name='book_id'),
    path('location/',views.location,name='location'),
]