from . import views
from .models import *
from django.shortcuts import redirect,HttpResponseRedirect
from django.contrib.auth import authenticate, login , logout

def is_docter(view_fun):
    def wrap(request,*args, **kwargs):
        user = User.objects.get(username=request.user)
        try:
            staff = Staff.objects.get(user=user)
            return view_fun(request,*args,**kwargs)
        except:
            logout(request)
            return redirect("login_view")
                            
    return wrap

def is_patient(view_fun):
    def wrap(request,*args, **kwargs):
        user = User.objects.get(username=request.user)
        try:
            staff = Staff.objects.get(user=user)
            return redirect("login_view")
            logout(request)
        except:
            return view_fun(request,*args,**kwargs)
                            
    return wrap