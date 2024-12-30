from django.shortcuts import render
from App_Login.forms import CreateNewUser, EditProfile
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from App_Login.models import UserProfile, Follow
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from App_Post.forms import PostForm
from django.contrib.auth.models import User
def sign_up(request):
    form = CreateNewUser()
    registered = False
    if request.method == 'POST':
        form = CreateNewUser(request.POST)
        if form.is_valid():
            user=form.save()
            registered = True
            user_profile = UserProfile(user=user)
            user_profile.save()
            return HttpResponseRedirect(reverse('App_Login:login'))
    return render(request, 'App_Login/sign_up.html', {'form': form, 'title': 'Sign Up'})

def login_page(request):
    form=AuthenticationForm()
    if request.method == 'POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('App_Post:home'))
    return render(request, 'App_Login/login.html', {'form': form, 'title': 'Login'})

@login_required
def edit_profile(request):
    current_user = UserProfile.objects.get(user=request.user)
    form=EditProfile(instance=current_user)
    if request.method == 'POST':
        form=EditProfile(request.POST,request.FILES, instance=current_user)
        if form.is_valid():
            form.save(commit=True)
            form=EditProfile(instance=current_user)
            return HttpResponseRedirect(reverse('App_Post:home'))
    return render(request, 'App_Login/profile.html',context={'title': 'Edit Profile', 'form': form})    

@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('App_Login:login'))

@login_required
def profile(request):
    form=PostForm()
    if request.method == 'POST':
        form=PostForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.save()
            return HttpResponseRedirect(reverse('App_Post:home'))
    return render(request, 'App_Login/user.html', context={'title': 'Profile' , 'form': form})

@login_required
def user_profile(request, username):
    user_profile = User.objects.get(username=username)
    already_followed = Follow.objects.filter(following=user_profile, follower=request.user) 
    if user_profile == request.user:
        return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request, 'App_Login/user_profile.html', context={'title': 'User Profile', 'user_profile': user_profile, 'already_followed': already_followed})


@login_required
def follow(request, username):
    following_user = User.objects.get(username=username)
    follower_user = request.user
    already_following = Follow.objects.filter(following=following_user, follower=follower_user)
    if not already_following:
        followed_user = Follow(following=following_user, follower=follower_user)
        followed_user.save()
    return HttpResponseRedirect(reverse('App_Login:user_profile', kwargs={'username': username}))

@login_required
def unfollow(request, username):
    following_user = User.objects.get(username=username)
    follower_user = request.user
    already_following = Follow.objects.filter(following=following_user, follower=follower_user)
    if already_following:
        already_following.delete()
    return HttpResponseRedirect(reverse('App_Login:user_profile', kwargs={'username': username}))