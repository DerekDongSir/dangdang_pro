import uuid

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render,redirect,HttpResponse
from pyecharts.charts import Pie,Page
from pyecharts import options as opts

from bookapp.models import BookInfo,TDelivery,TCatogray,TOrder
# Create your views here.

def index(request):
    return render(request,'manageapp/index.html')


def booklist(request):
    all_books = BookInfo.objects.all()
    book_id = request.GET.get('book_id') # 从 book_id页面通过点击 更多 进入此页面
    if book_id:
        all_books = BookInfo.objects.filter(id=book_id) # 此时，仅显示被选中的书籍
    page_num = int(request.GET.get('page_num',1)) #在booklist页面内进行跳转
    """
    :return: 将联合查询的书籍的种类名作为键，书籍作为值，构成字典传递到前端
    """
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

def mass_delete(request):
    '''接收前端传递的拼接后的id字符串，进行拆分，取出单个id'''
    ids = request.GET.get('ids')
    id_ls =ids.split('/') #获得书籍的id列表
    return HttpResponse('ok')


def add_parent_type(request):
    return render(request,'manageapp/add_parent_type.html')


def add_parent_type_logic(request):
    '''接收到的父类名称,查询数据库该名称是否已经存在，不存在则添加'''
    type_name = request.GET.get('type_name') # 将父类名称添加入类别库中
    if TCatogray.objects.filter(catogry_name=type_name):
        return HttpResponse('failed')
    #由于建表时采用integer作为primary key数据类型，因而此时不能使用 uuid 来生成 id
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
    parent_id = int(request.GET.get('parent'))
    if TCatogray.objects.filter(parent_id=parent_id,catogry_name=type_name):
        return HttpResponse('failed')
    return HttpResponse('ok')


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


def add_location(request):
    return  render(request,'manageapp/add_location.html')

def add_location_logic(request):
    location_id = request.GET.get("location_id")
    user_name = request.GET.get("user_name")
    receiver = request.GET.get("receiver")
    phone = request.GET.get("phone")
    crate_time = request.GET.get("crate_time")
    send_time = request.GET.get("send_time")
    receive_time = request.GET.get("receive_time")
    return HttpResponse('ok')


def catogray_num_pie(request):
    '''
     #catogray 是一个一级类的字典，键为 类id，每个键对应的值为一个列表
            #列表第一项为该类下共有多少本图书，第二项为类名,第三项为该类对应的二级类字典
            #二级类字典 键为 类id，值为列表，列表第一项为该二级类下的书的数量，第二项为类名
    '''
    catogray = request.session.get('catogray')
    def pie_base() -> Pie:
        c = (
            Pie()
                .add("", [[item[1],item[0]] for item in catogray.values()])
                .set_global_opts(title_opts=opts.TitleOpts(title="图书类别统计"))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )
        return c
    c = pie_base()
    return HttpResponse(c.render_embed()) # 将一级类图书类别和数量以大饼图的形式内嵌在网页中
