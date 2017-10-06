from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator

from django.views import View

from expert_app.models import SignupForm, LoginForm


def need_login(func):
    return login_required(func, redirect_field_name='continue')


class Home(View):
    def get(self, request):
        return render(request, 'front/home.html')


class Logout(View):
    @method_decorator(need_login)
    def get(self, request):
        redirect = request.GET.get('continue', '/')
        auth.logout(request)
        return HttpResponseRedirect(redirect)


class Login(View):
    def get(self, request):
        redirect = request.GET.get('continue', '/')
        if request.user.is_authenticated():
            return HttpResponseRedirect(redirect)

        form = LoginForm()

        return render(request, 'front/login.html', {
            'form': form,
        })

    def post(self, request):
        redirect = request.GET.get('continue', '/')
        if request.user.is_authenticated():
            return HttpResponseRedirect(redirect)

        form = LoginForm(request.POST)

        if form.is_valid():
            auth.login(request, form.cleaned_data['user'])
            return HttpResponseRedirect(redirect)

        return render(request, 'front/login.html', {
            'form': form,
        })


class Signup(View):
    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')

        form = SignupForm()

        return render(request, 'front/signup.html', {
            'form': form,
        })

    def post(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')

        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return HttpResponseRedirect('/')

        return render(request, 'front/signup.html', {
            'form': form,
        })


class OfficeDashboard(View):
    @method_decorator(need_login)
    def get(self, request):
        return redirect(reverse('office_systems'))


class OfficeSystems(View):
    @method_decorator(need_login)
    def get(self, request, page='mine'):
        if page not in ['mine', 'all']:
            page = 'mine'

        return render(request, 'office/systems.html', {
            'page': page,
        })
