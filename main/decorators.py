from django.http import HttpResponse
from django.shortcuts import redirect
#*This decorator will not display the login page to users that are already logged in:
def prevent_relogin(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request,*args,**kwargs)
    return wrapper_func

#*This decorator will allow only users belonging to certain groups to access the view:
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            group=None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request,*args,**kwargs)
            else:
                return HttpResponse('<h1>You are not authorized to view this page</h1>')
        return wrapper_func
    return decorator