from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, request, HttpResponseRedirect
from django.contrib import auth
from sign.models import Event,Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
#s首页
def index(request):
    return  render(request, "index.html")
#登陆动作
def login_action(request):
    if request.method == 'POST':
        login_username = request.POST.get("username")
        login_password = request.POST.get("password")
        if login_username == '' or login_password == '':
            return render(request, "index.html", {"error": "username or password null!"})
        else:
            user = auth.authenticate(username=login_username, password=login_password)
            if user is not None:
                auth.login(request, user)  # 登录判断
                response = HttpResponseRedirect('/event_manage/')
                #response.set_cookie('user', login_username, 3600)  # 添加浏览器 cookie
                request.session['user'] = login_username    # 添加浏览器 session
                return response
            else:
                return render(request, "index.html", {"error": "username or password ERROR!"})
    else:
        return render(request, "index.html")


#发布会管理
@login_required
def event_manage(request):
    #username = request.COOKIES.get('user','')  # 读取浏览器 cookie
    username = request.session.get('user', '')  # 读取浏览器 session
    event_list = Event.objects.all()
    return render(request,"event_manage.html",{"user":username,
    "events":event_list})




# 发布会名称搜索
@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("name", "")
    #search_name_bytes = search_name.encode(encoding="utf-8")
    events_list= Event.objects.filter(name__contains=search_name)
    if len(events_list) == 0:
        return render(request, "event_manage.html", {"user": username,
                                                     "hint": "根据输入的 `发布会名称` 查询结果为空！"})
    return render(request, "event_manage.html", {"user": username, "events": events_list})



#嘉宾管理
@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guests_list= Guest.objects.all()
    paginator = Paginator(guests_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username, "guests": contacts})




#嘉宾手机号查询
@login_required
def search_phone(request):
    username = request.session.get('user', '')
    search_phone = request.GET.get("phone", "")
    #search_name_bytes = search_name.encode(encoding="utf-8")
    guest_list= Guest.objects.filter(phone__contains=search_phone)
    if len(guest_list) == 0:
        return render(request, "guest_manage.html", {"user": username,
                                                     "hint": "根据输入的 `手机号` 查询结果为空！"})
    paginator = Paginator(guest_list, 2)  # 少于2条数据不够分页会产生警告
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render(request, "guest_manage.html", {"user": username,
                                                 "guests": contacts,
                                                 "phone": search_phone})


# 签到页面
@login_required
def sign_index(request, event_id):
    print(event_id)
    event = get_object_or_404(Event, id=event_id)
    guest_list = Guest.objects.filter(event_id=event_id)           # 签到人数
    sign_list = Guest.objects.filter(sign="1", event_id=event_id)   # 已签到数
    guest_data = str(len(guest_list))
    sign_data = str(len(sign_list))
    return render(request, 'sign_index.html', {'event': event,
                                               'guest':guest_data,
                                               'sign':sign_data})




# 嘉宾签到处理
@login_required
def sign_index_action(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    guest_list = Guest.objects.filter(event_id=event_id)
    sign_list = Guest.objects.filter(sign="1", event_id=event_id)
    guest_data = str(len(guest_list))
    sign_data = str(len(sign_list))

    phone =  request.POST.get('phone','')

    result = Guest.objects.filter(phone = phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event,'hint': 'phone error.','guest':guest_data,'sign':sign_data})

    result = Guest.objects.filter(phone = phone,event_id = event_id)
    if not result:
        return render(request, 'sign_index.html', {'event': event,'hint': 'event id or phone error.','guest':guest_data,'sign':sign_data})

    result = Guest.objects.get(event_id = event_id,phone = phone)

    if result.sign:
        return render(request, 'sign_index.html', {'event': event,'hint': "user has sign in.",'guest':guest_data,'sign':sign_data})
    else:
        Guest.objects.filter(event_id = event_id,phone = phone).update(sign = '1')
        return render(request, 'sign_index.html', {'event': event,'hint':'sign in success!',
            'sign_user': result,
            'guest':guest_data,
            'sign':str(int(sign_data)+1)
            })

#退出系统
@login_required
def logout(request):
    auth.logout(request)  # 退出登录
    response = HttpResponseRedirect('/index/')
    return response
