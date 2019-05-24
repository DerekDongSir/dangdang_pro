# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class BookInfo(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    book_name = models.CharField(max_length=40, null=True)
    author = models.CharField(max_length=80, null=True)
    catogray = models.ForeignKey('TCatogray', models.DO_NOTHING,null=True)
    marketing_price = models.FloatField(null=True)
    dangdang_price = models.FloatField(null=True)
    sales_num = models.IntegerField(null=True)
    stock = models.IntegerField(null=True)
    press = models.CharField(max_length=60,null=True)
    cover_pics = models.TextField(null=True)
    words = models.IntegerField(null=True)
    pages = models.SmallIntegerField( null=True)
    book_size = models.SmallIntegerField( null=True)
    paper_type = models.CharField(max_length=20,  null=True)
    packing_type = models.CharField(max_length=20,  null=True)
    version = models.SmallIntegerField( null=True)
    printing_index = models.SmallIntegerField( null=True)
    isbn = models.CharField(db_column='ISBN', max_length=50,  null=True)  # Field name made lowercase.
    publish_time = models.DateField( null=True)
    printint_time = models.DateField( null=True)
    recommend = models.TextField( null=True)
    content_intro = models.TextField( null=True)
    author_intro = models.TextField( null=True)
    catalog = models.TextField( null=True)
    comments = models.TextField( null=True)
    experpt_pics = models.TextField( null=True)
    status = models.CharField(max_length=100,  null=True)

    class Meta:
        db_table = 'book_info'


class GoodsList(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    order = models.ForeignKey('TOrder', models.DO_NOTHING,  null=True)
    book = models.ForeignKey(BookInfo, models.DO_NOTHING,  null=True)
    book_num = models.IntegerField( null=True)
    book_price = models.FloatField( null=True)

    class Meta:
        db_table = 'goods_list'


class TCatogray(models.Model):
    id = models.IntegerField(primary_key=True)
    catogry_name = models.CharField(max_length=40,  null=True)
    parent_id = models.IntegerField( null=True)

    class Meta:
        db_table = 't_catogray'


class TDelivery(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    user = models.ForeignKey('TUser', models.DO_NOTHING,  null=True)
    receiver_name = models.CharField(max_length=20,  null=True)
    address = models.CharField(max_length=100,  null=True)
    zipt_code = models.CharField(max_length=6,  null=True)
    telephone = models.CharField(max_length=12,  null=True)
    phone = models.CharField(max_length=15,  null=True)
    status = models.CharField(max_length=40,  null=True)

    class Meta:
        db_table = 't_delivery'


class TOrder(models.Model):
    order_id = models.CharField(primary_key=True, max_length=40)
    user = models.ForeignKey('TUser', models.DO_NOTHING,  null=True)
    total_num = models.IntegerField( null=True)
    total_price = models.FloatField( null=True)
    delivery = models.ForeignKey(TDelivery, models.DO_NOTHING,  null=True)
    create_time = models.DateTimeField( null=True)
    status = models.CharField(max_length=40,  null=True)

    class Meta:
        db_table = 't_order'


class TUser(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    nick_name = models.CharField(max_length=20,  null=True)
    email = models.CharField(max_length=40,  null=True)
    password = models.CharField(max_length=40,  null=True)
    salt = models.CharField(max_length=40,  null=True,verbose_name='盐')
    status = models.BooleanField(default=False, verbose_name='激活状态')
    create_time = models.DateTimeField(auto_now_add=True,null=True,verbose_name='创建时间')

    class Meta:
        db_table = 't_user'


class ConfirmCode(models.Model):
    code = models.CharField(max_length=128,verbose_name='邮箱验证码')
    user = models.ForeignKey('TUser',models.CASCADE,verbose_name='用户id')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        db_table ='t_confirmcode'

