from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post


# Create your views here.

def index(request):
    file_path = 'blog/index.html'
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, file_path, context={
        'post_list': post_list
    })


def detail(request, pk):
    file_path = 'blog/detail.html'
    post = get_object_or_404(Post, pk=pk)
    return render(request, file_path, context={
        'post': post
    })
