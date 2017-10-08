from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

from django.views import View

from expert_app.models import SignupForm, LoginForm, System, SystemForm


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
            lst = System.objects.all()

        return render(request, 'office/systems/list/page.html', {
            'page': page,
            'systems': lst
        })


class OfficeSystemSingle(View):
    def get_sections(self):
        return [
            {
                'title': 'О системе',
                'key': 'about',
                'color': 'danger',
                'class': OfficeSystemAbout,
            },
            {
                'title': 'Атрибуты объектов',
                'key': 'attrs',
                'color': 'warning',
                'class': OfficeSystemAttrs,
            },
            {
                'title': 'Объекты',
                'key': 'objects',
                'color': 'warning',
                'class': OfficeSystemObjects,
            },
            {
                'title': 'Параметры',
                'key': 'params',
                'color': 'success',
                'class': OfficeSystemParams,
            },
            {
                'title': 'Вопросы',
                'key': 'questions',
                'color': 'success',
                'class': OfficeSystemQuestions,
            },
            {
                'title': 'Правила',
                'key': 'rules',
                'color': 'success',
                'class': OfficeSystemRules,
            },
        ]

    def detect_section(self, section):
        sections = self.get_sections()
        section_keys = [section['key'] for section in sections]

        if section not in section_keys:
            return (section_keys or [None])[0]

        return section

    def get_section_data(self, section):
        for s in self.get_sections():
            if s['key'] == section:
                return s

        return None

    def handle(self, request, sid, section='about'):
        system = get_object_or_404(System, pk=sid)
        is_mine = system.is_by_user(request.user)

        sections = self.get_sections()
        section = self.detect_section(section)

        if section is None:
            raise Http404

        data = {
            'section_active': section,
            'sections': sections,
            'title': system.name,
            'system': system,
            'is_mine': is_mine,
        }

        section_data = self.get_section_data(section)
        klass = section_data['class']

        obj = klass()
        return obj.handle(request, data)

    def get(self, *args, **kwargs):
        return self.handle(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.handle(*args, **kwargs)


class OfficeSystemBase(View):
    def handle(self, request, data):
        pass

    def get(self, request, data):
        return self.handle(request, data)

    def post(self, request, data):
        return self.handle(request, data)


class OfficeSystemAbout(OfficeSystemBase):
    def handle(self, request, data):
        if request.method == 'POST':
            form = SystemForm(request.POST, request.FILES)
        else:
            form = SystemForm(initial=model_to_dict(data['system']))

        form.set_system(data['system'])
        data.update({
            'form': form,
        })

        if request.method == 'POST':
            if form.is_valid():
                system = form.save(request.user)
                return HttpResponseRedirect(
                    reverse('office_system', kwargs={'sid': system.id, 'section': 'about'}))

        return render(request, 'office/systems/single/about.html', data)


class OfficeSystemAttrs(OfficeSystemBase):
    def handle(self, request, data):
        return render(request, 'office/systems/single/about.html', data)


class OfficeSystemObjects(OfficeSystemBase):
    def handle(self, request, data):
        return render(request, 'office/systems/single/about.html', data)


class OfficeSystemParams(OfficeSystemBase):
    def handle(self, request, data):
        return render(request, 'office/systems/single/about.html', data)


class OfficeSystemQuestions(OfficeSystemBase):
    def handle(self, request, data):
        return render(request, 'office/systems/single/about.html', data)


class OfficeSystemRules(OfficeSystemBase):
    def handle(self, request, data):
        return render(request, 'office/systems/single/about.html', data)


class OfficeSystemAdd(View):
    def handle(self, request):
        sections = [
            {
                'title': 'О системе',
                'key': 'about',
                'color': 'danger',
            },
        ]

        section = 'about'

        form = SystemForm()

        if request.method == 'POST':
            form = SystemForm(request.POST, request.FILES)
            if form.is_valid():
                system = form.save(request.user)

                return HttpResponseRedirect(
                    reverse('office_system', kwargs={'sid': system.id, 'section': 'about'}))

        return render(request, 'office/systems/single/about.html', {
            'section_active': section,
            'sections': sections,
            'title': 'Создание системы',
            'system': None,
            'is_mine': False,
            'form': form,
        })

    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)


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
