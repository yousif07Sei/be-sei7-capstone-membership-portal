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
    path('organization/update', views.organization_update, name = 'organization_update'),
    path('organization/members', views.organization_members, name = 'organization_members'),

    # API endpoints for plan
    path('plan/list', views.plan_list, name = 'plan_list'),
    path('plan/create', views.plan_create, name = 'plan_create'),
    path('plan/update', views.plan_update, name = 'plan_update'),

    # API endpoints for Events
    path('event/list', views.event_list, name = 'event_list'),

    # API engpoints for countries
    path('country/list', views.country_list, name = 'country_list'),

    path('user/',views.user_detail,name='user_detail'),
    path('user/create/',views.user_create,name='user_create')
    # path('login/',views.LoginAPIView,name='login')  

    # Test model
    # path('test/create', views.test_create, name = 'test_create'),
]