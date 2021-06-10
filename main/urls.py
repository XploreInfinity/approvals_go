from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    #*authentication urls
    path('',auth_views.LoginView.as_view(template_name='main/login.html',redirect_authenticated_user=True),name='login'),
    path('home/',views.home,name='home'),
    path('logout',views.log_out,name='logout'),

    #*general urls
    path('post/create/',views.PostCreateView.as_view(),name='create-post'),
    path('post/<int:pk>/',views.PostDetailView.as_view(),name='view-post'),
    path('post/<int:pk>/update/',views.PostUpdateView.as_view(),name='update-post'),
    path('post/<int:pk>/delete/',views.PostDeleteView.as_view(),name='delete-post'),
    path('post/<int:pk>/approve/',views.PostApproveView.as_view(),name='approve-post'),
    path('post/<int:pk>/reject/',views.PostRejectView.as_view(),name='reject-post'),
   
    #*pdf display url
    path('PDFCollection/<str:PDFfile>',views.getPDF),

    #*Password management urls
    path('pass_reset/',auth_views.PasswordResetView.as_view(template_name='main/pwd_reset/pwd_reset.html'),name='pwd_reset'),
    path('pass_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='main/pwd_reset/pwd_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='main/pwd_reset/pwd_reset_confirm.html'),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='main/pwd_reset/pwd_reset_complete.html'),name='password_reset_complete')

]
