from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta,datetime
from django.utils import timezone

def getPath(instance,filename):
    return str(f"Profile/{instance.username}/{filename}")

class User(AbstractUser):
	phone = models.CharField(max_length=14, blank=True, null=True)
	profile = models.ImageField(default="https://img.freepik.com/premium-vector/account-icon-user-icon-vector-graphics_292645-552.jpg?w=740",upload_to=getPath)
	address = models.TextField()
		
	def __str__(self):
	    return self.username
	
class Staff(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	joining_date = models.DateTimeField( auto_now_add=True)
	
	def __str__(self):
		return f"{self.user}"

def getUploadPath(instance,filename):
    return str(f"Blogs/{instance.doctor.username}/{filename}")  

class Blog(models.Model):
	doctor = models.ForeignKey(User, on_delete=models.CASCADE)
	category_choice = (
		("mental_health","Mental Health"),
		("heart_disease","Heart Disease"),
		("covid19","Covid19"),
		("immunization","Immunization")
	)
	category = models.CharField(max_length=25,choices=category_choice)
	title = models.CharField(max_length=50)
	image = models.ImageField(upload_to=getUploadPath)
	content = models.TextField()
	summary = models.TextField()
	status_choice = (
		("draft","Draft"),
		("published","Published"),
		("take_down","Take Down")
	)
	status = models.CharField(max_length=25,choices=status_choice)

class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments')
    specialty = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.DateTimeField()  
    duration = models.DurationField(default=timedelta(minutes=45))

    def save(self, *args, **kwargs):
        date_obj = datetime.strptime(self.date, '%Y-%m-%d').date()
        start_time_obj = datetime.strptime(self.start_time, '%H:%M').time()
        start_datetime = datetime.combine(date_obj, start_time_obj)
        print(self.date,self.start_time)
        print(start_datetime)
        # self.end_time = self.start_time + timedelta(minutes=45)
        # self.end_time = start_datetime + timedelta(minutes=45)
        start_datetime_aware = timezone.make_aware(start_datetime, timezone.get_current_timezone())
        self.end_time = start_datetime_aware + timedelta(minutes=45)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient}"
