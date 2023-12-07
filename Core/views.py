from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login , logout
from .models import *
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
    
        user = authenticate(username=username, password= password)
        if user is not None:
            login(request, user)

            try:
                staff_query = Staff.objects.get(user=user)
                return redirect(docter_page_view)
            except:
                return redirect(patient_page_view)
        else:
            messages.error(request,"User not Found")

    return render(request,"Core/login.html")
   
def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        address = request.POST['address']
        email = request.POST['email']
        phone_no = request.POST['phone']
        isDocter = request.POST.get("isDocter")
        # profile = request.FILES.get('profile_pic')
        if password1==password2:
            if User.objects.filter(username=username):
                messages.error(request,"User already Exists!")
                return redirect('signup')
            

            user = User.objects.create_user(username=username,first_name=fname,last_name=lname,password=password1,phone=phone_no,address=address,email=email)
            if len(request.FILES['profile_pic']):
                user.profile = request.FILES['profile_pic']
                user.save()
            if isDocter is not None:
                staff  = Staff.objects.create(user=user)

            messages.success(request,"Account Created")
        else:
            messages.error(request,"Password is not Matching")
        print(request)
    return render(request,"Core/signup.html")

    

@login_required(login_url="login")
@is_docter
def docter_page_view(request):
    user = User.objects.get(username=request.user)
    context ={
        'title':"Docter Dashboard",
        'user':user,
    }
    return render(request,"Core/docter.html",context=context)


@login_required(login_url="login")
@is_patient
def patient_page_view(request):
    user = User.objects.get(username=request.user)
    context ={
        'title':"Docter Dashboard",
        'user':user,
    }
    return render(request,"Core/patient.html",context=context)


# @login_required(login_url="login_view")
def logout_view(request):
    if request.user.is_authenticated:
        print("logged out")
        logout(request)
    return redirect(login_view)