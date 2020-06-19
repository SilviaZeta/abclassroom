from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from . import models
from . import forms

def signup_view(request):

    if request.method == 'POST':
        form = forms.SignupUserForm(request.POST)
            
        if form.is_valid():
            user = form.save()
            user.refresh_from_db() #solve synch issues when using signal

            user.profile.full_name = form.cleaned_data.get('full_name')
            user.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return redirect('dashboard', username=username)

    else:
        form = forms.SignupUserForm()
    
    context = {"form": form }
    return render(request, 'signup.html', context)


def validate_username_view(request):
    username = request.GET.get('username', None)
    data = {
            'is_empty': len(username) == 0,
            'is_taken': User.objects.filter(username__iexact=username).exists(),
            }
    if data['is_empty']:
        data['errormsg'] = 'This field is required.'
    if data['is_taken']:
        data['errormsg'] = 'A user with this username already exists.'
    return JsonResponse(data)

def email_is_valid(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def validate_email_view(request):
    email = request.GET.get('email', None)

    data = {
            'is_empty' : len(email) == 0,
            'is_invalid': not email_is_valid(email),
            'is_taken': User.objects.filter(email__iexact=email).exists(),
            }

    if data['is_empty']:
        data['errormsg'] = 'This field is required.'
    elif data['is_invalid']:   
        data['errormsg'] = 'Email is invalid.'  
    elif data['is_taken']:
        data['errormsg'] = 'A user with this email already exists.'

    return JsonResponse(data)

def password_is_valid(password):
    if len(password) < 8:
        return False
    elif not any(i.isdigit() for i in password):
        return False
    elif not any(i.isalpha() for i in password):
        return False
    else:
        return True

def validate_password1_view(request):
    password1 = request.GET.get('password1', None)
    data = {
            'is_empty': len(password1) == 0,
            'is_invalid': not password_is_valid(password1),
            }
    if data['is_empty']:
        data['errormsg'] = 'This field is required.'
    elif data['is_invalid']:
        data['errormsg'] = "Invalid password. You must use at least 8 \
                            characters, one digit and one letter."

    return JsonResponse(data) 

def validate_password2_view(request):
    password1 = request.GET.get('password1', None)
    password2 = request.GET.get('password2', None)

    data = {
            'is_invalid': not password_is_valid(password2),
            'is_unmatched': password1 != password2,
            }
    if data['is_invalid']:
        data['errormsg'] = "Invalid password. You must use at least 8 \
                            characters, one digit and one letter."
    elif data['is_unmatched']:
        data['errormsg'] = "The two password don't match."
        
    return JsonResponse(data)     

def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard', request.user.username)
    else:
        logout(request) #otherwise login only at second attempt
    
        
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
    
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            if username and password:
                user = authenticate(username=username, password=password)
                #form = forms.LoginForm() #refresh entries
                
                if user is None:
                    messages.error(request, "Please enter a correct username and password. \
                                   Note that both fields are case-sensitive.")
                elif not user.is_active:
                    messages.error(request, "This account is inactive.")
                else:
                    login(request, user) 
                    return redirect('dashboard', username)
    else:
        form = forms.LoginForm()
    
    context = {"form": form}
    return render(request, 'login.html', context)


@login_required
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')


@login_required
def update_profile_view(request, username):

    profile = request.user.profile

    if request.method == 'POST':
        form = forms.UpdateProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('dashboard', username=request.user.username)
    else:
        form = forms.UpdateProfileForm(instance=profile)

    context = {"form": form}
    return render(request, 'profile_settings.html', context)

@login_required
def update_user_view(request, username):

    if request.method == 'POST':
        form = forms.CustomUserChangeForm(request.POST, instance=request.user)
    else:
        form = forms.CustomUserChangeForm(instance=request.user)

    context = {"form": form}
    return render(request, 'account_settings.html', context)


@login_required
def delete_user_view(request, username):

    if request.method == 'POST':
        request.user.delete()
        return redirect('delete_account_confirm', username=username)

    return render(request, 'delete_account.html')


def delete_account_confirm_view(request, username):
   return render(request, 'delete_account_confirm.html')

@login_required
def admin_change_password(request, username):

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()

            raw_password = form.cleaned_data.get('new_password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return redirect('dashboard', username)
    else:
        form = PasswordChangeForm(request.user)

    context = {'form': form}
    return render(request, 'change_password.html', context)    
