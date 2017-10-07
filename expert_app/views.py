from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

from django.views import View

from expert_app.models import SignupForm, LoginForm, System


def need_login(func):
    return login_required(func, redirect_field_name='continue')


class Home(View):
    def get(self, request):
        systems = System.objects.all_for_front()
        return render(request, 'front/home.html', {
            'systems': systems,
        })


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

        lst = []

        if page == 'mine':
            lst = System.objects.get_by_user(request.user)
        elif page == 'all':
            lst = System.objects.all(True)

        return render(request, 'office/systems/list/page.html', {
            'page': page,
            'systems': lst
        })


class OfficeSystemSingle(View):
    def get(self, request, sid, section='about'):
        system = get_object_or_404(System, pk=sid)
        is_mine = system.is_by_user(request.user)

        sections = [
            {
                'title': 'О системе',
                'key': 'about',
                'color': 'danger',
            },
            {
                'title': 'Атрибуты объектов',
                'key': 'attrs',
                'color': 'warning',
            },
            {
                'title': 'Объекты',
                'key': 'objects',
                'color': 'warning',
            },
            {
                'title': 'Параметры',
                'key': 'params',
                'color': 'success',
            },
            {
                'title': 'Вопросы',
                'key': 'questions',
                'color': 'success',
            },
            {
                'title': 'Правила',
                'key': 'rules',
                'color': 'success',
            },
        ]

        section_keys = [section['key'] for section in sections]

        if section not in section_keys:
            if section is None or len(section) == 0:
                section = 'about'
            else:
                raise Http404

        return render(request, 'office/systems/single/about.html', {
            'section_active': section,
            'sections': sections,
            'title': system.name,
            'system': system,
            'is_mine': is_mine,
        })


class OfficeSystemAdd(View):
    def get(self, request):
        sections = [
            {
                'title': 'О системе',
                'key': 'about',
                'color': 'danger',
            },
        ]

        section = 'about'

        return render(request, 'office/systems/single/about.html', {
            'section_active': section,
            'sections': sections,
            'title': 'Создание системы',
            'system': None,
            'is_mine': False,
        })


def handler404(request):
    response = render_to_response('error.html', {
        'request': request,
        'error_code': 404,
        'error_title': 'Страница не найдена!',
    })
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('error.html', {
        'request': request,
        'error_code': 500,
        'error_title': 'Ошибочка вышла',
    })
    response.status_code = 500
    return response
