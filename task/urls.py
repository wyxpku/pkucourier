from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^new/$', views.new, name='newtask'),
    url(r'^(\d+)/$', views.get_info, name='taskinfo'),
    url(r'^(\d+)/ap/$', views.get_ap_info, name='taskapinfo'),
    url(r'^resp/$', views.task_resp, name='taskresp'),
    url(r'^user/(\d+)/$', views.get_user_tasks, name='getUserTasks'),
    url(r'^all/$', views.all, name='alltasks'),
]