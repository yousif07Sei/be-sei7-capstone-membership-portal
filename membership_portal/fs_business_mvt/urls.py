from django.urls import path,include
from . import views


app_name="bussines_portal_app"
urlpatterns = [
    path('',views.home,name='home'),
    path('organization/',views.OrganizationList.as_view(),name='organization_index'),
    path('organization/<int:pk>/update/',views.OrganizationUpdate.as_view(),name='organization_update'),
]
