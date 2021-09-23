from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Product, Basket, Review
from django.http.response import HttpResponse, JsonResponse
# 한글 정규식
import re
#forms.py file upload
from django.http import HttpResponseRedirect, request, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
# forms.py에서 import해온다
from .forms import UploadFileForm
import datetime

# Create your views here.
# forms.py에서 파일업로드를 하는 함수
# def upload_file(req):
#     if req.method == 'POST':
#         form = UploadFileForm(req.POST, req.FILES)

#         if form.is_valid():
#             handle_uploaded_file(req.FILES['myfile']) # myfile은 forms.py에서 받아 온 파일업로드 변수명, 아래에 만든 함수 불러와서 사용
#             messages.info(req, '업로드 성공')
#             return render(req, 'login.html') # return render 사용해서 html파일로 보내도 됨
#     else:
#         form = UploadFileForm()
#         return render(req, 'upload.html', {'form': form})

# def handle_uploaded_file(f): # f는 넘어온 파일
#     with open(os.path.abspath( './bora/static/' + f.name), 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)

# forms.py 없이 파일업로드 하는 함수
def upload_file(req):
    # if req.method == 'POST':
    #     with open(os.path.abspath( './bora/static/' + req.FILES['myfile'].name), 'wb+') as destination:
    #         for chunk in req.FILES['myfile'].chunks():
    #             destination.write(chunk)
    #     messages.info(req, '업로드 성공')
    #     return render(req, 'upload.html')
    # else:
    #     return render(req, 'upload.html')
    coffee = req.POST.getlist("coffee")
    print(coffee)
    return render(req, "upload.html", {"cafe": req.POST.getlist("coffee")})

def main(req):
    if req.method == "POST":
        logged_user = User.objects.filter(userid = req.POST.get("loginid"), userpw = req.POST.get("loginpw"))
        print(logged_user)
        if logged_user:
            req.session["id"] = logged_user[0].userid
            print("로그인, 세션")
            print(req.session.get("id"))
            context = {
            "session_user": req.session.get("id")
            }
            print(context)
            return render(req, "index.html", context)
        return render (req, 'index.html')
    print("logout?")
    return render(req, "index.html")

def join(req):
    try:
        if req.POST.get('user_id') == User.objects.get(userid = req.POST.get('user_id')):
            print('fail')
            return HttpResponse('fail')
        else:
            print('success')
            return HttpResponse('success')
    except :
        return render(req, 'join.html')

def login(req):
    if req.method == "POST":
        username=req.POST.get('user_name')
        userid=req.POST.get('user_id')
        userpw=req.POST.get('user_pw')
        # userphone=req.POST.get('user_phone')
        joined_user = User(username=req.POST.get('user_name'), userid=userid, userpw=userpw, userphone=req.POST.get('user_phone'))
        joined_user.save()
        return render(req, 'login.html', {"id": userid, "pw": userpw, "name": username})
    else:
        return render(req, "login.html")

def checkid(req):
    # return render(req, 'ajax.html', {"p1": req.POST.get("id_"), "p2": req.POST.get("pw_")})
    # 1트
    joinid = req.GET['user_id']
    print(joinid)
    try:
        # 중복된 아이디가 있을때
        user = User.objects.get(userid = joinid)
    except:
        # 중복된 아이디가 없을때
        user = None
    if user is None:
        overlap = "pass"
        msg = "사용 가능한 아이디입니다."
    else:
        overlap = "fail"
        msg = "이미 사용중인 아이디입니다."
    # 아이디에 한글 있는지 확인
    hanCount = len(re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', joinid))
    if hanCount > 0:
        overlap = "reg"
        msg = "영문자 또는 숫자로 3자 이상 입력해주세요."
    if len(joinid) < 3:
        print("three")
        overlap = "three"
        msg = "3자 이상 입력해주세요."
    context = {"overlap": overlap, "msg": msg}
    # return render(req, 'join.html', context)
    return JsonResponse(context)
    # id_ck = User.objects.filter(userid = req.POST.get('inputid'))
    # if id_ck:
    #     return HttpResponse("중복")
    # else:
    #     return HttpResponse("통과")

def logout(req):
    print(req.session.get("id"))
    # req.session.clear()
    req.session.pop("id")
    print(req.session.get("id"))
    return redirect("http://49.50.164.62:8000/bora/")

def exhibition(req):
    # if exh == "past":
    #     past = Product.objects.filter(exhstart__gte=datetime.date(2000, 1, 1), exhend__lte=datetime.date.today())
    # elif exh == "current":
    #     current = Product.objects.filter(exhstart__lte=datetime.date.today(), exhend__gte=datetime.date.today())
    # elif exh == "upcoming":
    #     upcoming = Product.objects.filter(exhstart__gte=datetime.date.today())
    context = {
    "past": Product.objects.filter(exhstart__gte=datetime.date(2000, 1, 1), exhend__lt=datetime.date.today()),
    "current": Product.objects.filter(exhstart__lte=datetime.date.today(), exhend__gte=datetime.date.today()),
    "upcoming": Product.objects.filter(exhstart__gt=datetime.date.today())
    }
    return render(req, "exhibition.html", context)