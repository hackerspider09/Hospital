from django.db import models
from django.contrib.auth.models import AbstractUser

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
    
	
