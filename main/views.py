from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import prevent_relogin,allowed_users
#*Create your views here.
@login_required
@allowed_users(['HOD'])
def home(request):
    return render(request,'main/home.html')
def log_out(request):
    logout(request)
    messages.success(request,'Logged out successfully!')
    return redirect('login')