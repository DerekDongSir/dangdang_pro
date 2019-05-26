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

def delete_book(request):
    book_id = request.GET.get('book_id')
    book = BookInfo.objects.get(id=book_id)
    # book.delete()
    return HttpResponse('ok')


def add_parent_type(request):
    return render(request,'manageapp/add_parent_type.html')


def add_parent_type_logic(request):
    '''
    :param request:接收到的父类名称
    :return:
    '''
    type_name = request.GET.get('type_name') # 将父类名称添加入类别库中
    # print(type_name)

    return HttpResponse('ok')


def add_book_type(request):
    parents = request.session.get('parents')
    if not parents:
        parents = TCatogray.objects.filter(parent_id=None)
        request.session['parents'] = parents
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
    catogray = request.session.get('catogray')
    if not catogray:
        catogray = TCatogray.objects.filter(parent_id__isnull=False)#筛选出所有的二级类
        request.session['catogray'] = catogray
    return render(request,'manageapp/add_book.html',{'catogray':catogray})


def add_book_logic(request):
    book_name = request.GET.get('book_name')
    author = request.GET.get('author')
    press = request.GET.get('press')
    catogray_id = request.GET.get('catogray_id')
    publish_time = request.GET.get('publish_time')
    # print(catogray_id)
    return HttpResponse('ok')


def location(request):
    page_num = int(request.GET.get('page_num',1))
    locations = request.session.get('locations')
    if not locations:
        locations = TDelivery.objects.filter(torder__create_time__isnull=False) #筛选出创建过订单的用户地址信息
        request.session['locations'] = locations
    paginator = Paginator(locations,per_page=10)
    page = paginator.page(page_num)
    location_dict ={ location.torder_set.all()[0].create_time:location for location in page }
    return render(request,'manageapp/location.html',{'page':page,'location_dict':location_dict})


