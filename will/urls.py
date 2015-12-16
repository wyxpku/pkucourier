from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^new/', views.new, name='newwill'),
    url(r'^(\d+)/', views.get_info, name='getWillInfo'),
    url(r'^all/', views.all, name='allwill'),
]