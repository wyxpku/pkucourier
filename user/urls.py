from django.conf.urls import url
from . import views


urlpatterns = [

    url(r'login/$', views.login, name = 'login'),
    url(r'signup/$', views.signup, name = 'signup'),
    url(r'all/$', views.all, name = 'alluser'),
    url(r'(\d+)/$', views.user_info, name = 'userinfo'),
]