from django.shortcuts import render
from django.http import HttpResponse
from django.http import  HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event

# Create your views here.
def index(request):
    return render(request,"index.html")

#登录动作
def login_action(request):
    if request.method=="POST":
        username=request.POST.get('username','')
        password=request.POST.get('password','')
        print(username,"   ",password)
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)#登录
            request.session['user']=username
            response=HttpResponseRedirect('/event_manage/')
            return response
        else:
            return render(request,'index.html',{'error':'username or password error!'})
    else:
        return HttpResponse('get请求!')

#发布会管理
@login_required
def event_manage(request):
    username=request.session.get('user',' ')
    event_list=Event.objects.all()
    username=request.session.get('user','')
    return render(request,"event_manage.html",{"user":username,"events":event_list})

# 发布会名称搜索
@login_required
def search_name(request):
    username = request.session.get('username', '')
    search_name = request.GET.get("name", "")
    search_name_bytes = search_name.encode(encoding="utf-8")
    event_list = Event.objects.filter(name__contains=search_name_bytes)
    return render(request, "event_manage.html", {"user": username, "events": event_list})