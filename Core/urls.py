"""
URL configuration for Hospital project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_view,name="second_login"),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('docter/', views.docter_page_view, name='docter_page_view'),
    path('patient/', views.patient_page_view, name='patient_page_view'),
    path('bookappointment/', views.doctor_list, name='doctor_list_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('blog/create/', views.PostCreateView.as_view(), name='create_blog'),
    path('blog/update/<int:pk>/', views.PostUpdateView.as_view(), name='update_blog'),
    path('blog/view/<int:pk>/', views.PostDetailView.as_view(), name='view_blog'),
    path('view/appointment/<int:pk>/', views.AppointmentDetailView.as_view(), name='view_appointment'),
    path('makeappointment/<int:docterId>/', views.make_appointment, name='make_appointment'),
]
