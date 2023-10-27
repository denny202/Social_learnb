from django.contrib import admin
from .models import Profile ,Post,LikePost,No_Followers

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(No_Followers)
# Register your models here.
