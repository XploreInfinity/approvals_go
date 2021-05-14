from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('',auth_views.LoginView.as_view(template_name='main/login.html',redirect_authenticated_user=True),name='login'),
    path('home/',views.home,name='home'),
    path('logout',views.log_out,name='logout'),


    path('post/create/',views.PostCreateView.as_view(),name='create-post'),
    path('post/<int:pk>/',views.PostDetailView.as_view(),name='view-post'),
    path('post/<int:pk>/update/',views.PostUpdateView.as_view(),name='update-post'),
    path('post/<int:pk>/delete/',views.PostDeleteView.as_view(),name='delete-post'),
    path('showhome',views.PostListView.as_view(),name='some-home'),

    path('PDFCollection/<str:PDFfile>',views.getPDF),

    path('pass_reset/',auth_views.PasswordResetView.as_view(template_name='main/pwd_reset/pwd_reset.html'),name='pwd_reset'),
    path('pass_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='main/pwd_reset/pwd_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='main/pwd_reset/pwd_reset_confirm.html'),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='main/pwd_reset/pwd_reset_complete.html'),name='password_reset_complete')

]
