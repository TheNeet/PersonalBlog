from django import forms 
from django.contrib.auth.models import User
from .models import Profile

# 登陆表单
class UserLoginForm(forms.Form):
    user_name = forms.CharField()
    password = forms.CharField()


# 用户注册
class UserRegisterForm(forms.ModelForm):

    # 保存两次密码
    password = forms.CharField()
    password_confirm = forms.CharField()

    class Meta:
        model = User
        # 此处的 username 定义了前端回传至后台的表单中用户名的 id
        # 并且此处声明的 username 不是数据库中用户名的标签
        fields = ('username', 'email')

    # def clean_[字段]这种写法Django会自动调用，来对单个字段的数据进行验证清洗。
    def clean_password_confirm(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password_confirm'):
            return data.get('password')
        else:
            return forms.ValidationError('两次密码不同，请重新输入。')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_num', 'blog_head', 'bio')

