import json

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

from expert_app.domain.common import EQ, NQ, LT, LQ, GT, GQ, PARAMETER_TO_ATTRIBUTE, PARAMETER_TO_PARAMETER
from expert_app.models import SignupForm, LoginForm, System, SystemForm, Attribute, AttributeAllowedValue, ObjectForm, \
    Object, Parameter, ParameterAllowedValue, QuestionForm, Question, Answer, AnswerForm

from expert_app.domain.Session import Session as SessionDomain
from expert_app.domain.Session import get_session as get_session_domain
from expert_app.domain.SessionManager import *
from expert_app.domain.System import get_system as get_system_domain
from expert_app.domain.enableManagers import enableManagers


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
        if page not in ['mine', ]:
            page = 'mine'

        lst = []

        if page == 'mine':
            lst = System.objects.get_by_user(request.user)

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
                'title': 'Вопросы и ответы',
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

        if not is_mine:
            raise Http404

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

        if request.method == 'POST':
            return obj.post(request, data)
        elif request.method == 'GET':
            return obj.get(request, data)

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
        system = data['system']
        attrs = system.attribute_set.prefetch_related('attributeallowedvalue_set').all()
        data['attrs'] = attrs

        return render(request, 'office/systems/single/attrs.html', data)

    def post(self, request, data):
        system = data['system']
        attrs = json.loads(request.POST.get('attrs'))

        i = 0
        for attr in attrs:
            i = i + 1
            attr_id = int(attr['id']) if attr['id'] is not None else None

            if attr_id is None:
                if attr['removed']:
                    continue

                a = Attribute()
                a.system = system
                a.name = attr['name']
                a.order = i
                a.save()
            else:
                a = Attribute.objects.get(pk=attr_id)
                if attr['removed']:
                    a.delete(keep_parents=True)
                    continue
                else:
                    a.system = system
                    a.name = attr['name']
                    a.order = i
                    a.save()

            j = 0
            for attrv in attr['vals']:
                j = j + 1
                attrv_id = int(attrv['id']) if attrv['id'] is not None else None
                if attrv_id is None:
                    if attrv['removed']:
                        continue

                    av = AttributeAllowedValue()
                    av.attribute = a
                    av.value = attrv['name']
                    av.order = j
                    av.save()
                else:
                    av = AttributeAllowedValue.objects.get(pk=attrv_id)
                    if attrv['removed']:
                        av.delete(keep_parents=True)
                        continue
                    else:
                        av.attribute = a
                        av.value = attrv['name']
                        av.order = j
                        av.save()

        return HttpResponse(
            content=json.dumps({
                'result': True,
            })
        )


class OfficeSystemObjects(OfficeSystemBase):
    def handle(self, request, data):
        system = data['system']

        object_id = request.GET.get('object_id', None)
        if object_id is not None:
            if request.method == 'POST':
                if request.GET.get('action', None) == 'delete':
                    obj = get_object_or_404(Object, pk=object_id)
                    obj.delete()
                    return HttpResponse()
                form = ObjectForm(request.POST, request.FILES)
            elif object_id == 'new':
                form = ObjectForm()
            else:
                obj = get_object_or_404(Object, pk=object_id)
                form = ObjectForm(initial=model_to_dict(obj))

            object_attrs = []
            if object_id != 'new':
                obj = get_object_or_404(Object, pk=object_id)
                form.set_object(obj)
                object_attrs = list(obj.objectattributevalue_set.all())

            form.set_system(system)
            data['form'] = form

            attrs = system.attribute_set.prefetch_related('attributeallowedvalue_set').all()

            attrs_data = []
            for attr in attrs:
                active = None
                for oav in object_attrs:
                    if oav.attribute_id == attr.id:
                        active = oav.attribute_value_id
                        break

                allowed = [{'val': val, 'active': val.id == active} for val in attr.attributeallowedvalue_set.all()]
                attrs_data.append({
                    'attr': attr,
                    'allowed_vals': allowed,
                })

            data['attrs'] = attrs_data

            print(attrs_data)

            if request.method == 'POST':
                if form.is_valid():
                    object = form.save()
                    return HttpResponseRedirect(
                        reverse('office_system', kwargs={'sid': system.id, 'section': 'objects'}))

            return render(request, 'office/systems/single/objects_form.html', data)

        else:
            objects = system.object_set.all()
            data['objects'] = objects
            return render(request, 'office/systems/single/objects.html', data)


