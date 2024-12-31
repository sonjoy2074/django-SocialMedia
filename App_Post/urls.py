from App_Post import views
from django.urls import path
app_name = 'App_Post'

urlpatterns = [ 
    path('',views.home,name='home'),
    path('like_post/<pk>/',views.like_post,name='like_post'),
    path('unlike_post/<pk>/',views.unlike_post,name='unlike_post'),
    
]