from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(\d+)/', views.get_info, name='dealinfo'),
    url(r'^user/(\d+)/', views.get_user_deals, name='getUserDeals'),
    url(r'^complete/$', views.complete, name='completeDeal'),
]