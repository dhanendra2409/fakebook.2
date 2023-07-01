from myapp import models as myapp_models



class PostFunction:
    def all_posts():
        queryset = myapp_models.Posts.objects.all()
        return queryset