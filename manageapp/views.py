from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render,redirect,HttpResponse
from bookapp.models import BookInfo,TDelivery,TCatogray
# Create your views here.

def index(request):
    return render(request,'manageapp/index.html')


def booklist(request):
    page_num = int(request.GET.get('page_num',1))
    """
    :return: 将联合查询的书籍的种类名作为键，书籍作为值，构成字典传递到前端
    """
    all_books = BookInfo.objects.all()
    # books ={book.catogray.catogry_name:book for book in BookInfo.objects.all()}
    paginator = Paginator(all_books,per_page=20)
    page = paginator.page(page_num)
    book_dic = {book.catogray.catogry_name:book for book in page}
    return render(request, 'manageapp/bookIist.html',{'page':page,'book_dic':book_dic})


def add_parent_type(request):
    return render(request,'manageapp/add_parent_type.html')


def add_book_type(request):
    parents = TCatogray.objects.filter(parent_id=None)
    return render(request,'manageapp/add_book_type.html',{"parents":parents})

def add_book_type_logic(request):
    type_name = request.GET.get('t_name')
    num = request.GET.get('number')
    parent_id = request.GET.get('parent')
    # print(type_name,num,parent_id)
    return HttpResponse('添加成功！')


def book_id(request):
    page_num = int(request.GET.get('page_num',1))
    paginator = Paginator(BookInfo.objects.all(),per_page=15)
    page = paginator.page(page_num)
    return render(request,'manageapp/book_id.html',{'page':page})


def add_book(request):
    return render(request,'manageapp/add_book.html')


def location(request):
    return render(request,'manageapp/location.html')


