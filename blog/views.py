from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def index(request):
    file_path = 'blog/index.html'
    return render(request, file_path, context={
        'title': '博客首页',
        'welcome': '欢迎访问我的博客!'
    })
