from django.shortcuts import render
from django.http import HttpResponse
from .models import Post


# Create your views here.

def index(request):
    file_path = 'blog/index.html'
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, file_path, context={
        'post_list': post_list
    })
