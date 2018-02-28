from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)


class Tag(models.Model):
    name = models.CharField(max_length=100)


class Post(models.Model):
    title = models.CharField(max_length=80)  # 文章标题
    body = models.TextField()  # 正文,使用TextField()储存大段的文本

    created_time = models.DateTimeField()  # 文章修改前后的时间
    modified_time = models.DateTimeField()

    excerpt = models.CharField(max_length=200, blank=True)  # CharField不允许出现空值,所以必须声明blank=True

    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    # 文章作者,User由django.contrib.auth.models导入
    author = models.ForeignKey(User)
