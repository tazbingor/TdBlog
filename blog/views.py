from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post
import markdown
from .models import Post, Category


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

    # 使用md
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])

    return render(request, file_path, context={'post': post})


def archives(request, year, mouth):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=mouth).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})
