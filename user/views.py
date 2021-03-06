from django.shortcuts import render, redirect

# importing View
from django.views.generic import View, TemplateView, ListView, CreateView

from django.contrib.auth.models import User

#modules of authentication
from django.contrib.auth import authenticate, login, logout

#flash messages
from django.contrib import messages

from django.urls import reverse_lazy

#forms
from user.forms import UserForm, UserProfileForm

def register(request) :
    user_form = UserForm()
    user_profile_form = UserProfileForm()

    if request.method == 'POST' :
        user_form = UserForm(request.POST)
        user_profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save()
            user_profile_form = user_profile_form.save(commit = False)
            user_profile_form.user = user
            user_profile_form.save()

            #login
            login(request, user)

            return redirect('user_app:user')

    return render(request, 'register.html', {
        'user_form': user_form, 
        'user_profile_form':user_profile_form
    })


class LoginView(View):
    template_name = 'log_in.html'

    def get(self, request, *args, **kwargs) :
        return render(request, self.template_name)

    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST' :

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username = username, password = password)

            if user :
                login(request, user)
                return redirect('user_app:user')

            messages.warning(request, 'No te has podido identificar correctamente')
            return redirect('user_app:log_in')


def user_logout(request):
    logout(request)
    return redirect('user_app:user')


def user(request) :

    return render(request, 'user.html', {
        'title': 'Bienvendido a usuarios'
    })




