from django.urls import path
from . import views

urlpatterns = [
    path('user/list', views.user_list, name = 'user_list'),

    # API endpoints for benefit
    path('benefit/list', views.benefit_list, name = 'benefit_list'),
    path('benefit/adduser', views.benefit_add_user, name = 'benefit_add_user'),
    path('benefit/detail/', views.benefit_detail, name = 'benefit_detail'),
    path('benefit/qrcode', views.benefit_qrcode, name = 'benefit_qrcode'),
    path('benefit/delete', views.benefit_delete, name = 'benefit_delete'),
    path('benefit/create', views.benefit_create, name = 'benefit_create'),
    path('benefit/update', views.benefit_update, name = 'benefit_update'),
    
    # API endpoints for organization
    path('organization/list', views.organization_list, name = 'organization_list'),
    path('organization/detail/', views.organization_detail, name = 'organization_detail'),
    path('organization/delete', views.organization_delete, name = 'organization_delete'),
    path('organization/create', views.organization_create, name = 'organization_create'),

    path('user/',views.user_details,name='user_details'),
    path('user/create/',views.user_create,name='user_create')
    # path('login/',views.LoginAPIView,name='login')  

    # Test model
    # path('test/create', views.test_create, name = 'test_create'),
]