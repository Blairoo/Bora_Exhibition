from django.shortcuts import render, redirect, get_object_or_404
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
# from .forms import UploadFileForm
import datetime
# sweetify
import sweetify

def main(req):
    if req.session.get('id') == None:
        context = {
            "past": Product.objects.filter(exhstart__gte=datetime.date(2000, 1, 1), exhend__lt=datetime.date.today()),
            "current": Product.objects.filter(exhstart__lte=datetime.date.today(), exhend__gte=datetime.date.today()),
            "upcoming": Product.objects.filter(exhstart__gt=datetime.date.today())
            }
        print(context)
        return render(req, "index.html", context)
    else:
        context = {
            "session_user": req.session.get("id"),
            "logged_user": User.objects.filter(pk = req.session.get('id')),
            "past": Product.objects.filter(exhstart__gte=datetime.date(2000, 1, 1), exhend__lt=datetime.date.today()),
            "current": Product.objects.filter(exhstart__lte=datetime.date.today(), exhend__gte=datetime.date.today()),
            "upcoming": Product.objects.filter(exhstart__gt=datetime.date.today()),
            "reserve": Basket.objects.filter(who=req.session.get("id"))
            }
        print(context)
        print(Basket.objects.filter(who=req.session.get("id")))
        return render(req, "index.html", context)

def checkid(req):
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
    context = {
        "overlap": overlap,
        "msg": msg
        }
    return JsonResponse(context)

def ajaxlogin(req):
    print(req.GET["login_id"])
    print(req.GET["login_pw"])
    login_id = req.GET["login_id"]
    login_pw = req.GET["login_pw"]
    if User.objects.filter(userid = login_id) and User.objects.filter(userpw = login_pw):
        req.session["id"] = login_id
        session_user = req.session.get("id")
        msg = "로그인 성공"
        check = "suc"
    else:
        session_user = req.session.get("id")
        msg = "로그인 정보를 확인해주세요"
        check = "fail"
    context = {
        "session_user": session_user,
        "msg": msg,
        "check": check
    }
    return JsonResponse(context)

def signup(req):
    if req.method == "POST":
        username=req.POST.get('user_name')
        userid=req.POST.get('user_id')
        userpw=req.POST.get('user_pw')
        # userphone=req.POST.get('user_phone')
        joined_user = User(username=req.POST.get('user_name'), userid=userid, userpw=userpw, userphone=req.POST.get('user_phone'))
        joined_user.save()
        sweetify.info(req, "회원 가입이 완료되었습니다.", timer=1200)
        return redirect('http://3.38.152.216:8000/bora/main#section-login')
    else:
        return render(req, "index.html")

def withdrawal(req):
    try:
        leave_id = req.POST.get("leave_id")
        leave_pw = req.POST.get("leave_pw")
        user_id = User.objects.get(userid = leave_id)
        user_pw = User.objects.get(userid = leave_id).userpw
        # print(User.objects.filter(userpw = req.POST.get("leave_pw")).userpw)
        if req.session.get("id") == leave_id:
            if leave_pw == user_pw:
                print('id, pw 동일')
                req.session.pop("id")
                User.objects.filter(pk=req.POST.get('leave_id')).delete()
                sweetify.info(req, "회원 탈퇴가 완료되었습니다.", timer=1200)
                return redirect('main')
            else:
                print('id 동일 pw 동일 안함')
                sweetify.info(req, "계정 정보가 일치하지 않습니다.", timer=1200)
                return redirect('http://3.38.152.216:8000/bora/main#section-mypage')
    except:
        print('id 동일 안함')
        sweetify.info(req, "계정 정보가 일치하지 않습니다.", timer=1200)
        return redirect('http://3.38.152.216:8000/bora/main#section-mypage')

def logout(req):
    print(req.session.get("id"))
    # req.session.clear()
    req.session.pop("id")
    print(req.session.get("id"))
    return redirect("http://3.38.152.216:8000/bora/main")

def edit(req):
    logged_user = User.objects.get(pk = req.session.get("id"))
    print("edit", logged_user)
    if logged_user.userpw != req.POST.get('edit_pw') or logged_user.userphone != req.POST.get('edit_phone'):
        logged_user.userpw = req.POST['edit_pw']
        logged_user.userphone = req.POST['edit_phone']
        logged_user.save()
        print('editsuc')
        sweetify.info(req, '성공적으로 수정되었습니다.', timer=1200)
        return redirect('http://3.38.152.216:8000/bora/main#section-mypage')
    else:
        sweetify.warning(req, '기존 정보와 동일합니다.', timer=1200)
        print('goback')
        return redirect('http://3.38.152.216:8000/bora/main#section-mypage')