class OfficeSystemParams(OfficeSystemBase):
    def handle(self, request, data):
        system = data['system']
        params = system.parameter_set.prefetch_related('parameterallowedvalue_set').all()
        data['params'] = params

        return render(request, 'office/systems/single/params.html', data)

    def post(self, request, data):
        system = data['system']
        params = json.loads(request.POST.get('params'))

        i = 0
        for param in params:
            i = i + 1
            param_id = int(param['id']) if param['id'] is not None else None

            if param_id is None:
                if param['removed']:
                    continue

                p = Parameter()
                p.system = system
                p.name = param['name']
                p.type = param['type']
                p.order = i
                p.save()
            else:
                p = Parameter.objects.get(pk=param_id)
                if param['removed']:
                    p.delete(keep_parents=True)
                    continue
                else:
                    p.system = system
                    p.name = param['name']
                    p.type = param['type']
                    p.order = i
                    p.save()

            j = 0
            for paramv in param['vals']:
                j = j + 1
                paramv_id = int(paramv['id']) if paramv['id'] is not None else None
                if paramv_id is None:
                    if paramv['removed']:
                        continue

                    pv = ParameterAllowedValue()
                    pv.parameter = p
                    pv.value = paramv['name']
                    pv.order = j
                    pv.save()
                else:
                    pv = ParameterAllowedValue.objects.get(pk=paramv_id)
                    if paramv['removed']:
                        pv.delete(keep_parents=True)
                        continue
                    else:
                        pv.parameter = p
                        pv.value = paramv['name']
                        pv.order = j
                        pv.save()

        return HttpResponse(
            content=json.dumps({
                'result': True,
            })
        )


class OfficeSystemQuestions(OfficeSystemBase):
    def handle(self, request, data):
        system = data['system']

        question_id = request.GET.get('question_id', None)
        answer_id = request.GET.get('answer_id', None)
        action = request.GET.get('action', 'questions')

        question = None
        if question_id is not None and question_id != 'new':
            question = get_object_or_404(Question, pk=question_id)
            data['question'] = question

        if action == 'question':
            kwargs = {'params': system.parameter_set}

            if question is not None:
                kwargs['initial'] = model_to_dict(question)

            if request.method == 'POST':
                form = QuestionForm(request.POST, request.FILES, **kwargs)
                form.set_system(system)
                form.set_question(question)

                if form.is_valid():
                    question = form.save()
                    return HttpResponseRedirect(
                        reverse('office_system', kwargs={'sid': system.id, 'section': 'questions'}))
            else:
                form = QuestionForm(**kwargs)
                form.set_system(system)
                form.set_question(question)

            data['form'] = form

            return render(request, 'office/systems/single/questions_form.html', data)
        elif action == 'delete':
            if question is None:
                raise Http404

            if answer_id is not None:
                answer = get_object_or_404(Answer, pk=answer_id)
                answer.delete()
                return HttpResponse()
            else:
                question.delete()
                return HttpResponse()
        elif action == 'answers':
            if question is None:
                raise Http404

            answers = question.answer_set.all()
            data['answers'] = answers

            return render(request, 'office/systems/single/answers.html', data)
        elif action == 'answer':
            if question is None:
                raise Http404

            kwargs = {'question': question}

            answer = None
            if answer_id is not None and answer_id != 'new':
                answer = get_object_or_404(Answer, pk=answer_id)
                kwargs['initial'] = model_to_dict(answer)

            if request.method == 'POST':
                form = AnswerForm(request.POST, request.FILES, **kwargs)
                form.set_answer(answer)

                if form.is_valid():
                    answer = form.save()
                    return HttpResponseRedirect(
                        reverse('office_system', kwargs={'sid': system.id, 'section': 'questions'}) + (
                            '?question_id=%s&action=%s' % (question.id, 'answers')))
            else:
                form = AnswerForm(**kwargs)
                form.set_answer(answer)

            data['form'] = form

            return render(request, 'office/systems/single/answers_form.html', data)

        else:
            questions = system.question_set.all()
            data['questions'] = questions
            return render(request, 'office/systems/single/questions.html', data)


