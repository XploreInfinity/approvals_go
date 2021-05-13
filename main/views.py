import unicodedata
from django.shortcuts import render,redirect
from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView
from .models import Post
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django import forms
from .forms import PostsForm
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import prevent_relogin,allowed_users
from django.http import HttpResponse
#*Create your views here.
@login_required
@allowed_users(['HOD','faculty'])
def home(request):
    context={'posts':Post.objects.all(),'title':'Home'}
    return render(request,'main/home.html',context)

def log_out(request):
    logout(request)
    messages.success(request,'Logged out successfully!')
    return redirect('login')
class PostListView(ListView):
    model=Post
    
    template_name='main/home.html'
    context_object_name='posts'
    ordering=['-date_posted']
class PostDetailView(LoginRequiredMixin,DetailView):
    model=Post
    template_name='main/post_detail.html'
class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    fields=['title','description','PDFfile']
    template_name='main/post_creation.html'
    def get(self,request):
        #*only allow faculty user groups to create posts
        if self.request.user.groups.all()[0].name=='faculty':
            return super().get(request)
        else:
            messages.error(self.request,'You cannot create posts!')
            return redirect('home')
    #*custom validation of the uploaded PDF file:
    def clean_content(self,form):
        content = form.cleaned_data['PDFfile']
        content_type = content.content_type.split('/')[1]
        if content_type in settings.CONTENT_TYPES:
            if content.size > int(settings.MAX_UPLOAD_SIZE):
                return unicodedata.normalize("NFKD",('Please keep filesize under %s. Current filesize: %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content.size)))
        else:
            return 'Only PDFs are supported!' 
        return None
    #*Add the current user as the author of this post,call custom PDF validator,then continue:
    def form_valid(self,form):
        form.instance.author=self.request.user
        file_error=self.clean_content(form)
        if file_error is None:
            messages.success(self.request,'Post Created Successfully!')
            return super().form_valid(form)
            
        else:
            messages.error(self.request,file_error) 
            return super().form_invalid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Post
    fields=['title','description','PDFfile']
    template_name='main/post_creation.html'
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False
    #*custom validation of the uploaded PDF file:
    def clean_content(self,form):
        if form.cleaned_data['PDFfile'] is None:
            content = form.cleaned_data['PDFfile']
            content_type = content.content_type.split('/')[1]
            if content_type in settings.CONTENT_TYPES:
                if content.size > int(settings.MAX_UPLOAD_SIZE):
                    return unicodedata.normalize("NFKD",('Please keep filesize under %s. Current filesize: %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content.size)))
            else:
                return 'Only PDFs are supported!' 
        return None
    #*Add the current user as the author of this post,call custom PDF validator,then continue:
    def form_valid(self,form):
        file_error=self.clean_content(form)
        if file_error is None:
            messages.success(self.request,'Post Updated Successfully!')
            return super().form_valid(form)
            
        else:
            messages.error(self.request,file_error) 
            return super().form_invalid(form)
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Post
    success_url='/home'
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author or self.request.user.groups.all()[0].name=='HOD':
            return True
        return False
class DocDetailView(LoginRequiredMixin,UserPassesTestMixin,DetailView):
    model=Post
    template_name='main/doc_detail.html'
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author or self.request.user.groups.all()[0].name=='HOD':
            return True
        return False

#*
def PostActions(request):
    if request.topple:
        return  HttpResponse('<h1>Topple them!ye!</h1>')
    return HttpResponse('No')
