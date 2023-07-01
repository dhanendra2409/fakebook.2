from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.conf import settings
from datetime import date
from helper import choice_keys 
from .managers import CustomUserManager

class User(AbstractUser):
   username=None
   fullname=models.CharField(max_length = 50,default=None)
   email=models.EmailField(_('email address'), unique = True)
   gender=models.CharField(max_length=10, choices= choice_keys.gender)
   dob=models.DateField(blank = True, null = True)
   phone_no=models.CharField(max_length = 10)
   
   USERNAME_FIELD='email'
   REQUIRED_FIELDS=['fullname']

   objects = CustomUserManager()

   def __str__(self):
       return f"{self.fullname}({self.id})"
   
class Posts(models.Model):
    title=models.CharField(max_length=200)
    description=models.CharField(max_length=500)
    file=models.FileField(upload_to='uploads/')
    created_date= models.DateTimeField(auto_now_add=True)  
    owner= models.ForeignKey(User,on_delete=models.CASCADE)
    liked_by=models.ManyToManyField(User,related_name='liked_by',null=True,blank=True,default=None)
    total_likes=models.IntegerField(default=0)   
 
    def __str__(self):
       return f"({self.id}){self.title}"
    
class Likes(models.Model):
    user = models.ForeignKey(User,related_name="likes",on_delete=models.CASCADE,null=True,blank=True)    
    post = models.ForeignKey(Posts,related_name="likes", on_delete=models.CASCADE,null=True,blank=True)  