class OfficeSystemRules(OfficeSystemBase):
    def handle(self, request, data):
        system = data['system']

        parameters = system.parameter_set.all()
        attributes = system.attribute_set.all()

        info_parameters = {}
        for parameter in parameters:
            p = model_to_dict(parameter)
            p['values'] = list(map(lambda x: model_to_dict(x), parameter.parameterallowedvalue_set.all()))
            info_parameters.update({
                parameter.id: p,
            })

        info_attributes = {}
        for attribute in attributes:
            a = model_to_dict(attribute)
            a['values'] = list(map(lambda x: model_to_dict(x), attribute.attributeallowedvalue_set.all()))
            info_attributes.update({
                attribute.id: a,
            })

        info = {
            'parameters': info_parameters,
            'attributes': info_attributes,
            'operations': {
                EQ: '=',
                NQ: '!=',
                LT: '<',
                LQ: '<=',
                GT: '>',
                GQ: '>=',
            },
            'attribute': PARAMETER_TO_ATTRIBUTE,
            'parameter': PARAMETER_TO_PARAMETER,
            'or': 0,
            'and': 1,
        }

        data['info'] = json.dumps(info)

        info_rules = [
            {
                'id': 1,
                'data': {
                    'type': PARAMETER_TO_PARAMETER,
                    'condition': [
                        {
                            'param_id': 4,
                            'param_value_id': 9,
                            'operation': LT,
                            'param_value_any': None,
                        },
                        {
                            'param_id': 2,
                            'param_value_id': 2,
                            'operation': EQ,
                            'param_value_any': None,
                        }
                    ],
                    'operation': 1,
                    'second_id': 5,
                    'second_value_id': None,
                    'second_value_any': 678,
                }
            }
        ]

        data['rules'] = json.dumps(info_rules)

        return render(request, 'office/systems/single/rules.html', data)


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


class ScienceSystem(View):
    def get(self, request, slug):
        system = get_object_or_404(System, slug=slug)

        return render(request, 'science/intro.html', {
            'title': system.name,
            'description': system.description,
            'slug': slug,
            'system': system,
            'hasSession': 'exp_session_id_' + slug not in request.session
        })


class ScienceSession(View):
    def get(self, request, slug):
        enableManagers()

        system = get_object_or_404(System, slug=slug)

        #request.session.clear()

        if 'exp_session_id_' + slug not in request.session:
            system_domain = get_system_domain(system.id)
            session_domain = SessionDomain(system_domain, request.user)
            request.session['exp_session_id_' + slug] = session_domain.id
        else:
            session_domain = get_session_domain(request.session['exp_session_id_' + slug])

        next_question = session_domain.next_question()

        stat_items = session_domain.get_stat()

        if not next_question:
            request.session.clear()
            return render(request, 'science/session.html', {
                'title': system.name,
                'description': system.description,
                'slug': slug,
                'system': system,
                'finished': True,
                'stat_items': stat_items
            })

        question = {'text': next_question['text'], 'type': next_question['type']}
        answers = next_question['answers']

        return render(request, 'science/session.html', {
            'title': system.name,
            'description': system.description,
            'slug': slug,
            'system': system,
            'answers': answers,
            'question': question,
            'stat_items': stat_items
        })

    def post(self, request, slug):
        result = request.POST['answer']

        if 'exp_session_id_' + slug in request.session:
            session_domain = get_session_domain(request.session['exp_session_id_' + slug])
            session_domain.answer(result)

        return HttpResponseRedirect(reverse('science_session', kwargs={'slug': slug}))


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
