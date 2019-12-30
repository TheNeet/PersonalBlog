from django.db import models
# 导入内建的 User 模型
from django.contrib.auth.models import User
# 导入用于处理时间相关事务的模块
from django.utils import timezone

# Create your models here.

# 博客文章数据模型
class ArticlePost(models.Model):
    # 文章作者。 on_delete 指明数据删除的方式
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 文章标题。
    title = models.CharField(max_length=100)
    # 文章正文。
    body = models.TextField()
    # 文章创建时间。
    created_time = models.DateTimeField(default=timezone.now)
    # 文章更新时间.
    update_time = models.DateTimeField(auto_now=True)
    # 文章阅读量
    total_views = models.PositiveIntegerField(default=0)

    class Meta:
        # ordering 指定模型返回的数据的排列顺序，必须是一个 tuple/list
        # '-created_time' 表明数据应该以倒序排列
        ordering = ('-created_time',)

    def __str__(self):
        return self.title