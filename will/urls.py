from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'will/new/', views.new, name='newwill'),
]