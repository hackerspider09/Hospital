from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login , logout
from .models import *
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib import messages
from django.views.generic import UpdateView, CreateView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.decorators import method_decorator
from createEvent import main

def login_view(request):
    # main()
    # create_event_for_new_user()
    try:
        user= User.objects.get(username=request.user)
        try:
            staff_query = Staff.objects.get(user=user)
            return redirect(docter_page_view)
        except:
            return redirect(patient_page_view)
    except:
        pass

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
    # try:
    #     main()
    # except:
    #     pass
    user = User.objects.get(username=request.user)

    blogs = Blog.objects.filter(doctor=request.user).order_by("status")
    appointment = Appointment.objects.filter(doctor=request.user)
    context ={
        'title':"Docter Dashboard",
        'user':user,
        'blogs':blogs,
        'appointments':appointment
    }
    return render(request,"Core/docter.html",context=context)


@login_required(login_url="login")
@is_patient
def patient_page_view(request):
    user = User.objects.get(username=request.user)
    blogs = Blog.objects.filter(status="published").order_by("title")
    appointment = Appointment.objects.filter(patient=request.user)
    context ={
        'title':"Patient Dashboard",
        'user':user,
        "blogs":blogs,
        'appointments':appointment,
    }
    return render(request,"Core/patient.html",context=context)

def doctor_list(request):
    doctors = Staff.objects.all()
    return render(request, 'Core/listDocters.html', {'doctors': doctors})

# @login_required(login_url="login_view")
def logout_view(request):
    if request.user.is_authenticated:
        print("logged out")
        logout(request)
    return redirect(login_view)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['category', 'title', 'image','content','summary','status']
    template_name = 'Core/create.html'

    @method_decorator(is_docter)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        if self.object.status == 'published':
            return reverse('docter_page_view')  # Redirect to home page for published blogs
        elif self.object.status == 'draft':
            return reverse('update_blog', kwargs={'pk': self.object.pk})  # Redirect to update page for draft blogs
    
    
    def form_valid(self, form):
        print(self.request.user)
        form.instance.doctor = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ['category','title','image','content','summary','status']

    template_name ='Core/create.html'

    def get_success_url(self):
        if self.object.status == 'published':
            return reverse('docter_page_view')  # Redirect to home page for published blogs
        elif self.object.status == 'draft':
            return reverse('update_blog', kwargs={'pk': self.object.pk})  


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostDetailView(DetailView):
    model = Blog
    template_name ='Core/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context["blog"].doctor)
        return context
    

def make_appointment(request, docterId):
    try:
        print(docterId)
        doctor = User.objects.get(id=docterId)  
        print(docterId)
        print(doctor.username)
    except:

        return render(request, 'Core/bookAppointment.html', { 'doctor': doctor})



    if request.method == 'POST':
        specialty = request.POST['specialty']
        date = request.POST['date']
        start_time = request.POST['start_time']

        # Create the appointment instance
        appointment = Appointment(
            doctor=doctor,
            patient=request.user,
            specialty=specialty,
            date=date,
            start_time=start_time,
            # Add more fields and data as needed
        )
        appointment.save()

        main(appointment)

        # return HttpResponseRedirect('/bookappointment/')  
        return HttpResponseRedirect(reverse('view_appointment', kwargs={'pk': appointment.id}))


    else:
        return render(request, 'Core/bookAppointment.html', {'doctor': doctor})
    
class AppointmentDetailView(DetailView):
    model = Appointment
    template_name ='Core/appointmentDetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context