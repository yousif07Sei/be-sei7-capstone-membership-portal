from django.urls import path,include
from . import views


app_name="bussines_portal_app"
urlpatterns = [
    path('',views.home,name='home')
]
