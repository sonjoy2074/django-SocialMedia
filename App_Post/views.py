from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required   
from App_Login.models import UserProfile, Follow 
from django.contrib.auth.models import User
from App_Post.models import Post, Like
# Create your views here.

@login_required
def home(request):
    following_list = Follow.objects.filter(follower=request.user)
    following_users = [follow.following for follow in following_list]
    posts = Post.objects.filter(author__in=following_users).order_by('-upload_date')
    liked_post = Like.objects.filter(user=request.user)
    like_post_list = liked_post.values_list('post', flat=True)
    if request.method == 'GET':
        search = request.GET.get('search', '')
        result = User.objects.filter(username__icontains=search)
    
    return render(request, 'App_Post/home.html', {
        'title': 'Home',
        'search': search,
        'result': result,
        'following_list': following_list,
        'posts': posts,
        'like_post_list': like_post_list

    })


@login_required
def like_post(request, pk):
    post = Post.objects.get(pk=pk)
    already_liked = Like.objects.filter(post=post, user=request.user)
    if not already_liked:
        liked_post = Like(post=post, user=request.user)
        liked_post.save()
    return HttpResponseRedirect(reverse('App_Post:home'))


@login_required
def unlike_post(request, pk):
    post = Post.objects.get(pk=pk)
    already_liked = Like.objects.filter(post=post, user=request.user)
    already_liked.delete()
    return HttpResponseRedirect(reverse('App_Post:home'))
