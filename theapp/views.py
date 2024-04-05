from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from datetime import date, timezone, datetime
# from .forms import *
from django.db.models import Prefetch, Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.exceptions import ObjectDoesNotExist
from . forms import *
from . models import *
import random
# Create your views here.

def checkBookLibrary(profile, book):
    if book in profile.books.all():
        return True
    else:
        return False

def index(response):
    user = None
    if response.user.is_authenticated:
        user = response.user
        p = user.profile
        added = p.books.all()
        # Reccomendation algorithm, based on User preferred genre,
        pref_array = user.profile.preference.split(",") # Create an array of user's preference
        prefs = [x.strip(' ') for x in pref_array] # Clean the array
        queries = [Q(genre__contains=pref) for pref in pref_array] # 
        combined_pref = queries[0]
        for query in queries[1::]:
            combined_pref != query
        
        filtered_queryset = Series.objects.filter(combined_pref)
        recc = filtered_queryset.exclude(pk__in=added.values_list('pk', flat=True))
        randomed = list(recc)
        ran_rec = random.sample(randomed, 5)

        print(added)
        print(f"user id : {user.id}")
        print(f"profile id : {p.id}")
        print('=========== This is my Library ===========')
        for mybook in added:
            print(f"{mybook.title} : {mybook.id}")
        print('=========== This is the Recommended ===========')
        for b in recc:
            print(f"{b.title} : {b.id}")
        print('=========== End ===========')

        context = {
            'user' : user,
            'pref_array' : pref_array,
            'ran_rec' : ran_rec
        }
        return render(response, 'base_base-index.html', context)
    else:
        return render(response, 'base_base-index.html')


@login_required
def profile(request):
    user = request.user
    profile = user.profile
    if request.method == 'POST':
        form = SetProfile(request.POST, instance=profile)
        if form.is_valid():
            form.save()
        
        return render(request, 'user_profile.html')
    else:
        form = SetProfile(instance=profile)
                
    context = { 
        'user' : user, 
        'profile' : profile,
        'form' : form
    }
    return render(request, 'base_user-profile.html', context)

@login_required
def library(request):
    user = request.user
    p = user.profile
    user_book = p.books.all()
    print(user_book)
    context = {
        'user' : user,
        'user_book' : user_book
    }
    return render(request, 'base_user-library.html', context)

def view_book(request, id):
    user = request.user
    profile = user.profile
    book = Series.objects.get(pk=id)
    volume = book.volume_set.all()
    genres = book.genre
    genres = genres.replace(" ", "")
    genres = genres.split(",")
    if request.method == 'POST':
        if checkBookLibrary(profile, book):
            profile.books.remove(book)
        else:
            profile.books.add(book)
        messages.success(request, "Added to library")
        return render(request, 'base_book-view.html', {'book' : book, 'volume' : volume, 'genres' : genres})
    else:
        status =  checkBookLibrary(profile, book)
        return render(request, 'base_book-view.html', {'book' : book, 'volume' : volume, 'genres' : genres, 'status' : status})

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"you are logged as {username}")
                return redirect("theapp:index")
            else:
                messages.error(request, "Invalid username or password")
            
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()

    return render(request, 'base_base-login.html', {'form' : form})       