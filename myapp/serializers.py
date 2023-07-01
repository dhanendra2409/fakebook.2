from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()


class RegistrationsSerializer(serializers.ModelSerializer):
    confirm_pass = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['id','fullname','email','gender','dob','phone_no','password','confirm_pass']
        extra_kwargs={
            'password':{'write_only':True}
        }

    def validate(self,attrs):
        password =attrs.get('password')   
        password2 =attrs.get('confirm_pass')   
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs
    
    def create(self, validate_data):
       return User.objects.create_user( **validate_data)

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=150)
    class Meta:
        model = User
        fields = ['email','password']
    

class ProfileSerializer(serializers.ModelSerializer):
   class Meta:
         model = User
         fields = ['id','fullname','email','gender','dob','phone_no']



class CreatePostSerializer(serializers.ModelSerializer):
    owner=serializers.SerializerMethodField(read_only=True)
    # liked_by=ProfileSerializer(many=True)
    class Meta:
        model = Posts
        fields = ['id','title','description','file','created_date','owner','total_likes']
    
    def get_owner(self,instance):
        user = instance.owner
        return ProfileSerializer(user).data

class PostSerializer(serializers.ModelSerializer):
    owner=serializers.SerializerMethodField(read_only=True)
    liked_by=ProfileSerializer(many=True)
    class Meta:
        model = Posts
        fields = ['id','title','description','file','created_date','owner','liked_by','total_likes']
    
    def get_owner(self,instance):
        user = instance.owner
        return ProfileSerializer(user).data
    
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields=['id','user','post']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.fullname')
    class Meta:
        model = Comments
        fields = ('id', 'user', 'post', 'body', 'created')        