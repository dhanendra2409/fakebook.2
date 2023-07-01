from django.urls import path
from myapp import apis as myapp_apis
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [

    path('register/',myapp_apis.RegisterView.as_view(),name='register'),
    path('login/',myapp_apis.loginView.as_view(),name='login'),
    path('postcreate/',myapp_apis.CreatePostView.as_view(),name='post_create'),
    path('viewpost/',myapp_apis.GetPostView.as_view(),name='view_post'),
    path('editpost/<int:pk>/',myapp_apis.EditPostView.as_view(),name='edit_post'),
    path('userpost/',myapp_apis.UserWisePost.as_view(),name='user_post'),
    path('postlike/<int:pk>/',myapp_apis.LikePostView.as_view(),name='post_like'),
    path('unlike/<int:pk>/',myapp_apis.unlikePostView.as_view(),name='post_like'),
    path('comment/<int:pk>/',myapp_apis.CommentAPIView.as_view(),name='post_comment'),
    
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)