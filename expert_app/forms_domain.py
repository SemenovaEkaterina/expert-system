import json
import time
from django import forms
from django.forms import ModelChoiceField

from expert_app.models import System, Object, ObjectAttributeValue, Attribute, Parameter, Question


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
    image = forms.FileField(
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
            if not image:
                system.image.delete(save=True)
            else:
                system.image.save('%s_%s' % (slug, image.name), image, save=True)

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
    image = forms.FileField(
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
        if not image:
            obj.image.delete(save=True)
        else:
            obj.image.save('%s_%s' % (time.time(), image.name), image, save=True)

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
    image = forms.FileField(
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
        type = data.get('type')

        if self.question:
            question = self.question
        else:
            question = Question()
            question.system = self.system

        question.name = name
        question.parameter = parameter
        question.type = type
        if not image:
            question.image.delete(save=True)
        else:
            question.image.save('%s_%s' % (time.time(), image.name), image, save=True)

        question.save()

        return question
