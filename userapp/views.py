import datetime
import hashlib,random,string
import time,uuid

from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.shortcuts import render,redirect,HttpResponse
from django.urls import reverse

from bookapp.models import TUser,ConfirmCode
# Create your views here.
from userapp.captcha.image import ImageCaptcha


def register(request):
    # current_id用来判断用户是在index,booklist,book_details的哪个也页面发起的请求
    current_id = request.GET.get('current_id','0')
    request.session['current_id'] = current_id
    # cato_one_id = request.GET.get('cato_one_id')
    # cato_two_id = request.GET.get('cato_two_id')
    # page_num = request.GET.get('page_num')
    # request.session['current_id'] = current_id
    # request.session['cato_one_id'] = cato_one_id
    # request.sesson['cato_two_id'] = cato_two_id
    # request.session['page_num'] = page_num
    return render(request,'userapp/register.html')


def check_email(request):
    """
    用户注册时，验证用户的邮箱是否已在数据库中，若不在，证明可用
    :param request:
    :return:
    """
    text_email = request.POST.get('text_email')
    # return render(request,'userapp/register_ok.html')
    return HttpResponse('no') if TUser.objects.filter(email=text_email) else HttpResponse('ok')


def generate_code(request):
    image = ImageCaptcha()
    content = ''.join(random.sample(string.ascii_letters,4))
    print(content)
    request.session['code'] = content
    data = image.generate(content)
    return HttpResponse(data,'image/png')


def process_pwd(pwd,salt=None):
    h = hashlib.md5()
    if not salt:
        salt = ''.join(random.sample(string.ascii_letters,5))
    h.update((pwd+salt).encode())
    return salt,h.hexdigest()


def check_code(request): # 前端的 ajax 请求，判断验证码输入是否正确
    text_code = request.GET.get('text_code')
    session_code = request.session.get('code')
    # session_code = request.session.get('login_code') if 'login' in request.path else request.session.get('code')
    if(text_code.lower() == session_code.lower()):
        return HttpResponse('ok')
    return HttpResponse('no')


def generate_confirmcode():
    """
    产生邮箱验证码
    :return:
    """
    time_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    h = hashlib.md5()
    h.update(time_string.encode())
    print(h.hexdigest())
    return h.hexdigest()


def send_confirmEmail(confirm_code,user_id,email):
    """
    给用户发送激活用户的邮件
    :param confirm_code:
    :param user_id:
    :return:
    """
    subject, from_email, to = 'This is Derek',  'derekdongsir@sina.com',email,
    text_content = 'Hi,this is from Derek'
    html_content = '<p>感谢注册<a href="http://{}/userapp/activate_user/?code={}&user_id={}"target = blank > www.baidu.com < / a >，\欢迎你来验证你的邮箱，验证结束你就可以登录了！ < / p > '.format('127.0.0.1:8000',confirm_code,user_id)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def activate_user(request):
    """
    用户点击该链接以激活状态
    :param request:
    :return:
    """
    code = request.GET.get('code')
    user_id = request.GET.get('user_id')
    if ConfirmCode.objects.filter(code=code):
        user =TUser.objects.get(id=user_id)
        user.status = True
        user.save()
        return HttpResponse('ok')
    return HttpResponse('failed')


def registerlogic(request):
    time.sleep(2)
    id = str(uuid.uuid4())
    email = request.POST.get('txt_email')
    name = request.POST.get('txt_name')
    password = request.POST.get('txt_password')
    repassword = request.POST.get('txt_repassword')
    if password == repassword: # 再确认从前端传递过来的密码是否一致
        salt,password = process_pwd(password) # 获得盐和加密后的密码
        # request.session['user_id'] = id #将用户的id存储进session,便于后续使用
        # request.session['username'] = name # 将用户昵称保存在 session中，表示用户已登录，同时便于取出显示在主页面
        user=TUser(id=id,email=email,password=password,nick_name=name,salt=salt)
        user.save()
        confirm_code = generate_confirmcode() #产生邮箱验证码
        ConfirmCode.objects.create(code=confirm_code,user=user)
        send_confirmEmail(confirm_code,id,email) # 给用户发送激活邮件
        return render(request, 'userapp/register_ok.html',{'email':email}) # 注册成功，返回注册成功的页面
    return HttpResponse('密码不一致')


def login(request): #渲染登录界面
    #依据发送登录请求的页面的不同，渲染不同的页面给用户
    # '1':booklist,'2':book_detail,'3':购物车页面  默认为index
    current_id = request.GET.get('current_id','0')
    request.session['current_id'] = current_id #存进session,便于 jump时候使用
    return render(request,'userapp/login.html')


def loginlogic(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    auto_login = request.POST.get('auto_login') # 值为真则设置cookie记住密码
    try:
        user= TUser.objects.get(email=email)
        if user.password == process_pwd(password,salt=user.salt)[1]:
            if user.status: #判断用户是否处于激活状态
                request.session['username'] = user.nick_name # 将用户昵称存入session，代表用户已登录
                request.session['user_id'] = user.id  # 将用户的id存储进 session
                return HttpResponse('ok')
            return HttpResponse('dead')
        return HttpResponse('no') # 用户存在但是密码不对，返回no
    except: #用户不存在返回 no
       return HttpResponse('no')


def login_jump(request):
    order_confirmed = request.session.get("order_confirmed")
    if not order_confirmed: #如果此时订单未确认，则进一步判断用户处于哪一页
        current_id = request.session.get('current_id')
        if current_id == '1':
            cato_one_id = str(request.session.get('cato_one_id'))
            cato_two_id  = str(request.session.get('cato_two_id'))
            page_num = str(request.session.get('page_num'))
            # url1 ="bookapp/booklist/?cato_one_id="+cato_one_id+'&cato_two_id='+cato_two_id+'&page_num='+page_num
            return redirect("bookapp:booklist")
        elif current_id == '2': #代表从书籍详情页发起的登录
            return redirect('bookapp:book_details')
        elif current_id == '3': # 代表从购物车页面发起登录
            return redirect('orderapp:cart_page')
        else:
            return redirect('bookapp:index')
    return redirect('orderapp:indent')#进入地址填写页面


def logout(request): #使用Ajax请求进行登出，将用户名从session中清除即可
    if request.session.get('username') and request.session.get('user_id'):
        if request.session.get("order_confirmed"): #将订单确认标志删除
            del request.session["order_confirmed"]
        if request.session.get('cart'):
            del request.session['cart'] #将购物车清除
        del request.session['username']
        del request.session['user_id']
    return HttpResponse('no') if request.session.get('username') else HttpResponse('ok')


