from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required # 登陆修饰器
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.core import serializers
import json
import markdown

from .forms import ArticlePostForm
from .models import ArticlePost


# 文章列表，添加翻页功能
def aritcle_list(req):
    # 返回根据某属性排序后的对象数组
    if req.GET.get('order') == 'total_views':
        # 使用 ‘-’ 进行逆排序，没有 ‘-’ 为升序排序
        article_list = ArticlePost.objects.all().order_by('-total_views')
        order = 'total_views'
    else:
        # 取出所有文章
        article_list = ArticlePost.objects.all()
        order = 'normal'

    paginator = Paginator(article_list, 6)
    page = req.GET.get('page')
    articles = paginator.get_page(page)
    contexts = {'articles': articles, 'order': order}


    # 将 markdown 样式文章转义成 html 样式
    for article in contexts['articles']:
        article.body = markdown.markdown(
            article.body,
            extensions = [
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.tables',
            ]
        )

    if req.is_ajax():
        contexts['articles'] = json.loads(serializers.serialize("json", contexts['articles']))
        return JsonResponse(contexts)
    else:
        return render(req, 'article/list.html', contexts)

# 文章详情
def aritcle_detail(req, id):
    # 取出对应的文章
    aritcle = ArticlePost.objects.get(id=id)

    # 文章阅读数 +1  
    aritcle.total_views += 1
    aritcle.save(update_fields=['total_views'])

    # 将 markdown 渲染成 html 样式
    aritcle.body = markdown.markdown(
        aritcle.body,
        extensions = [
            # 缩写，表格等常用扩展
            'markdown.extensions.extra',
            # 语法高亮
            'markdown.extensions.codehilite',
            # 表格
            'markdown.extensions.tables',
        ]
    )

    # 将文章内容发送给前端
    context = {'article': aritcle}
    return render(req, 'article/detail.html', context)

# 编写文章触发的函数
@login_required(login_url='/userprofile/login')
def article_write(req):
    # 提交
    if req.method == 'POST':
        # 用提交的文章内容创建一个实例
        article_form = ArticlePostForm(data=req.POST)
        # 判断该提交是否满足模型要求
        if article_form.is_valid():
            # 保存数据，但暂时不提交至数据库
            new_article = article_form.save(commit=False)
            # 通过 id 索引作者
            new_article.author = User.objects.get(id=req.user.id)
            # 保存文章
            new_article.save()
            # 提交之后，自动跳转至 article_list ，也称为重定向
            return redirect("blog:article_list")
        else:
            return HttpResponse("表单内容有误，请重新填写")
    # 数据获取，给用户提供一个用于编辑、提交的 html
    else:
        article_form = ArticlePostForm()
        context = {'article_form': article_form}
        return render(req, 'article/write.html', context)

def article_delete(req, id):
    article = ArticlePost.objects.get(id=id)
    article.delete()
    return redirect('blog:article_list')

def article_update(req, id):
    article = ArticlePost.objects.get(id=id)

    if req.method == 'POST':
        article_form = ArticlePostForm(data=req.POST)
        if article_form.is_valid():
            article.title = req.POST['title']
            article.body = req.POST['body']
            article.save()
            return redirect('blog:article_detail', id=id)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        article_form = ArticlePostForm()
        context = {'article': article, 'article_form': article_form}
        return render(req, 'article/update.html', context)