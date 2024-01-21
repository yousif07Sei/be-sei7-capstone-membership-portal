from django.urls import path,include
from . import views


app_name="bussines_portal_app"
urlpatterns = [
    path('',views.home,name='home'),
    path('organization/',views.OrganizationList.as_view(),name='organization_index'),
    path('organization/<int:pk>/update/',views.OrganizationUpdate.as_view(),name='organization_update'),
    path('organization/<int:pk>/delete/',views.OrganizationDelete.as_view(),name='organization_delete'),

    # yousif added the plan
    path('plan/',views.PlanList.as_view(),name='plan_index'),
    path('plan/<int:pk>/update/',views.PlanUpdate.as_view(),name='plan_update'),
    path('plan/<int:pk>/delete/',views.PlanDelete.as_view(),name='plan_delete')
]
