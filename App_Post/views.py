from django.shortcuts import render
from django.http import HttpResponse  
from django.contrib.auth.decorators import login_required   
from django.contrib.auth.models import User
# Create your views here.

@login_required
def home(request):
    if request.method =='GET':
        search = request.GET.get('search','')
        result= User.objects.filter(username__icontains=search)
    return render(request, 'App_Post/home.html', {'title': 'Home' ,'search': search, 'result': result})
