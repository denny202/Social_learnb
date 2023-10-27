from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns= [ 
    path('',views.index,name='index'),
    path('settings',views.settings,name='settings'),
    path('upload',views.upload,name='upload'),
    path('profile/<str:pk>',views.profile,name='profile'),
    path('like-post',views.like_post,name='like-post'),
    path('follow',views.follow,name='follow'),
    path('search',views.search,name='search'),
    path('signup',views.signup,name='signup'),
    path('signin',views.signin,name='signin'),
    path('logout',views.logout,name='logout'),
    path('test',views.test,name='test'),
    
]