
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.db import models
from .models import *
from django.db.models import Q

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

from django.utils import timezone
from datetime import timedelta

from django.core import serializers


# Create your views here.
def home(request):
    search = ''
    if 'search' in request.GET:
        search = request.GET.get('search')
    rooms = Room.objects.filter(Q(search_keyword__icontains=search) |
                                Q(description__icontains=search) |
                                Q(host__username=search)
                                )
    keywords = Keyword.objects.annotate(
        total_search=models.Sum('search_keyword_users__total_search')
    ).all()

    users = User.objects.all()

    now = timezone.now()

    # implement from documentation 
    # today = Keywordsearch.objects.filter(created__lte=now.today())
    # last_seven_days = Keywordsearch.objects.filter(created__gt=F('created') + timedelta(days=7))
    
    result = Keywordsearch.objects.aggregate(
        total=models.Count('keyword'),
        today=models.Count('keyword',filter=models.Q(created__date=now.date())),
        yesterday = models.Count('keyword',filter=models.Q(created__date__gte=(now - timedelta(days=1)).date())),
        last_seven_days = models.Count('keyword',filter=models.Q(created__date__gte=(now - timedelta(days=7)).date())),
        last_30_days = models.Count('keyword',filter=models.Q(created__date__gte=(now - timedelta(days=30)).date())),
    )
    context = {
        'rooms': rooms,
        'keywords': keywords,
        'users': users,
        'result':result
    }
    return render(request, 'home.html', context)


@login_required(login_url='login')
def usearch(request):
    if request.method == "POST":
        # user = request.POST.get('username')
        user = request.user
        keyword = request.POST.get('search')
        print(keyword)
        try:
            keyword_obj = Keyword.objects.get(name=keyword)
        # new_data.save()
        except Keyword.DoesNotExist:
            keyword_obj = Keyword.objects.create(name=keyword)

        if keyword_obj:

            try:
                user_keyword = Keywordsearch.objects.get(keyword=keyword_obj, user=user)
                user_keyword.total_search += 1
                user_keyword.save()
            # new_data.save()
            except Keywordsearch.DoesNotExist:
                Keywordsearch.objects.create(keyword=keyword_obj, user=user, total_search=1)

        return redirect('home')


def loginUser(request):
    page = 'login'
    if request.method == 'POST':
        # get username and password form user input 
        username = request.POST.get('username')
        password = request.POST.get('password')

        # check this user exit or not 
        try:
            user = User.objects.get(username=username)
        except:
            return HttpResponse('User does not exit')

        # if user exit make sure the credential is correct or not 
        user = authenticate(request, username=username, password=password)

        # login user and create the session on db browser and redirect home page 
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('Username or Password does not exit')

    context = {'page': page}
    return render(request, 'login_register.html', context)


def logoutPage(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username
            user.save()
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('An error occured during registrations')

    context = {'form': form}
    return render(request, 'login_register.html', context)


def showusername(request):
    all_users = User.objects.all()
    context = {
        'all_users': all_users
    }
    return render(request, 'home.html', context)


def everyusersearch(request,pk):
    user = User.objects.get(id=pk)
    user_srch = user.search_keywords.all()
    # print(user_srch)
    context = {
        'user_search':user_srch
    }
    return render(request, 'all_user.html', context)


def timerange(request):
    now = timezone.now()

    # implement from documentation 
    # today = Keywordsearch.objects.filter(created__lte=now.today())
    # last_seven_days = Keywordsearch.objects.filter(created__gt=F('created') + timedelta(days=7))
    
    result = Keywordsearch.objects.aggregate(
        total=models.Count('keyword'),
        yesterday = models.Count('keyword',filter=models.Q(created__date__gte=(now - timedelta(hours=24)).date())),
        last_seven_days = models.Count('keyword',filter=models.Q(created__date__gte=(now - timedelta(days=7)).date())),
        last_30_days = models.Count('keyword',filter=models.Q(created__date__gte=(now - timedelta(days=30)).date())),
    )
    context = {
        'result':result
    }
    return render(request, 'home.html',context)

 
def tuto(request,pk):
    user = User.objects.get(id=pk)
    tasks=  user.search_keywords.all()
    
    if request.is_ajax():
        task_serializers = serializers.serialize('json', tasks)
        return JsonResponse(task_serializers, safe=False)
    return JsonResponse({'message':'Wrong validation'})
