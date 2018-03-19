from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible


# Create your models here.
@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField(max_length=80)  # 文章标题

    body = models.TextField()  # 正文,使用TextField()储存大段的文本

    created_time = models.DateTimeField()  # 文章修改前后的时间
    modified_time = models.DateTimeField()

    excerpt = models.CharField(max_length=200, blank=True)  # 文章摘要,CharField不允许出现空值,所以必须声明blank=True

    category = models.ForeignKey(Category)  # 分类
    tags = models.ManyToManyField(Tag, blank=True)  # 标签

    # 文章作者,User由django.contrib.auth.models导入
    author = models.ForeignKey(User)

    # view字段以记录阅读量
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        '''
        阅读量+1
        :return:
        '''
        self.views += 1
        self.save(update_fields=['views'])  # 跟新数据库

    class Meta:
        ordering = ['-created_time']
