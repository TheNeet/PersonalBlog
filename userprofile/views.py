from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import UserLoginForm, UserRegisterForm, ProfileForm
from .models import Profile

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required # 登陆修饰器

# Create your views here.
def user_login(req):
    if req.method == 'POST':
        user_login_form = UserLoginForm(data=req.POST)
        if user_login_form.is_valid():
            # 使用 cleaned_data 对数据进行清洗
            data = user_login_form.cleaned_data

            # 检测用户名，此处的 username password 是关键字，与 forms 中声明的无关
            # 判断密码
            user = authenticate(username=data.get('user_name'), password=data.get('password'))
            if user:
                # 将用户数据保存在 session 中（实现登陆）
                login(request=req, user=user)
                return redirect('blog:article_list')
            else:
                return HttpResponse("账号或密码错误，请重新输入。")
        else:
            return HttpResponse('账号或密码输入不合法。')
    elif req.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form': user_login_form}
        return render(req, 'userprofile/login.html', context)
    else:
        return HttpResponse("请求异常。")

def user_logout(req):
    logout(req);
    return redirect('blog:article_list')

def user_register(req):
    if req.method == 'POST':
        user_register_form = UserRegisterForm(data=req.POST)
        print(req.POST, user_register_form.is_valid())
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()

            # 将创建用户保存至数据库
            login(req, user=new_user)
            return redirect('blog:article_list')
        else:
            return HttpResponse('表单输入有误，请重新输入。')
    elif req.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'form': user_register_form}
        return render(req, 'userprofile/register.html', context)
    else:
        return HttpResponse("请求异常。")

# 当用户没有登录时将会跳转到 login 页面
@login_required(login_url='/userprofile/login')
def user_delete(req, id):
    if req.method == 'POST':
        user = User.objects.get(id=id)
        # 身份验证
        if req.user == user:
            logout(req)
            user.delete()
            return redirect('blog:article_list')
        else:
            return HttpResponse('你没有权限执行此操作！')
    else:
        return HttpResponse('请求异常。')

# 编辑用户扩展信息
@login_required(login_url='/userprofile/login')
def profile_edit(req, id):
    user = User.objects.get(id=id)
    # user_id 是 OneToOneField 自动生成的
    # profile_user = Profile.objects.get(user_id=id)
    if Profile.objects.filter(user_id=id).exists():
        profile_user = Profile.objects.get(user_id=id)
    else:
        profile_user = Profile.objects.create(user=user)
    if req.method == 'POST':
        if req.user != user:
            return HttpResponse('用户错误。')

        profile_form = ProfileForm(data=req.POST, files=req.FILES)
        if profile_form.is_valid():
            profile_form = profile_form.cleaned_data
            profile_user.phone_num = profile_form['phone_num']
            profile_user.bio = profile_form['bio']
            print(profile_user)
            if 'blog_head' in req.FILES:
                profile_user.blog_head = profile_form['blog_head']
            profile_user.save()
            return redirect('userprofile:edit', id=id)
        else:
            return HttpResponse('表单错误。')

    elif req.method == 'GET':
        profile_form = ProfileForm()
        context = {'profile_form': profile_form, 'user': user, 'profile_user': profile_user}
        return render(req, 'userprofile/edit.html', context)
    else:
        return HttpResponse('请求错误。')
        
def profile_view(req, id):
    user = User.objects.get(id=id)
    if Profile.objects.filter(user_id=id).exists():
        profile_user = Profile.objects.get(user_id=id)
    else:
        profile_user = Profile.objects.create(user=user)
    return render(req, 'userprofile/edit.html', {'profile_user': profile_user})