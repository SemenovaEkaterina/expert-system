import json
import time

import os
from django import forms
from django.forms import ModelChoiceField

from expert_app.models import System, Object, ObjectAttributeValue, Attribute, Parameter, Question, Answer, \
    ParameterAllowedValue


class SystemForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Супер-система', }
        ),
        max_length=100,
        label=u'Название'
    )
    slug = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'super-system', }
        ),
        max_length=30,
        label=u'slug (для URL)'
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': '3', }
        ),
        label=u'Описание'
    )
    author = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Александр Иванник, ИУ5-73', }
        ),
        max_length=100,
        label=u'Авторы'
    )
    image = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={'class': 'form-control', }),
        required=False, label=u'Изображение'
    )
    public = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-control', }
        ),
        required=False,
        label=u'Доступна всем'
    )

    system = None

    def set_system(self, system):
        self.system = system

    def clean_slug(self):
        slug = self.cleaned_data.get('slug', '')
        slugged_system = System.objects.get_by_slug(slug)

        if not slugged_system:
            return slug

        slugged_system = slugged_system.all()[:1].get()

        if self.system is None or slugged_system.id != self.system.id:
            raise forms.ValidationError(u'Такой slug уже занят')

        return slug

    def save(self, user):
        data = self.cleaned_data

        name = data.get('name')
        description = data.get('description')
        author = data.get('author')
        slug = data.get('slug')
        image = data.get('image')
        public = data.get('public')

        if self.system:
            system = self.system
        else:
            system = System()
            system.user = user

        system.name = name
        system.description = description
        system.author = author
        system.slug = slug
        system.public = public

        if image is not None:
            if isinstance(image, bool) and not image:
                system.image.delete(save=True)
            else:
                name, extension = os.path.splitext(image.name)
                system.image = image

        system.save()

        return system


class ObjectForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Объект', }
        ),
        max_length=100,
        label=u'Название'
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': '3', }
        ),
        label=u'Описание'
    )
    image = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={'class': 'form-control', }),
        required=False, label=u'Изображение'
    )
    attrs = forms.CharField(
        widget=forms.HiddenInput()
    )

    system = None
    object = None

    def set_system(self, system):
        self.system = system

    def set_object(self, obj):
        self.object = obj

    def save(self):
        data = self.cleaned_data

        name = data.get('name')
        description = data.get('description')
        image = data.get('image')

        if self.object:
            obj = self.object
        else:
            obj = Object()
            obj.system = self.system

        obj.name = name
        obj.description = description

        if image is not None:
            if isinstance(image, bool) and not image:
                obj.image.delete(save=True)
            else:
                obj.image = image

        obj.save()

        attrs = json.loads(data.get('attrs', '[]'))

        for oav in obj.objectattributevalue_set.all():
            oav.delete()

        for attr in attrs:
            oav = ObjectAttributeValue()
            oav.object = obj
            oav.attribute = Attribute.objects.get(pk=attr['attr_id'])
            oav.attribute_value = oav.attribute.attributeallowedvalue_set.get(pk=attr['attr_value_id'])
            oav.save()

        return obj


class ParameterChoiceField(ModelChoiceField):
    def label_from_instance(self, parameter):
        return parameter.name


class QuestionForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Текст', }
        ),
        max_length=100,
        label=u'Текст вопроса'
    )
    image = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={'class': 'form-control', }),
        required=False, label=u'Изображение'
    )
    parameter = ParameterChoiceField(
        queryset=Parameter.objects.all(),
        empty_label=None,
        required=True,
        label=u'Параметр'
    )
    type = forms.ChoiceField(
        choices=Question.TYPES,
        label=u'Тип ответа'
    )

    def __init__(self, *args, **kwargs):
        qs = kwargs.pop('params')
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['parameter'].queryset = qs

    system = None
    question = None

    def set_system(self, system):
        self.system = system

    def set_question(self, question):
        self.question = question

    def save(self):
        data = self.cleaned_data

        name = data.get('name')
        image = data.get('image')
        parameter = data.get('parameter')
        tpe = data.get('type')

        if self.question:
            question = self.question
        else:
            question = Question()
            question.system = self.system

        question.name = name
        question.parameter = parameter
        question.type = tpe

        if image is not None:
            if isinstance(image, bool) and not image:
                question.image.delete(save=True)
            else:
                question.image = image

        question.save()

        return question


class ParameterValueChoiceField(ModelChoiceField):
    def label_from_instance(self, parameter_value):
        return parameter_value.value


class AnswerForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Текст', }
        ),
        max_length=50,
        label=u'Текст ответа'
    )
    image = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={'class': 'form-control', }),
        required=False, label=u'Изображение'
    )
    parameter_value = ParameterValueChoiceField(
        queryset=ParameterAllowedValue.objects.all(),
        empty_label=None,
        required=True,
        label=u'Значение параметра'
    )
    parameter_value_any = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Текст', }
        ),
        max_length=50,
        label=u'Значение параметра'
    )

    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question')
        super(AnswerForm, self).__init__(*args, **kwargs)

        if self.question.parameter.type == Parameter.TYPE_PREDEF:
            self.fields['parameter_value'].queryset = self.question.parameter.parameterallowedvalue_set.all()
            del self.fields['parameter_value_any']
        else:
            input_type = 'text'
            if self.question.parameter.type == Parameter.TYPE_INT:
                input_type = 'number'

            self.fields['parameter_value_any'].widget.input_type = type
            del self.fields['parameter_value']

    system = None
    question = None
    answer = None

    def set_answer(self, answer):
        self.answer = answer

    def save(self):
        data = self.cleaned_data

        name = data.get('name')
        image = data.get('image')
        parameter_value = data.get('parameter_value')
        parameter_value_any = data.get('parameter_value_any')

        if self.answer:
            answer = self.answer
        else:
            answer = Answer()
            answer.question = self.question

        answer.name = name
        answer.parameter_value = parameter_value
        answer.parameter_value_any = parameter_value_any

        if image is not None:
            if isinstance(image, bool) and not image:
                answer.image.delete(save=True)
            else:
                answer.image = image

        answer.save()

        return answer
