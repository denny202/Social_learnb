from django.shortcuts import render,redirect
from django.http import HttpResponse
#import auth allow to authenticate user 
from django.contrib.auth.models import User, auth
#import messages for errors 
from django.contrib import messages 
#import model
from .models import Profile,Post,LikePost,No_Followers
import random

from django.contrib.auth.decorators import login_required

from itertools import chain

@login_required(login_url='signin')
def index (request):
    user_object=User.objects.get(username=request.user.username)
    user_profile=Profile.objects.get(user=user_object)
    user_following_list=[]
    feed=[]
    user_following=No_Followers.objects.filter(follower=request.user.username)
    for users in user_following:
        user_following_list.append(users.user)
    
    for usernames in user_following_list:
        feed_list=Post.objects.filter(user=usernames)
        feed.append(feed_list)
        
    feed_list=list(chain(*feed))
        
    

#user suggestion

    #get all users 
    all_users=User.objects.all()
    
    #all the people already following
    user_following_all=[]


    for user in user_following:
        user_list=User.objects.get(username=user.user)
        user_following_all.append(user_list)


    new_suggestions_list=[x for x in list (all_users) if (x not in list (user_following_all))]
    #cant suggest current user to himself
    
    current_user=User.objects.filter(username=request.user.username)

    final_suggestions_list=[x for x in list (new_suggestions_list) if (x not in list(current_user))]

    random.shuffle(final_suggestions_list)

#get profile obj to show pic bio and username
    username_profile=[]
    username_profile_list=[]

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists=Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)


    suggestions_username_profile_list = list (chain(*username_profile_list))
    print(user_profile.profileimg.url)



    return render (request, 'index.html',{'user_profile':user_profile, 'posts':feed_list,'suggestions_username_profile_list':suggestions_username_profile_list[:4]})

@login_required(login_url='signin')
def profile (request,pk):
    user_object=User.objects.get(username=pk)
    user_profile= Profile.objects.get(user=user_object)
    user_posts=Post.objects.filter(user=pk)
    user_post_len=len(user_posts)


    follower=request.user.username
    user=pk

    if No_Followers.objects.filter(follower=follower,user=user).first():
        btn_text='Unfollow'
    else:
        btn_text='Follow'

    user_followers=len(No_Followers.objects.filter(user=pk))
    user_following=len(No_Followers.objects.filter(follower=pk))


    #context is used when you pass a lot of data
    context = {
        'user_object':user_object,
        'user_profile':user_profile,
        'user_posts':user_posts,
        'user_post_len':user_post_len,
        'btn_text':btn_text,
        'user_followers':user_followers,
        'user_following':user_following,


    }

    return render(request,'profile.html',context)


@login_required(login_url='signin')
def search(request): 
    user_object=User.objects.get(username=request.user.username)
    user_profile=Profile.objects.get(user=user_object)



    if request.method=='POST':
        username=request.POST['username']
        username_object=User.objects.filter(username__icontains=username)
        
        username_profile=[]
        username_profile_list=[]

        for users in username_object:
            username_profile.append(users.id)
            

        for ids in username_profile:
            profile_lists=Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)

        
        username_profile_list =list(chain(*username_profile_list))

    return render (request,'search.html',{'user_profile':user_profile,'username_profile_list':username_profile_list})



@login_required(login_url='signin')
def like_post (request):
    username=request.user.username
    post_id=request.GET.get('post_id')

    post=Post.objects.get(id=post_id)

    like_filter=LikePost.objects.filter(post_id=post_id,username=username).first()

    if like_filter==None:
        new_like=LikePost.objects.create(post_id=post_id,username=username)
        new_like.save()
        post.no_of_likes=post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes=post.no_of_likes-1
        post.save()
        return redirect('/')

@login_required(login_url='signin')
def follow (request):
    if request.method=='POST':
        follower=request.POST['follower']
        user=request.POST['user']

        if No_Followers.objects.filter(follower=follower,user=user).first():
            delete_follower=No_Followers.objects.get(follower=follower,user=user)
            delete_follower.delete()
            return redirect ('/profile/'+user)
        
        else:
            new_follower=No_Followers.objects.create(follower=follower,user=user)
            new_follower.save()
            return redirect ('/profile/'+user)
    else:
        return redirect('/')


@login_required(login_url='signin')
def upload (request):
    
    if request.method=='POST':
        user=request.user.username
        image=request.FILES.get('image_upload')
        caption=request.POST.get('caption')

        new_post=Post.objects.create(user=user,image=image,caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect ('/')
   

@login_required(login_url='signin')
def settings(request): 

    #get profile object logged in user 
    user_profile=Profile.objects.get(user= request.user)

    if request.method == 'POST':
        
        if request.FILES.get('image')==None:

                image=user_profile.profileimg
                bio=request.POST['bio'] 
                location = request.POST['location']

                user_profile.profileimg=image
                user_profile.bio=bio
                user_profile.location=location
                user_profile.save()
        if request.FILES.get('image')!=None:
            image=user_profile.profileimg
            bio=request.POST['bio'] 
            location = request.POST['location']

            user_profile.profileimg=image
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()
        return redirect('settings')


    return render (request,'setting.html',{'user_profile':user_profile})



def signup(request):

    if request.method =='POST':
        username = request.POST ['username']
        email = request.POST [ 'email']
        password = request.POST [ 'password']
        password2 = request.POST [ 'password2']
        if password==password2:
            #check if email is already used 
            if User.objects.filter(email=email).exists():
                messages.info(request,'email already in use')
                return redirect('signup')
#check if username is already used 
            elif User.objects.filter(username=username).exists():
                messages.info(request,'username already in use')
                return redirect('signup')
            else:
                #save user object 
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()
                
                #log user in and redirect to profile setup
                user_login = auth.authenticate(username=username,password=password)
                auth.login(request,user_login)

                #create a profile object 
                user_model=User.objects.get(username=username)
                new_profile=Profile.objects.create(user=user_model,id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request,'Password not matching')
            return redirect('signup')
        

        
    return render(request, 'signup.html')

def signin(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        user=auth.authenticate(username=username,password=password)
        #if we have in db is not none
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Error not valid')
            return redirect('signin')
            
    else:
            return render(request,'signin.html')


@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')



def test(request):
    return render(request,'signin1.html')