from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout

from .models import Profile, Meep
from .forms import MeepForm, SignUpForm, UpdateForm, ProfilePicForm


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        form = MeepForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                meep = form.save(commit=False)
                meep.user = request.user
                meep.save()
                messages.success(request, 'Your meep has been posted')
                return redirect('home')

        meeps = Meep.objects.all().order_by('-created_at')
        return render(request, 'home.html', {'meeps': meeps, 'form': form})
    else:
        meeps = Meep.objects.all().order_by('-created_at')
        return render(request, 'home.html', {'meeps': meeps})
def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {'profiles': profiles})
    else:
        messages.success(request, 'You must be logged in to access this page')
        return redirect('home')


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        zaps = Meep.objects.filter(user_id=pk).order_by('-created_at')

        if request.method == 'POST':
            # get current user
            current_user_profile = request.user.profile
            # get form data
            action = request.POST['follow']
            # decide to follow or unfollow
            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            elif action == 'follow':
                current_user_profile.follows.add(profile)
        return render(request, 'profile.html', {'profile': profile, 'meeps': zaps})
    else:
        messages.success(request, 'You must be logged in to access this page')
        return redirect('home')


def followers(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'followers.html', {'profiles': profiles})
        else:
            messages.success(request, 'That\'s not your profile page.')
            return redirect('home')
    else:
        messages.success(request, 'You must be logged in to access this page')
        return redirect('home')


def follows(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'follows.html', {'profiles': profiles})
        else:
            messages.success(request, 'That\'s not your profile page.')
            return redirect('home')
    else:
        messages.success(request, 'You must be logged in to access this page')
        return redirect('home')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.success(request, 'Login failed...')
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, 'Bye bye!')
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #first_name = form.cleaned_data['first_name']
            #last_name = form.cleaned_data['last_name']
            #email = form.cleaned_data['email']
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Welcome! You\'re now registered!')
            return redirect('home')

    return render(request, 'register.html', {'form':form})


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)
        user_form = UpdateForm(request.POST or None, request.FILES or None, instance=current_user)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your info has been updated')
            return redirect('home')
        return render(request, 'update_user.html', {'user_form':user_form, 'profile_form':profile_form})
    else:
        messages.success(request, 'you have to be logged in to access this page')
        return redirect('home')


def meep_like(request, pk):
    if request.user.is_authenticated:
        meep = get_object_or_404(Meep, id=pk)
        if meep.likes.filter(id=request.user.id):
            meep.likes.remove(request.user)
        else:
            meep.likes.add(request.user)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, 'you have to be logged in to access this page')
        return redirect('home')


def meep_show(request, pk):
    meep = get_object_or_404(Meep, id=pk)
    if meep:
        return render(request, 'meep_show.html', {'meep':meep})
    else:
        messages.success(request, 'This meep doesn\'t exist')
        return redirect('home')


def unfollow(request, pk):
    if request.user.is_authenticated:
        #get the profile to unfollow
        unfollow_profile = Profile.objects.get(user_id=pk)
        request.user.profile.follows.remove(unfollow_profile)
        request.user.profile.save()
        messages.success(request, f'User unfollowed {unfollow_profile.user.username}')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, 'You must be logged in to do this.')
        return redirect('home')


def follow(request, pk):
    if request.user.is_authenticated:
        #get the profile to follow
        follow_profile = Profile.objects.get(user_id=pk)
        request.user.profile.follows.add(follow_profile)
        request.user.profile.save()
        messages.success(request, f'User unfollowed {follow_profile.user.username}')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, 'You must be logged in to do this.')
        return redirect('home')


def meep_delete(request, pk):
    if request.user.is_authenticated:
        meep = get_object_or_404(Meep, id=pk)
        if meep.user.id == request.user.id:
            meep.delete()
            messages.success(request, 'Meep successfully deleted')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.success(request, 'This meep isn\'t yours!')
            return redirect('home')
    else:
        messages.success(request, 'You need to be logged in to do this')
        return redirect(request.META.get('HTTP_REFERER'))


def meep_edit(request, pk):
    if request.user.is_authenticated:
        meep = get_object_or_404(Meep, id=pk)

        if meep.user.id == request.user.id:
            form = MeepForm(request.POST or None, instance=meep)

            if request.method == 'POST':
                if form.is_valid():
                    meep = form.save(commit=False)
                    meep.user = request.user
                    meep.save()
                    messages.success(request, 'Your meep has been edited')
                    return redirect('home')
            return render(request, 'meep_edit.html', {'form':form,'meep':meep})
        else:
            messages.success(request, 'This meep isn\'t yours!')
            return redirect('home')
    else:
        messages.success(request, 'You need to be logged in to do this')
        return redirect('home')


def search(request):
    if request.method == 'POST':
        search_term = request.POST['search']
        searched_term = Meep.objects.filter(body__contains=search_term)
        return render(request, 'search.html', {'search': search_term, 'searched_term':searched_term})
    else:
        return render(request, 'search.html', {})
