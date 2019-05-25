import datetime
import time
import uuid

from django.db import transaction
from django.shortcuts import render,redirect,HttpResponse
from django.urls import reverse

from bookapp.models import BookInfo,TDelivery,TOrder,GoodsList,TUser,BookInfo
from orderapp.cart import Cart, Item
from django.http import JsonResponse

from orderapp.models import City


def add_to_cart(request):
    cart = request.session.get('cart')
    if not cart:
        cart = Cart()  # 如果购物车不存在，则实例化一个购物车
    book_id = request.GET.get('book_id') #从前端获得书籍的id
    book_num = int(request.GET.get('book_num',1)) # 获得书籍数量，如果不是拼接在路径后，则默认为1
    if book_id:
        book = BookInfo.objects.get(id=book_id) # 可以加一个 KeyError的防护机制
        item = Item(book,book_num) # 实例化一个商品项对象
        cart.add_item(item) # 将书籍项添加入购物车中
        # print(item.book_num)
        request.session['cart'] = cart # 将cart重新保存入 session
        res = {
            'total_cost': ('%.1f' % cart.total_cost),
            'saving_cost': ('%.1f' % cart.saving_cost)
        }
        return JsonResponse(res)
    return HttpResponse('no')


def remove_from_cart(request):
    """
    处理两种业务，一种是将书籍状态置为False,一种是将书籍从购物车中删除，再次重新加入
    :param request:'1':置False;'2':删除
    :return:
    """
    cart = request.session.get('cart')
    if not cart:
        return HttpResponse('cart not found')
    book_id = request.GET.get('book_id')
    state = request.GET.get('state')
    if book_id:
        if state == '1':
            cart.remove_item(book_id) # 将键为 book_id的状态置为 False
        elif state == '2':
            del cart.cart_items[book_id]  #将此项删除，对应的是恢复区的内容
            cart.update_cost()
        request.session['cart'] = cart #重新保存购物车
        res = {
            'total_cost':('%.1f'%cart.total_cost),
            'saving_cost':('%.1f'%cart.saving_cost)
        }
        return JsonResponse(res)

def all_operation(request):
    """
    :param request:request接收全选的方式，'1'为全部选中，'2'为全部不选
    :return:total_cost,saving_cost
    """
    cart = request.session.get('cart')
    method = request.GET.get('method')
    if method == '1':
        for item in cart.cart_items.values():
            item.status = True
    elif method =='2':
        for item in cart.cart_items.values():
            item.status = False
    cart.update_cost()
    request.session['cart'] = cart  # 重新保存购物车
    res = {
        'total_cost': ('%.1f' % cart.total_cost),
        'saving_cost': ('%.1f' % cart.saving_cost),
        'num_items':len(cart.cart_items)
    }
    return JsonResponse(res)


def cart_page(request): #渲染购物车页面
    cart = request.session.get('cart')
    if cart: #默认购物车页面上的物品是全部选中的
        for item in cart.cart_items.values():
            item.status = True
            cart.update_cost() # 更新购物车的总金额
    data = {
        #{}.values() -->dict([]) 但是 cart为空则点不出 cart_items
        'items':cart.cart_items.values() if cart else None,
        'num_of_items':len(cart.cart_items) if cart else 0, # len()可以直接获得字典中的项数
        'cart':cart
    }
    request.session['cart'] = cart # 将更新后的购物车保存进 session
    return render(request,'orderapp/cart.html',data)


def book_num_adjust(request): #购物车页面对书籍的数量进行调整
    cart = request.session.get('cart')
    book_id = request.GET.get('book_id')
    number = int(request.GET.get('number',0))
    cart.book_num_adjust(book_id,number) #调整书籍的数量
    request.session['cart'] =cart #将购物车重新保存
    res={'total_cost':('%.1f'%cart.total_cost),
         'saving_cost':('%.1f'%cart.saving_cost)}
    # return HttpResponse(cart.total_cost)
    return JsonResponse(res)


def indent(request): #渲染订单确认页面，填写地址信息等
    request.session['order_confirmed'] = True #设置订单确认标志，便于定位到订单确认页
    if not request.session.get('username'):
        return redirect('userapp:login') #若此时用户未登录，则强制其登录
    cart = request.session.get('cart')
    if not cart:
        return redirect('orderapp:cart_page')
    user_id = request.session.get('user_id')
    locations = TDelivery.objects.filter(user=user_id)
    provinces = City.objects.filter(type=1) #获得省份
    data = {
        'province': provinces,
        'locations':locations,
        'total_cost': ('%.1f' % cart.total_cost),
        'items':[item for item in cart.cart_items.values() if item.status] if cart else None,
        # 'items': cart.cart_items.values() if cart else None,
        'num_of_items': len(cart.cart_items) if cart else 0,  # len()可以直接获得字典中的项数
    }
    return render(request,'orderapp/indent.html',data)


def get_delivery_info(request):
    '''通过地址 id 查询地址信息，返回到前端'''
    delivery_id = request.GET.get('delivery_id')
    delivery = TDelivery.objects.get(id=delivery_id)
    res = {
        'name':delivery.receiver_name,
        'address':delivery.address,
        'zip_code':delivery.zipt_code,
        'phone':delivery.phone,
        'telephone':delivery.telephone
    }
    return JsonResponse(res)


