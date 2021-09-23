from django.db import models
from django.db.models.fields import DateField, TextField
from django.db.models.fields.related import ForeignKey
import datetime

from django.forms.fields import DateTimeField
# from django.db.models.fields.related import ForeignKey, ManyToManyField

# Create your models here.

# 아직 migration 노노 ForeignKey 쓸 지 ManyToManyField 쓸 지 정하자
class User(models.Model):
    basketuser = models.ManyToManyField('Product', through="Basket", max_length=20, verbose_name='장바구니 사용자', related_name='basketuser')
    username = models.CharField(max_length=20, verbose_name='사용자명')
    userid = models.CharField(max_length=20, verbose_name='아이디', null=False, blank=True, default='', primary_key=True)
    userpw = models.CharField(max_length=20, verbose_name='비밀번호')
    userphone = models.CharField(max_length=11, verbose_name='휴대폰')
    registered = models.DateTimeField(auto_now_add = True, verbose_name='계정 생성시간')
    def __str__(self):
        return self.userid
    class Meta:
        db_table = 'User'
        verbose_name = '유저'
        verbose_name_plural = '유저'

class Product(models.Model):
    exhname = models.CharField(max_length=64, verbose_name='전시회명', default='', blank=True, null=False, primary_key=True)
    # 전시 기간은 yy.mm.dd~yy.mm.dd 형태로 받아야 함 노션 models.py 확인
    exhstart = models.DateField(default=datetime.date.today, verbose_name='전시 시작')
    exhend = models.DateField(default=datetime.date.today, verbose_name="전시 종료")
    # STATE = (('P', '지난 전시'), ('C', '현재 전시'), ('U', '전시 예정'))
    # exhstat = models.CharField(max_length=1, verbose_name='전시 상태', choices=STATE)
    exhinfo = TextField(max_length=250, verbose_name='전시 정보', default="")
    exhimage = models.ImageField(blank=True, verbose_name='전시포스터', upload_to="bora/productimage")
    def __str__(self):
        return self.exhname
    class Meta:
        db_table = 'Product'
        verbose_name = '전시회'
        verbose_name_plural = '전시회'

class Basket(models.Model):
    who = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='예매자')
    what = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='예매 전시')
    count = models.PositiveSmallIntegerField(default=1, verbose_name='인원')
    def __str__(self):
        return self.who
    class Meta:
            db_table = 'Basket'
            verbose_name = '장바구니'
            verbose_name_plural = '장바구니'

class Review(models.Model):
    exhibit = ForeignKey(Product, on_delete=models.CASCADE, verbose_name='리뷰 전시회')
    reviewer = ForeignKey(User, on_delete=models.CASCADE, verbose_name='리뷰 작성자')
    exhreview = TextField(max_length=200, verbose_name='전시 리뷰')
    writetime = models.DateTimeField(auto_now=True, verbose_name="리뷰 작성 시간")
    def __str__(self):
        return self.exhibit
    class Meta:
        db_table = 'Review'
        verbose_name = '리뷰'
        verbose_name_plural = '리뷰'