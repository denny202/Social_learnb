from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User=get_user_model()

# Create your models here.
class Profile (models.Model):
	
    user=models.ForeignKey (User,on_delete=models.CASCADE ,related_name="profile")
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
	#this image needs to be stored somewhere 
    profileimg=models.ImageField(upload_to='profile_images/',default='default_user.jpg')
    location=models.CharField(max_length=100,blank=True)


def __str__(self):
    return self.user.username



class Post(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    user=models.CharField(max_length=100)
    #author = models.ForeignKey(User, on_delete=models.CASCADE)
    image=models.ImageField(upload_to='post_img')
    caption=models.TextField()
    created_at=models.DateTimeField(default=datetime.now)
    no_of_likes=models.IntegerField(default=0)
  


    def __str__(self):
        return self.user
    
class Comment(models.Model):
    post=models.ForeignKey(Post,related_name="comments" ,on_delete=models.CASCADE)
    username=models.CharField(max_length=100)
    body=models.TextField()
    date= models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '%s - %s ' % (self.post.caption,self.username)
    
class LikePost(models.Model):
    post_id=models.CharField(max_length=500)
    username=models.CharField(max_length=100)

    def __str__(self):
        return self.username
    

class No_Followers(models.Model):
    follower=models.CharField(max_length=100)
    user=models.CharField(max_length=100)

    def __str__(self):
        return self.user


    