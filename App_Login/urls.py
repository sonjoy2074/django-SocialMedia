from django.urls import path
from App_Login import views

app_name = 'App_Login'
urlpatterns = [ 
 path('signup/', views.sign_up, name='signup'),
 path('login/', views.login_page, name='login'),
 path('edit_profile/', views.edit_profile, name='edit_profile'),
 path('logout/', views.logout_user, name='logout'),
]