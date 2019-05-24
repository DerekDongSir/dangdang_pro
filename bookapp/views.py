from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,redirect
from bookapp.models import BookInfo,TCatogray
# Create your views here.

def index(request):
    catogray = request.session.get('catogray') #首先从session中获取分类信息，若没有，则从数据库中查找
    if not catogray:
        catogray_one = TCatogray.objects.filter(parent_id__isnull=True).values()
        catogray_one_name = [val['catogry_name'] for val in catogray_one]
        catogray_one_id = [val['id'] for val in catogray_one]
        catogray = {}
        for name,id in zip(catogray_one_name,catogray_one_id):
            total_count,name_ls,count_ls,id_ls = 0,[],[],[]
            for val in TCatogray.objects.filter(parent_id=id):
                name_ls.append(val.catogry_name)
                id_ls.append(val.id)
                sub_count = BookInfo.objects.filter(catogray=val.id).count()
                count_ls.append(sub_count)
                total_count += sub_count
            #catogray 是一个一级类的字典，键为 类id，每个键对应的值为一个列表
            #列表第一项为该类下共有多少本图书，第二项为类名,第三项为该类对应的二级类字典
            #二级类字典 键为 类id，值为列表，列表第一项为该二级类下的书的数量，第二项为类名
            catogray[id] = [total_count,name,{ sub_id:[sub_count,name] for name,sub_count,sub_id in zip(name_ls,count_ls,id_ls)}]
        request.session['catogray'] = catogray #将分类信息存入session，便于后续刷新页面时直接使用

    # print(catogray)
    hot_sales = BookInfo.objects.all().order_by("-sales_num")[0:8] #获取销量前8的书籍
    latest = BookInfo.objects.all().order_by('-publish_time')[0:8] #获取最新出版的8本书籍
    data = {
        'catogray':catogray,
        'hot_sales':hot_sales,
        'latest':latest,
    }
    return  render(request,'bookapp/index.html',data)


def book_details(request):
    username = request.session.get('username')
    book_id = request.GET.get('book_id')
    book = BookInfo.objects.get(id=book_id)
    discount = '%.1f'% (book.dangdang_price/book.marketing_price*10)
    catogray_two_id = book.catogray_id
    catogray_two = TCatogray.objects.get(id=catogray_two_id)
    catogray_one = TCatogray.objects.get(id=catogray_two.parent_id)
    data = {
        'discount':discount,
        'username':username,
        'book': book,
        'catogray_two':catogray_two, # 直接传类别到前端，类别名，类别id均可用
        'catogray_one':catogray_one
    }
    return render(request, 'bookapp/Book_details.html',data)


def booklist(request):
    cato_two_flag,cato_two_name,cato_two_num = False,None,None #传到前端页面，指示需不需要列出二级类名
    # catogray 是一个一级类的字典，键为 类id，每个键对应的值为一个列表
    # 列表第一项为该类下共有多少本图书，第二项为类名,第三项为该类对应的二级类字典
    # 二级类字典 键为 类id，值为列表，列表第一项为该二级类下的书的数量，第二项为类名
    catogray = request.session.get('catogray')
    cato_two_id = request.GET.get('cato_two_id')#得到的值可能是字符串，'None',None
    cato_one_id = request.GET.get('cato_one_id')
    page_num = request.GET.get('page_num')
    if not cato_one_id or cato_one_id == 'None': #说明是从login_jump 跳转=过来，需要从session中取出原页面的类别id和page_num
        cato_one_id = request.session.get('cato_one_id')
        cato_two_id = request.session.get('cato_two_id')
        page_num = request.session.get('page_num')
    #如果用户在booklist页面继续点击分类标签，利用get到的参数 对 session中的cato_one_id,cato_two_id,page_num进行更新
    request.session['cato_one_id'] = cato_one_id
    request.session['cato_two_id'] = cato_two_id
    request.session['page_num'] = page_num
    if not cato_one_id: #用户不是从index页面点入进booklist页面，而是直接访问，跳转进入index页面
        return redirect('bookapp:index')
    cato_one_id = int(cato_one_id) #将字符类型转化为整型
    if not cato_two_id or cato_two_id == 'None':
        cato_two_ids = (val['id'] for val in TCatogray.objects.filter(parent_id=cato_one_id).values())
        books = BookInfo.objects.filter(catogray__in=cato_two_ids)
    else:
        cato_two_id = int(cato_two_id)
        books = BookInfo.objects.filter(catogray=int(cato_two_id))
        cato_two_flag = True
        cato_two_name = catogray[cato_one_id][2][cato_two_id][1]
        cato_two_num = catogray[cato_one_id][2][cato_two_id][0]
    #构造分页器对象
    paginator = Paginator(books,per_page=3)
    cur_page = paginator.page(1)
    if page_num and page_num !='None':
        cur_page = paginator.page(page_num)
    # print(cato_two_id,page_num)
    data = {
        'cato_one':{'id':cato_one_id,'name':catogray[cato_one_id][1],'num':catogray[cato_one_id][0]},
        'cato_two':{'flag':cato_two_flag,'id':cato_two_id,'name':cato_two_name,'num':cato_two_num},
        # 'cato_one_id':cato_one_id,
        # 'cato_two_id':cato_two_id,
        'catoinfo':catogray[cato_one_id], #传到前端页面的是一级类下的列表，第一项为图书数量，第二项为类名，第三项为二级类字典
        # 'cato_two_flag':cato_two_flag,
        # 'cato_two_name':cato_two_name,
        'books':cur_page, #当前页的书籍
        'title_list':['CV','PR','NLP','DeepLearning','BigData','OCR']
    }
    return  render(request,'bookapp/booklist.html',data)


def book_sort(request):
    method = request.GET.get('method') # '0':销量降序,'1'：价格升序,'2'：时间降序
    cato_one_id = request.GET.get('cato_one_id')
    cato_two_id = request.GET.get('cato_two_id')
    page_num = request.GET.get('page_num')
    # print(cato_one_id,cato_two_id,page_num)
    start_index = (int(page_num)-1)*3 #每次只需要返回到前端最多3条记录，第一页返回前3条，第二页返回4-6条
    catogray_id = [val['id'] for val in TCatogray.objects.filter(parent_id=cato_one_id).values()] # catogray_id 默认为在一级类下进行筛选
    if cato_two_id and cato_two_id != 'None':
        catogray_id = int(cato_two_id)
    if method == '0':
        books = BookInfo.objects.filter(catogray__in=catogray_id).order_by('-sales_num')[start_index:start_index+3]
    elif method == '1':
        books = BookInfo.objects.filter(catogray__in=catogray_id).order_by('dangdang_price')[start_index:start_index+3]
    elif method == '2':
        books = BookInfo.objects.filter(catogray__in=catogray_id).order_by('-publish_time')[start_index:start_index+3]
    else:
        books = BookInfo.objects.filter(catogray__in=catogray_id)[start_index:start_index+3]
    def my_default(book):
        if isinstance(book,BookInfo):
            return {'book_name':book.book_name,'cover_pic':book.cover_pics,'dangdang_price':book.dangdang_price,\
                    'marketing_price':book.marketing_price,'publish_time':book.publish_time.strftime('%Y/%m/%d'),\
                    'discount':('%.1f'%(book.dangdang_price/book.marketing_price *10)),'id':book.id}
    return JsonResponse(list(books),safe=False,json_dumps_params={'default':my_default})







