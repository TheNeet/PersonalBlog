from django.urls import path
import blog.views_article
import blog.views_other

# 正在部署的应用名称
app_name = 'blog'

urlpatterns = [
    # 添加我需要的 url
    path('article-list', blog.views_article.aritcle_list, name='article_list'),
    path('article-detail/<int:id>/', blog.views_article.aritcle_detail, name='article_detail'),
    path('article-delete/<int:id>/', blog.views_article.article_delete, name='article_delete'),
    path('article-update/<int:id>/', blog.views_article.article_update, name='article_update'),
    path('article-write/', blog.views_article.article_write, name='article_write'),
    path('happy-new-year', blog.views_other.happy_new_year, name='happy_new_year'),
    path('happy-new-yearLH', blog.views_other.happy_new_yearLH, name='happy_new_yearLH'),
]