import unicodedata, os
from django.shortcuts import render, redirect
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from .models import Post
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django import forms
from .forms import PostsForm
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import prevent_relogin, allowed_users
from django.http import Http404, FileResponse

# *Create your views here.
@login_required
@allowed_users(["HOD", "faculty"])
def home(request):

    posts = Post.objects.order_by("-date_posted")
    if request.user.groups.all()[0].name == "faculty":
        posts = Post.objects.filter(author=request.user).order_by("-date_posted")
    context = {"posts": posts, "title": "Home"}
    return render(request, "main/home.html", context)


def log_out(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "main/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_group"] = self.request.user.groups.all()[0].name
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "description", "PDFfile"]
    template_name = "main/post_creation.html"

    def get(self, request):
        # *only allow faculty user groups to create posts
        if self.request.user.groups.all()[0].name == "faculty":
            return super().get(request)
        else:
            messages.error(self.request, "You cannot create posts!")
            return redirect("home")

    # *custom validation of the uploaded PDF file:
    def clean_content(self, form):
        content = form.cleaned_data["PDFfile"]
        content_type = content.content_type.split("/")[1]
        if content_type in settings.CONTENT_TYPES:
            if content.size > int(settings.MAX_UPLOAD_SIZE):
                return unicodedata.normalize(
                    "NFKD",
                    ("Please keep filesize under %s. Current filesize: %s")
                    % (
                        filesizeformat(settings.MAX_UPLOAD_SIZE),
                        filesizeformat(content.size),
                    ),
                )
        else:
            return "Only PDFs are supported!"
        return None

    # *Add the current user as the author of this post,call custom PDF validator,then continue:
    def form_valid(self, form):
        form.instance.author = self.request.user
        file_error = self.clean_content(form)
        if file_error is None:
            messages.success(self.request, "Post Created Successfully!")
            return super().form_valid(form)

        else:
            messages.error(self.request, file_error)
            return super().form_invalid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "description", "PDFfile"]
    template_name = "main/post_update.html"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    # *custom validation of the uploaded PDF file:
    def clean_content(self, form):
        if form.cleaned_data["PDFfile"] is None:
            content = form.cleaned_data["PDFfile"]
            content_type = content.content_type.split("/")[1]
            if content_type in settings.CONTENT_TYPES:
                if content.size > int(settings.MAX_UPLOAD_SIZE):
                    return unicodedata.normalize(
                        "NFKD",
                        ("Please keep filesize under %s. Current filesize: %s")
                        % (
                            filesizeformat(settings.MAX_UPLOAD_SIZE),
                            filesizeformat(content.size),
                        ),
                    )
            else:
                return "Only PDFs are supported!"
        return None

    # *Add the current user as the author of this post,call custom PDF validator,then continue:
    def form_valid(self, form):
        form.instance.status = "pending"
        file_error = self.clean_content(form)
        if file_error is None:
            messages.success(self.request, "Post Updated Successfully!")
            return super().form_valid(form)

        else:
            messages.error(self.request, file_error)
            return super().form_invalid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/home"

    def test_func(self):
        post = self.get_object()
        if (
            self.request.user == post.author
            or self.request.user.groups.all()[0].name == "HOD"
        ) and (post.status != "approved"):
            return True
        return False


class PostApproveView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = []
    template_name = "main/post_confirm_approve.html"

    def test_func(self):
        if self.request.user.groups.all()[0].name == "HOD":
            return True
        return False

    # *since user clicked on the submit button,we'll assume the post has to be approved
    def form_valid(self, form):
        form.instance.status = "approved"
        messages.success(self.request, "Post Approved!")
        return super().form_valid(form)


class PostRejectView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["comments"]
    template_name = "main/post_confirm_reject.html"

    def test_func(self):
        post = self.get_object()
        if (
            self.request.user.groups.all()[0].name == "HOD"
            and post.status != "approved"
        ):
            return True
        return False

    # *Since user clicked on the submit button,we'll assume the post has to be rejected
    def form_valid(self, form):
        form.instance.status = "rejected"
        messages.success(self.request, "Post Rejected!")
        return super().form_valid(form)


# *Protection for pdf files(This view restricts pdf files to logged in users only):
@login_required
def getPDF(request, PDFfile):
    # check if there exists a post having this file in its PDFfile field:
    post = Post.objects.filter(PDFfile=PDFfile).first()
    # if not,raise a 404 error
    if post is None:
        raise Http404

    return FileResponse(
        open(os.path.join(settings.MEDIA_ROOT, PDFfile), "rb"),
        content_type="application/pdf",
    )
