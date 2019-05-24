from django.urls import path,re_path
from bookapp import views
app_name = 'bookapp'
urlpatterns = [
    path('index/',views.index,name='index'),
    path('booklist/',views.booklist,name='booklist'),
    path('book_details/',views.book_details,name='book_details'),
    path('book_sort/',views.book_sort,name='book_sort'),
]