def check_address(request):
    '''从前端获得详细地址，查询数据库是否该地址已经存在'''
    province = request.GET.get('province')+'/'
    city = request.GET.get('city')+'/'
    town = request.GET.get('town')+'/'
    address = province+city+town+request.GET.get('address')
    return HttpResponse('no') if TDelivery.objects.filter(address=address) else HttpResponse('ok')


def get_location_info(request):
    '''从delivery 表中根据用户id 查询出该用户存储的地址信息,通过ajax返回到前端'''
    locations = []
    user_id = request.session.get('user_id')
    if user_id:
        locations = list(TDelivery.objects.filter(user=user_id)) #获取该用户下的地址信息
        def my_default(location):
            if isinstance(location,TDelivery):
                return {'receiver_name':location.receiver_name,'address':location.address,\
                        'zip_code':location.zipt_code,'telephone':location.telephone,'phone':location.phone}

        return JsonResponse(list(locations),safe=False,json_dumps_params={'default':my_default})
    return JsonResponse(locations,safe=False) #此时传递的是空列表


def get_city(request):
    """
    通过前端ajax请求发送回来的省份id查询其下的城市，转换成 json格式响应到前端
    """
    pro_id = int(request.GET.get('pro_id'))
    cities = list(City.objects.filter(pid=pro_id))
    def my_default(city):
        if isinstance(city,City):
            return {'id':city.id,'cityname':city.cityname}
    return JsonResponse(cities,safe=False,json_dumps_params={'default':my_default})


def get_town(request):
    """
    通过前端 ajax请求发送过来的城市id查询其下的县区，转换成json返回到前端
    """
    city_id = int(request.GET.get('city_id'))
    towns = list(City.objects.filter(pid=city_id))
    def my_default(town):
        if isinstance(town,City):
            return {'id':town.id,'townname':town.cityname}
    return JsonResponse(towns,safe=False,json_dumps_params={'default':my_default})


def generate_order(request,delivery_id, user_id):
    cart = request.session.get('cart')
    if not cart:
        raise ValueError
    order_id = str(uuid.uuid4())  # 生成订单 id
    total_num = len(cart.cart_items)
    total_cost = cart.total_cost
    create_time = datetime.datetime.now()  # 生成当前时间
    user_obj = TUser.objects.get(id=user_id) # user_id为Torder的外键，需要获取对象
    delivery_obj = TDelivery.objects.get(id=delivery_id)#delivery_id 为 order_id 的外键
    TOrder.objects.create(order_id=order_id,user=user_obj,total_num=total_num, total_price=total_cost, \
                          delivery=delivery_obj, create_time=create_time)
    return cart,order_id


def generate_goodslist(cart,order_id):
    '''将商品清单存入数据库'''
    for book_id,item in cart.cart_items.items():
        id = str(uuid.uuid4()) # 生成每一项的id
        book_obj = BookInfo.objects.get(id=book_id)
        order_obj =TOrder.objects.get(order_id=order_id)
        order_obj.goodslist_set.create(id=id,book=book_obj,book_num=item.book_num,book_price=item.price)
        #这是错误的添加数据的方式！
        # GoodsList.objects.create(id=id,order=order_id,book=book_id,book_num=item.book_num,book_price=item.price)


def location_info(request):
    try:
        with transaction.atomic():
            user_id = request.session['user_id']#若取不到user_id,则全部内容回滚
            delivery_id = None
            if request.method == "POST":
                delivery_id = str(uuid.uuid4()) # 生成地址主键
                receiver_name = request.POST.get('receiver_name')
                province = request.POST.get('province')+'/'
                city = request.POST.get("city")+'/'
                town = request.POST.get("town")+'/'
                address = province+city+town+request.POST.get('address') #将地址进行拼接
                zipt_code = request.POST.get('zip_code')
                telephone = request.POST.get('telephone')
                phone = request.POST.get('phone')
                user_obj = TUser.objects.get(id=user_id) # Tuser作为外键，需要传入对象
                TDelivery.objects.create(id=delivery_id, user=user_obj, receiver_name=receiver_name, address=address,
                                         zipt_code=zipt_code,telephone=telephone, phone=phone)
            elif request.method == "GET":
                delivery_id = request.GET.get('delivery_id')
            if not delivery_id:
                raise ValueError # 地址id未取到，抛出异常
            cart,order_id = generate_order(request,delivery_id,user_id) #生成订单，同时返回购物车,订单 id
            request.session['order_id'] = order_id # 将订单id存入session,便于后续使用
            generate_goodslist(cart,order_id) #将商品清单存入数据库
            return redirect('orderapp:indent_ok') # 返回订单ok
    except:
        return HttpResponse('error')


def indent_ok(request): #渲染订单确认后的 ok 页面
    if not request.session.get('order_confirmed'):
        return redirect('orderapp:indent') #如果订单未被确认，返回订单确认页面
    order_id = request.session.get('order_id')
    order = TOrder.objects.get(order_id=order_id)
    data = {
        'num_of_items': order.total_num,
        'total_cost': ('%.1f' % order.total_price),
        'delivery':order.delivery
    }
    return render(request,'orderapp/indent_ok.html',data)



