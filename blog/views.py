import markdown

from markdown.extensions.toc import TocExtension

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.utils.text import slugify

from comments.forms import CommentForm
from .models import Post, Category, Tag


# Create your views here.

# def index(request):
#     file_path = 'blog/index.html'
#     post_list = Post.objects.all().order_by('-created_time')
#     return render(request, file_path, context={
#         'post_list': post_list
#     })

def index(request):
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={
        'post_list': post_list
    })


class IndexView(ListView):
    model = Post  # 获取模型为Post
    template_name = 'blog/index.html'  # 指定渲染模板(路径)
    context_object_name = 'post_list'  # 模型列表实例化

    # 指定分页功能
    paginate_by = 10

    def get_context_data(self, **kwargs):
        '''

        :param kwargs:
        :return:
        '''
        context = super().get_context_data(**kwargs)

        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新到context中
        context.update(pagination_data)

        # 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}
        left = []  # 左起页码
        right = []  # 右起页码

        first = False  # 首页页码是否显示
        last = False  # 尾页页码是否显示

        left_has_more = False  # 首页后是否显示省略号
        right_has_more = False  # 尾页后是否显示省略号

        page_number = page.number  # 当前页码
        total_pages = paginator.num_pages  # 页码总数
        page_range = paginator.page_range  # 页码列表

        if page_number == 1:
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages - 1:
                right_has_more = True

            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0: page_number - 1]
            if left[0] > 2:
                left_has_more = True

            if left[0] > 1:
                first = True

        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data


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


class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


# def category(request, pk):
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate).order_by('-created_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        '''
        文章阅读量+1
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)
        md = markdown.markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        # 渲染MD
        post.body = md.convert(post.body)
        post.toc = md.toc

        return post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set_all()
        context.update({
            'form': form,
            'comment_list': comment_list,
        })
        return context


class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)
