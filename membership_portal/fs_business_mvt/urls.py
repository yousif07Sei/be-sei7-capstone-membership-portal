from django.urls import path,include
from . import views


app_name="bussines_portal_app"
urlpatterns = [
    path('home/',views.home,name='home'),
    path('organization/',views.OrganizationList.as_view(),name='organization_index'),
    path('organization/<int:pk>/update/',views.OrganizationUpdate.as_view(),name='organization_update'),
    path('organization/<int:pk>/delete/',views.OrganizationDelete.as_view(),name='organization_delete'),

 # yousif added the planFeature
    # path('plan/feature/',views.PlanList.as_view(),name='plan_feature_index'),
    # path('plan/feature/<int:pk>/update/',views.PlanUpdate.as_view(),name='plan_feature_update'),
    # path('plan/feature/<int:pk>/delete/',views.PlanDelete.as_view(),name='plan_feature_delete'),
    # yousif added the plan
    path('plan/',views.PlanList.as_view(),name='plan_index'),
    path('plan/<int:pk>/update/',views.PlanUpdate.as_view(),name='plan_update'),
    path('plan/<int:pk>/delete/',views.PlanDelete.as_view(),name='plan_delete')
]
