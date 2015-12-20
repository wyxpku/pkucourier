from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^verify/$', views.verify, name='verify'),
    url(r'^message/$', views.send_message_admin, name='message'),
    url(r'^(\d+)/$', views.user_info, name='userinfo'),
    url(r'^all/$', views.getall, name='alluser'),
]