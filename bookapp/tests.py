import datetime
import hashlib

from django.core.mail import send_mail, EmailMultiAlternatives
from django.test import TestCase
import django,os,random

from dangdang_pro import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dangdang_pro.settings")
django.setup()
from bookapp.models import BookInfo,TCatogray,TUser


# marketing_price = models.FloatField(null=True) done
# dangdang_price = models.FloatField(null=True) done

# sales_num = models.IntegerField(null=True)  done
# stock = models.IntegerField(null=True) done


# press = models.CharField(max_length=60, null=True)
# cover_pics = models.TextField(null=True)
# words = models.IntegerField(null=True)
# pages = models.SmallIntegerField(null=True)
# book_size = models.SmallIntegerField(null=True)
# paper_type = models.CharField(max_length=20, null=True)
# packing_type = models.CharField(max_length=20, null=True)
# version = models.SmallIntegerField(null=True)
# printing_index = models.SmallIntegerField(null=True)
# isbn = models.CharField(db_column='ISBN', max_length=50, null=True)  # Field name made lowercase.
# publish_time = models.DateField(null=True)
# printint_time = models.DateField(null=True)
# recommend = models.TextField(null=True)
# content_intro = models.TextField(null=True)
# author_intro = models.TextField(null=True)
# catalog = models.TextField(null=True)
# comments = models.TextField(null=True)
# experpt_pics = models.TextField(null=True)
# status = models.CharField(max_length=100, null=True)
# for book in BookInfo.objects.all():
    # book.sales_num = random.randint(50,10000)
    # book.stock = random.randint(500,5000)
    # book.marketing_price = random.randint(20,80)
    # book.dangdang_price = book.marketing_price - random.randint(2,10)
    # book.save()
    # book.save()
# catogray_one= TCatogray.objects.filter(parent_id__isnull=True).values()
# catogray_one_dic = {val['id']:val['catogry_name'] for val in catogray_one }
# print(catogray_one_dic) #{1: '计算机', 2: '外语', 3: '人文社科', 4: '青春', 5: '小说', 6: '管理', 7: '少儿'}
# catogray_two_dic = {}
# for i in catogray_one_dic:
#     catogray_two_dic[i] = [val['catogry_name'] for val in TCatogray.objects.filter(parent_id=i).values()]
# print(catogray_two_dic) #{1: ['计算机理论', '数据库', '程序设计', '人工智能', '操作系统', '大数据'], 2

def save_pics():
    dirs = os.listdir('E:\LearningFiles\django\dangdang_pro\static\pics')
    for file_name in dirs:
        id =file_name.split('.')[0].split('_')[1]
        pic_path = os.path.join('pics',file_name)
        # print(pic_path)
        book = BookInfo.objects.get(id=id)
        book.cover_pics = pic_path
        book.save()

def generate_date():
    year = str(random.randint(1990,2019))
    month = str(random.randint(1,12))
    day = str(random.randint(1,28))
    p_date = '-'.join([year,month,day])
    return p_date
# print(generate_date())
# for book in BookInfo.objects.all():
#     book.publish_time = generate_date()
#     book.save()
# TUser.objects.all().delete()

def send_html():
    subject, from_email, to = 'This is Derek',  'derekdongsir@sina.com',  'derekdongsir@163.com',
    text_content = 'Hi,this is from Derek'
    html_content = '<p>感谢注册<a href="http://{}/confirm/?code={}"target = blank > www.baidu.com < / a >，\欢迎你来验证你的邮箱，验证结束你就可以登录了！ < / p > '.format('127.0.0.0','111')
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
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

if __name__ == '__main__':
    # send_mail(
    #     "Hello,this is Derek",
    #     " This is a test！I am tring to use my codes sending you a message",
    #     'derekdongsir@sina.com',
    #     ['651375149@qq.com'],
    # )
    # send_html()
    generate_confirmcode()


