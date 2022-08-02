from django.shortcuts import render
from .form import UserProfileInfoForm,UserForm

from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout



# Create your views here.

def index(request):
    return render(request, 'basic_app/index.html')

@login_required
def special(request):
    return HttpResponse('you are logged in, NICE!')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered=False

    if request.method=='POST':
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # grab user form data
            user=user_form.save()
            # user.set_password(user.password)           #  set_password() is use fo hashing the passowrd
            user.save()

            # grabe profile data
            profile=profile_form.save(commit=False)
            # check if profil pic is ther or not
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']

            profile.save()
            # After all conformation put registration = true
            registered=True
        else:
            # if any of them is invalid the we give erros
            print(user_form.errors,profile_form.errors)

    else:
        user_form=UserForm()
        profile_form=UserProfileInfoForm()

    return render(request, 'basic_app/registration.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered} )

def user_login(request):

    if request.method == 'POST':

        # get data from form
        username = request.POST.get('username')
        password=request.POST.get('password')

        #authenticate username and password
        user= authenticate(username=username, password=password)

        if user:
            # check if user is active or not
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print('someone try to login and faild!!!!')
            print("Username: {} and Password: {}".format(username,password))
            return HttpResponse("invalid login details supplied")

    else:
        return render(request, 'basic_app/login.html',{})
