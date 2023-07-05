from django.shortcuts import render
from django.shortcuts import render
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import get_user_model
from helper.functions import *
User = get_user_model()
def get_tokens(user):
     refresh = RefreshToken.for_user(user)
     return{
          'refresh': str(refresh),
          'access': str(refresh.access_token),
    }


# Create your views here.
class RegisterView(APIView):
    def post(self, request, format=None):
        serializer = RegistrationsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Registered successfully'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class loginView(APIView):
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens(user)
                return Response({'token':token,'msg':'logged in successfully'},status=status.HTTP_200_OK)
            return Response({'errors': 'Email or Password is not valid'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class CreatePostView(APIView):
    authentication_classes= [JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self, request):
          print(request.data)
          serializer = CreatePostSerializer(data=request.data)
          if serializer.is_valid():
               serializer.save(owner=request.user)
               return Response({'msg':'post Created'},status=status.HTTP_201_CREATED)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class GetPostView(APIView):
    authentication_classes= [JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request):    
        # data = Posts.objects.all()
        data = PostFunction.all_posts()
        serializer = PostSerializer(data, many=True,context={'request':request})
        return Response(serializer.data)
    
class EditPostView(APIView):
   authentication_classes= [JWTAuthentication]
   permission_classes=[IsAuthenticated]
   def get_object(self, pk):
        try:
            return Posts.objects.get(id=pk)
        except Posts.DoesNotExist:
            raise Http404    

   def patch(self, request, pk, format=None):
        post = self.get_object(pk)
        if post is None:
            return Response({'error':'Post Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post, data=request.data,partial=True)
        if serializer.is_valid():
            if post.owner.id == request.user.id: 
              serializer.save()
              return Response(serializer.data)
            return Response({'error':'You are not authorized to edit this post'},status=status.HTTP_401_UNAUTHORIZED)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
   def delete(self, request, pk, format=None):
        post= self.get_object(pk)
        if post is None:
            return Response({'error':'Post Not found'}, status=status.HTTP_404_NOT_FOUND)
        if post.owner.id == request.user.id: 
            post.delete()
            return Response({'res':'Post Deleted Successfully'})
        return Response({'error':'you are not authorized to delete this file'},status=status.HTTP_401_UNAUTHORIZED)
   

class UserWisePost(APIView):
    authentication_classes= [JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        user = request.user
        user_post = Posts.objects.filter(owner=user)
        print("user_post",user_post)
        serializer= PostSerializer(user_post,many=True,context={'request':request})

        return Response(serializer.data, status=status.HTTP_200_OK)
                
    
class LikePostView(APIView):
    authentication_classes= [JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Posts.objects.get(pk = pk)
        except Posts.DoesNotExist:
            return None

    def post(self, request, pk, *args, **kwargs):
        post = self.get_object(pk)
        if post is None:
            return Response({'error': 'Post not found'}, status = status.HTTP_404_NOT_FOUND) 
        liked_by = post.likepost.all().values_list('user', flat = True)
        if request.user.id in liked_by:
            post.total_likes -= 1
            post.liked_by.remove(request.user)
            post.likepost.filter(user = request.user).delete()
        else:
            post.total_likes += 1
            post.liked_by.add(request.user)
            like = Likes(user = request.user, post = post)
            like.save()
        post.save()
        return Response({'msg':'Response Accepted'}, status = status.HTTP_200_OK)

class CommentAPIView(APIView):
    authentication_classes= [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Posts.objects.get(pk = pk)
        except Posts.DoesNotExist:
            return None
    
    def get(self, request, pk, *args, **kwargs):
        post = self.get_object(pk)
        if post is None:
            return Response({'error': 'Post not found'}, status = status.HTTP_404_NOT_FOUND)
        comments = Comments.objects.filter(post = post)
        serializer = CommentSerializer(comments, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request, pk, *args, **kwargs):
        post = self.get_object(pk)
        if post is None:
            return Response({'error': 'Post not found'}, status = status.HTTP_404_NOT_FOUND)
        data = {
            'user': request.user,
            'post': post.id,
            'body': request.data.get('body')
        }
        serializer = CommentSerializer(data = data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            post.save()
            return Response({'msg':'Comment Posted Successfully'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
class EditCommentView(APIView):
   authentication_classes= [JWTAuthentication]
   permission_classes=[IsAuthenticated]
   def get_object(self, pk):
        try:
            return Comments.objects.get(id=pk)
        except Comments.DoesNotExist:
            raise Http404    

   def patch(self, request, pk, format=None):
        post = self.get_object(pk)
        if post is None:
            return Response({'error':'Comment Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(post, data=request.data,partial=True)
        if serializer.is_valid():
            if post.user.id == request.user.id: 
              serializer.save()
              return Response(serializer.data)
            return Response({'error':'You are not authorized to edit this post'},status=status.HTTP_401_UNAUTHORIZED)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
   def delete(self, request, pk, format=None):
        post= self.get_object(pk)
        if post is None:
            return Response({'error':'Comment Not found'}, status=status.HTTP_404_NOT_FOUND)
        if post.user.id == request.user.id: 
            post.delete()
            return Response({'res':'Post Deleted Successfully'})
        return Response({'error':'you are not authorized to delete this file'},status=status.HTTP_401_UNAUTHORIZED)
   



    

