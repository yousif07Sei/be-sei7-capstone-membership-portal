from django.urls import path
from . import views

urlpatterns = [
    path('user/list', views.user_list, name = 'user_list'),
    path('benefit/list', views.benefit_list, name = 'benefit_list'),
    path('benefit/adduser', views.benefit_add_user, name = 'benefit_add_user'),
    path('benefit/detail/', views.benefit_detail, name = 'benefit_detail'),
    path('benefit/qrcode', views.benefit_qrcode, name = 'benefit_qrcode'),
]