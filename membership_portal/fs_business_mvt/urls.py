from django.urls import path,include
from . import views


app_name="bussines_portal_app"
urlpatterns = [
    path('',views.home,name='home'),
    path('organization/',views.OrganizationList.as_view(),name='organization_index'),
    path('organization/<int:pk>/update/',views.OrganizationUpdate.as_view(),name='organization_update'),
    path('organization/<int:pk>/delete/',views.OrganizationDelete.as_view(),name='organization_delete'),
    path('organization/<int:pk>/',views.OrganizationDetail,name='organization_detail'),
    
    path('profile/<int:pk>/update',views.ProfileUpdate.as_view(),name='profile_update'),
    path('profile/',views.ProfileList.as_view(),name='profile_index'),
    path('organization/<int:user_id>/remove/<int:organization_id>',views.remove_member,name='remove_member')
]
