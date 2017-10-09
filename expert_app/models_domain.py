# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    order = models.IntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ['order']


class SystemQuerySet(models.QuerySet):
    def with_counters(self):
        return self.annotate(objects_count=Count('object', distinct=True),
                             questions_count=Count('question', distinct=True)
                             )

    def by_user(self, user):
        return self.filter(user=user)

    def by_slug(self, slug):
        return self.filter(slug=slug)

    def with_public(self, val=None):
        if val is None:
            return self

        return self.filter(public=val)

    def order_by_name(self):
        return self.order_by('name')

    def order_by_created_at(self):
        return self.order_by('-created_at')


class SystemManager(models.Manager):
    def get_queryset(self):
        res = SystemQuerySet(self.model, using=self._db)
        return res.with_counters()

    def get_by_user(self, user):
        q = self.get_queryset()
        return q.by_user(user)

    def get_by_slug(self, slug):
        q = self.get_queryset()
        return q.by_slug(slug)

    def all(self, public=None):
        q = self.get_queryset()
        return q.with_public(public)

    def all_for_front(self):
        q = self.get_queryset()
        return q.order_by_created_at().with_public(True)


class System(BaseModel):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User)  # пользователь-создатель
    author = models.CharField(max_length=100)  # как отображать автора
    description = models.TextField(default="")
    image = models.ImageField(upload_to='system_images/', blank=True, null=True)
    public = models.BooleanField(default=False)
    slug = models.CharField(max_length=30, default='', unique=True)

    objects = SystemManager()

    def is_by_user(self, user):
        if isinstance(user, int):
            return self.user.id == user

        if isinstance(user, User):
            return self.user.id == user.id


class Attribute(BaseModel):
    name = models.CharField(max_length=50)
    system = models.ForeignKey(System)


class AttributeAllowedValue(BaseModel):
    value = models.CharField(max_length=50)
    attribute = models.ForeignKey(Attribute)


class Object(BaseModel):
    name = models.CharField(max_length=50)
    description = models.TextField(default="")
    image = models.ImageField(upload_to='object_images/', blank=True, null=True)
    system = models.ForeignKey(System)


class ObjectAttributeValue(BaseModel):
    object = models.ForeignKey(Object)
    attribute = models.ForeignKey(Attribute)
    attribute_value = models.ForeignKey(AttributeAllowedValue)


class Parameter(BaseModel):
    TYPE_PREDEF = 0
    TYPE_INT = 1
    TYPE_STRING = 2
    TYPES = [
        (TYPE_PREDEF, 'Заранее определенные значения'),
        (TYPE_INT, 'Число'),
        (TYPE_STRING, 'Строка'),
    ]

    name = models.CharField(max_length=50)
    type = models.IntegerField(choices=TYPES, default=TYPE_PREDEF)
    system = models.ForeignKey(System)


class ParameterAllowedValue(BaseModel):
    value = models.CharField(max_length=50)
    parameter = models.ForeignKey(Parameter)


class Question(BaseModel):
    TYPE_PREDEF = 0
    TYPE_INT = 1
    TYPE_STRING = 2
    TYPES = [
        (TYPE_PREDEF, 'Заранее определенные значения'),
        (TYPE_INT, 'Число'),
        (TYPE_STRING, 'Строка'),
    ]
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='question_images/', blank=True, null=True)
    type = models.IntegerField(choices=TYPES, default=TYPE_PREDEF)
    parameter = models.ForeignKey(Parameter)
    system = models.ForeignKey(System)


class Answer(BaseModel):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='answer_images/', blank=True, null=True)
    parameter_value_any = models.CharField(max_length=50, default='')
    parameter_value = models.ForeignKey(ParameterAllowedValue)
    question = models.ForeignKey(Question)


###############################
class Rule(BaseModel):
    data = models.TextField()
    system = models.ForeignKey(System, blank=True, null=True)


class Session(models.Model):
    user = models.CharField(max_length=15)
    system = models.ForeignKey(System)
    current_question_id = models.IntegerField(blank=True, null=True)


class SessionParamState(models.Model):
    session = models.ForeignKey(Session)
    param = models.ForeignKey(Parameter)
    value = models.IntegerField(blank=True, null=True)


class SessionQuestionState(models.Model):
    session = models.ForeignKey(Session)
    question = models.ForeignKey(Question)
    value = models.IntegerField(blank=True, null=True)


class SessionAttributeState(models.Model):
    session = models.ForeignKey(Session)
    attr = models.ForeignKey(Attribute)
    value = models.IntegerField(blank=True, null=True)
