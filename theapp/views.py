from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.db.models import Sum, Count
from . forms import *
from . models import *
import random
# Create your views here.

def checkBookLibrary(profile, book):
    if book in profile.books.all():
        return True
    else:
        return False
    
def checkStatus(book):
    if book.status == "ON-GOING":
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
    context = {
        'user' : user,
        'user_book' : user_book
    }
    return render(request, 'base_user-library.html', context)

@login_required
def update(request, id):
    user = request.user
    p = user.profile
    book = Series.objects.get(pk=id)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
        messages.success(request, "Note added")
        return redirect("theapp:update", id=id)
    else:
        form = NoteForm()

    context = {
        'user' : user,
        'form' : form,  
    }
    return render(request, "base_book-update.html", context)

def view_book(request, id):
    user = request.user
    profile = user.profile
    book = Series.objects.get(pk=id)
    volume = book.volume_set.all()
    genres = book.genre
    genres = genres.split(",")
    if request.method == 'POST':
        if checkBookLibrary(profile, book):
            profile.books.remove(book)
            messages.success(request, "Removed from library")
        else:
            profile.books.add(book)
            messages.success(request, "Added to library")
        return redirect("theapp:view_book", id=id)
    else:
        seriesStatus = checkStatus(book)
        status =  checkBookLibrary(profile, book)
        return render(request, 'base_book-view.html', {'book' : book, 'volume' : volume, 'genres' : genres, 'status' : status, 'seriesStatus' : seriesStatus})

@login_required    
def view_book_update(request, id):
    user = request.user
    profile = user.profile
    book = Series.objects.get(pk=id)
    volume = book.volume_set.all()
    genres = book.genre
    genres = genres.split(",")
    checkReview = Review.objects.filter(profile=profile, series=book).exists()

    if request.method == 'POST':
        if 'note-form' in request.POST:
            form = NoteForm(request.POST)
            if form.is_valid():
                note = form.cleaned_data['note']
                idd = request.POST.get('pk')
                v = Volume.objects.get(uniq=idd)
                newNote = Note(profile=profile, volume=v, note=note)
                newNote.save()

                messages.success(request, "Note added")
            return redirect("theapp:view_book_update", id=id)

        if 'lib-form' in request.POST:
            if checkBookLibrary(profile, book):
                profile.books.remove(book)
                messages.success(request, "Removed from library")
            else:
                profile.books.add(book)
                messages.success(request, "Added to library")
            return redirect("theapp:view_book_update", id=id)
        
        if 'rev-form' in request.POST:
            revForm = ReviewForm(request.POST)
            if revForm.is_valid():
                review = revForm.cleaned_data['review']
                score = revForm.cleaned_data['score']
                series = request.POST.get('series')
                pr = request.POST.get('profile')
                
                p = Profile.objects.get(pk=pr)
                s = Series.objects.get(pk=series)
                if checkReview:
                    rev = Review.objects.get(profile=p, series=s)
                    rev.review = review
                    rev.score = score
                    rev.save()
                else:
                    newRev = Review(profile=p, series=s, review=review, score=score)
                    newRev.save()

                aggregates = book.review_set.aggregate(
                    total_score = Sum('score'),
                    review_count = Count('id')
                )
                if aggregates['review_count'] > 0:
                    book.score = aggregates['total_score'] / aggregates['review_count']
                else:
                    book.score = None
                book.save()

                messages.success(request, "Review added")
            return redirect("theapp:view_book_update", id=id)
    else:
        form = NoteForm()
        revForm = ReviewForm()
        seriesStatus = checkStatus(book)
        status =  checkBookLibrary(profile, book)
        context = {
            'book' : book,
            'volume' : volume,
            'genres' : genres,
            'status' : status,
            'seriesStatus' : seriesStatus,
            'form' : form,
            'revForm' : revForm,
            'profile' : profile,
            'checkReview' : checkReview,
            # ''
        }
        return render(request, 'base_book-update.html', context)

def login_request(request):
    if request.method == 'POST':
        if 'login' in request.POST:
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
        if 'register' in request.POST:
            registerForm = Register(request.POST)
            profileForm = SetProfile(request.POST)
            if registerForm.is_valid() and profileForm.is_valid():
                username = registerForm.cleaned_data['username']
                password = registerForm.cleaned_data['password1']
                preference = profileForm.cleaned_data['preference']
                blacklist = profileForm.cleaned_data['blacklist']
                registerForm.save()

                user = authenticate(request, username=username, password=password)
                u = User.objects.get(username=username)
                p = Profile(username=u, preference=preference, blacklist=blacklist)
                p.save()
                if user is not None:
                    login(request, user)
                    return redirect('theapp:index')
                
    else:
        form = AuthenticationForm()
        registerForm = Register()
        profileForm = SetProfile()

    return render(request, 'base_base-login.html', {'form' : form, 'registerForm' : registerForm, 'profileForm' : profileForm})

def logout_view(request):
    logout(request)