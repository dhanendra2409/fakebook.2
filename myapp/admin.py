from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
  list_display =['fullname', 'email','dob','gender','phone_no']
  search_fields = ['fullname', 'email', 'phone_no']
  list_filter = ['gender','dob']
  list_editable=['dob']
   
class PostAdmin(admin.ModelAdmin):
  list_display =['title','id', 'owner','total_likes','created_date','updated_date']
  list_filter = ['owner','created_date']

class LikeAdmin(admin.ModelAdmin):
  list_display =['user', 'post','created_date','updated_date']
  list_filter = ['user','post','created_date']

class CommentAdmin(admin.ModelAdmin):
  list_display =['user', 'post', 'body','created_date','updated_date']
  list_filter = ['user', 'post','created_date']

admin.site.register(User, UserAdmin)
admin.site.register(Posts, PostAdmin)
admin.site.register(Likes, LikeAdmin)
admin.site.register(Comments, CommentAdmin)
