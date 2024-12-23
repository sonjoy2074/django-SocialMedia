from django.shortcuts import render
from App_Login.forms import CreateNewUser
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from App_Login.models import UserProfile
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
def sign_up(request):
    form = CreateNewUser()
    registered = False
    if request.method == 'POST':
        form = CreateNewUser(request.POST)
        if form.is_valid():
            user=form.save()
            registered = True
            user_profile = UserProfile(user=user)
            pass
    return render(request, 'App_Login/sign_up.html', {'form': form, 'title': 'Sign Up'})

def login_page(request):
    form=AuthenticationForm()
    if request.method == 'POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))