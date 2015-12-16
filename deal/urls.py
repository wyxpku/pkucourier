from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'deal/new', views.new, name='newtask'),
]