def list(req):
    context = {
    "session_user": req.session.get("id"),
    "logged_user": User.objects.filter(pk = req.session.get('id')),
    "past": Product.objects.filter(exhstart__gte=datetime.date(2000, 1, 1), exhend__lt=datetime.date.today()),
    "current": Product.objects.filter(exhstart__lte=datetime.date.today(), exhend__gte=datetime.date.today()),
    "upcoming": Product.objects.filter(exhstart__gt=datetime.date.today())
    }
    return render(req, "list.html", context)

def detail(req, pk):
    if req.session.get("id") is None:
        sweetify.warning(req, "로그인 후 이용할 수 있습니다", timer=1200)
        return redirect("http://3.38.152.216:8000/bora/main#section-login")
    else:
        exh = get_object_or_404(Product, pk=pk)
        print(exh)
        revs = Review.objects.filter(exhibit=exh)
        this_rev = Review.objects.filter(exhibit=exh, reviewer=req.session.get("id"))
        if exh in Product.objects.filter(exhend__lt=datetime.date.today()):
            class_exh = "Past"
        elif exh in Product.objects.filter(exhstart__lte=datetime.date.today(), exhend__gte=datetime.date.today()):
            class_exh = "Current"
        elif exh in Product.objects.filter(exhstart__gte=datetime.date.today()):
            class_exh = "Upcoming"
        context = {
            "class_exh" : class_exh,
            "session_user": req.session.get("id"),
            "exh": exh,
            "reviews": revs,
            "this_rev": this_rev
        }
        print(context)
        return render(req, 'detail.html', context)

def ajaxreserve(req):
    reserve_exh = req.GET["reserve_exh"]
    reserve_id = req.GET["reserve_id"]
    reserve_num = req.GET["reserve_num"]
    # print(reserve_exh + reserve_id + reserve_num)
    countq = Basket.objects.filter(what=Product.objects.get(pk=reserve_exh), who=User.objects.get(pk=reserve_id)).count()
    if countq == 0:
        print('suc')
        basket = Basket(what=Product.objects.get(pk=reserve_exh), who=User.objects.get(pk=reserve_id), count=reserve_num)
        basket.save()
        print(basket)
        check = "success"
    else:
        print("fail")
        edit_basket = Basket.objects.get(what=Product.objects.get(pk=reserve_exh), who=User.objects.get(pk=reserve_id))
        edit_basket.count = reserve_num
        edit_basket.save()
        check = "fail"
    context = {
        "check": check
    }
    return JsonResponse(context)

def delete_res(req):
    del_what = req.POST.get("delwhat")
    del_who = req.POST.get("delwho")
    del_count = req.POST.get("delcount")
    print("nononononononno")
    Basket.objects.filter(what=Product.objects.get(pk=del_what), who=User.objects.get(pk=del_who), count=del_count).delete()
    print("ok")
    return redirect("http://3.38.152.216:8000/bora/main#section-mypage")

def ajaxleave_rev(req):
    revexh = req.GET["rev_exh"]
    revid = req.GET["rev_id"]
    reviews = req.GET["reviews"]
    print(reviews)
    countq = Review.objects.filter(exhibit = Product.objects.get(pk=revexh), reviewer=User.objects.get(pk=revid)).count()
    print(Basket.objects.filter(what=Product.objects.get(pk=revexh),who=User.objects.get(pk=revid)))
    if Basket.objects.filter(what=Product.objects.get(pk=revexh),who=User.objects.get(pk=revid)):
        if countq == 0:
            print('suc')
            review = Review(exhibit = Product.objects.get(pk=revexh), reviewer = User.objects.get(pk=revid), exhreview = reviews)
            review.save()
            check = "success"
        else:
            print("fail")
            edit_review = Review.objects.get(exhibit = Product.objects.get(pk=revexh), reviewer=User.objects.get(pk=revid))
            print(edit_review)
            edit_review.exhreview = reviews
            edit_review.save()
            check = "fail"
    else:
        check = "reserve_first"
    context = {
        "check": check
    }
    return JsonResponse(context)

def ajaxdelete_rev(req):
    del_exh = req.GET["del_rev_exh"]
    del_id = req.GET["del_rev_id"]
    print(del_id)
    countq = Review.objects.filter(exhibit = Product.objects.get(pk=del_exh), reviewer=User.objects.get(pk=req.session.get("id"))).count()
    print(Review.objects.filter(exhibit = Product.objects.get(pk=del_exh), reviewer=User.objects.get(pk=req.session.get("id"))))
    if countq == 0:
        print('fail')
        check = "fail"
    else:
        print('suc')
        Review.objects.filter(exhibit=Product.objects.get(pk=del_exh), reviewer=User.objects.get(pk=req.session.get("id"))).delete()
        check = "success"
    context = {
        "check": check
    }
    return JsonResponse(context)