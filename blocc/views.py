from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .email import send_priority_email
from .forms import *
from decouple import config,Csv
import datetime as dt
from django.http import JsonResponse
from .forms import SignupForm
import json
from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
# from .serializer import


# Create your views here.
def Signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			User.objects.create_user(username=username, email=email, password=password)
			return redirect('create-profile')
	else:
		form = SignupForm()
	
	context = {
		'form':form,
	}
	return render(request, 'registration/signup.html', context)

def index(request):
    try:
        if not request.user.is_authenticated:
            return redirect('/accounts/login/')
        current_user=request.user
        profile =Profile.objects.get(username=current_user)
        healthservices = Health.objects.filter(block=profile.block)
        authorities = Authorities.objects.filter(block=profile.block)
        businesses = Business.objects.filter(block=profile.block)

        if request.method=="POST":
            form =BusinessForm(request.POST,request.FILES)
            if form.is_valid():
                business = form.save(commit = False)
                business.owner = current_user
                business.block = profile.block
                business.save()

            return HttpResponseRedirect('/')

        else:
            form = BusinessForm()
    except ObjectDoesNotExist:
        return redirect('create-profile')

    return render(request,'index.html',{"healthservices":healthservices, "authorities":authorities, "businesses":businesses, "form":form})

@login_required(login_url='/accounts/login/')
def search_results(request):
    if 'business' in request.GET and request.GET["business"]:
        search_term = request.GET.get("business")
        searched_businesses = Business.search_business(search_term)
        message=f"{search_term}"

        print(searched_businesses)

        return render(request,'search.html',{"message":message,"businesses":searched_businesses})
    else:
        message="You haven't searched for any term"
        return render(request,'search.html',{"message":message})

@login_required(login_url='/accounts/login/')
def notification(request):
    current_user=request.user
    profile=Profile.objects.get(username=current_user)
    all_notifications = Notification.objects.filter(block=profile.block)

    if request.method=="POST":
        form =NotificationsForm(request.POST,request.FILES)
        if form.is_valid():
            notification = form.save(commit = False)
            notification.author = current_user
            notification.block = profile.block
            notification.save()

            if notification.priority == 'High Priority':
                send_priority_email(profile.name,profile.email,notification.title,notification.notification,notification.author,notification.block)

        return HttpResponseRedirect('/notifications')


    else:
        form = NotificationsForm()
    return render(request,'notifications.html',{"notifications":all_notifications, "form":form})

@login_required(login_url='/accounts/login/')
def blog(request):
    current_user=request.user
    profile=Profile.objects.get(username=current_user)
    blogposts = Post.objects.filter(block=profile.block)

    if request.method=="POST":
        form =PostForm(request.POST,request.FILES)
        if form.is_valid():
            blogpost = form.save(commit = False)
            blogpost.username = current_user
            blogpost.block = profile.block
            blogpost.avatar = profile.avatar
            blogpost.save()

        return HttpResponseRedirect('/blog')

    else:
        form = PostForm()
    return render(request,'blog.html',{"blogposts":blogposts, "form":form})

@login_required(login_url='/accounts/login/')
def view_blog(request,id):
    current_user = request.user

    try:
        comments = Comment.objects.filter(post_id=id)
    except:
        comments =[]

    blog = Post.objects.get(id=id)
    if request.method =='POST':
        form = CommentForm(request.POST,request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.username = current_user
            comment.post = blog
            comment.save()
    else:
        form = CommentForm()

    return render(request,'view_blog.html',{"blog":blog,"form":form,"comments":comments})

@login_required(login_url='/accounts/login/')
def my_profile(request):
    current_user=request.user
    profile =Profile.objects.get(username=current_user)
    if request.method=="POST":
        instance = Profile.objects.get(username=current_user)
        form =ProfileForm(request.POST,request.FILES,instance=instance)
        if form.is_valid():
            profile = form.save(commit = False)
            profile.username = current_user
            profile.save()

        return redirect('my-profile')

    elif Profile.objects.get(username=current_user):
        profile = Profile.objects.get(username=current_user)
        form = ProfileForm(instance=profile)
    else:
        form = ProfileForm()

    return render(request,'user_profile.html',{"profile":profile, "form":form})

@login_required(login_url='/accounts/login/')
def create_profile(request):
    current_user=request.user
    if request.method=="POST":
        form =ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            profile = form.save(commit = False)
            profile.username = current_user
            profile.save()
        return HttpResponseRedirect('/')

    else:

        form = ProfileForm()
    return render(request,'profile_form.html',{"form":form})



