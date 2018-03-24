from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView
from .models import Post
from comments.forms import CommentForm
import markdown
from .models import Post, Category


# Create your views here.

# def index(request):
#     file_path = 'blog/index.html'
#     post_list = Post.objects.all().order_by('-created_time')
#     return render(request, file_path, context={
#         'post_list': post_list
#     })
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'


def detail(request, pk):
    file_path = 'blog/detail.html'
    post = get_object_or_404(Post, pk=pk)

    # 阅读量+1
    post.increase_views()

    # 使用md
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])

    # CommentForm
    form = CommentForm()
    comment_list = post.comment_set.all()

    context = {'post': post,
               'form': form,
               'comment_list': comment_list, }

    # return render(request, file_path, context={'post': post})
    return render(request, 'blog/detail.html', context=context)


def archives(request, year, mouth):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=mouth).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})
