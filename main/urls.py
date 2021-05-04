from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('',auth_views.LoginView.as_view(template_name='main/login.html',redirect_authenticated_user=True),name='login'),
    path('home',views.home,name='home'),
    path('logout',views.log_out,name='logout')

]