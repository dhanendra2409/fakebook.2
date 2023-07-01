from myapp import models as myapp_models
from django.http import Http404
""" """

class PostFunction:
    def all_posts():
        queryset = myapp_models.Posts.objects.all()
        return queryset
    
    
class GetObject:
    def get_object(self,pk):
        try:
            return myapp_models.Posts.objects.get(id=pk)
        except myapp_models.Posts.DoesNotExist:
            raise Http404    
