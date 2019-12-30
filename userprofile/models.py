from django.db import models
from django.contrib.auth.models import User
# 内置信号
from django.db.models.signals import post_save
# 信号接收器的装饰器
from django.dispatch import receiver

# Create your models here.

# 用户扩展信息
class Profile(models.Model):
    # 与 User 模型构成一对一关系，即可以通过 Profile 去索引 User 中的信息，相当于继承作用
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # 电话
    phone_num = models.CharField(max_length=20, blank=True)
    # 头像
    blog_head = models.ImageField(upload_to='blog_head/%Y%m%d/', blank=True)
    # 个人简介
    bio = models.TextField(max_length=80, blank=True)

    def __str__(self):
        return 'user {} {}'.format(self.user.username, self.user)


'''
# 信号接收函数，创建用户调用
@receiver(post_save, sender=User)
def creat_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# 信号接收函数，更新用户调用
@receiver(post_save, sender=User)
def upgrade_user_profile(sender, instance, **kwargs):
    instance.profile.save()
'''