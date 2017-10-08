# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User


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


class System(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User)  # пользователь-создатель
    author = models.CharField(max_length=100)  # как отображать автора
    description = models.TextField(default="")
    image = models.ImageField(upload_to='system_images/', blank=True, null=True)
    public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.CharField(max_length=30, default='', unique=True)

    objects = SystemManager()

    def is_by_user(self, user):
        if isinstance(user, int):
            return self.user.id == user

        if isinstance(user, User):
            return self.user.id == user.id


class Object(models.Model):
    name = models.CharField(max_length=30)
    system = models.ForeignKey(System, blank=True, null=True)


class Attribute(models.Model):
    name = models.CharField(max_length=30)
    system = models.ForeignKey(System, blank=True, null=True)


class AttributeValue(models.Model):
    value = models.CharField(max_length=30)
    attribute = models.ForeignKey(Attribute)


class ObjectAttrValues(models.Model):
    object = models.ForeignKey(Object)
    attr_value = models.ForeignKey(AttributeValue)


class ObjectAttributes(models.Model):
    attribute = models.ForeignKey(Attribute)
    object = models.ForeignKey(Object)


class Parameter(models.Model):
    name = models.CharField(max_length=30)
    system = models.ForeignKey(System, blank=True, null=True)


class ParameterValue(models.Model):
    value = models.CharField(max_length=30)
    parameter = models.ForeignKey(Parameter)


class QuestionManager(models.Manager):
    @staticmethod
    def get_count(system_id):
        return Question.objects.filter(system__id=system_id).count()


class Question(models.Model):
    text = models.CharField(max_length=60)
    type = models.IntegerField()
    system = models.ForeignKey(System, blank=True, null=True)
    questions = QuestionManager()
    objects = models.Manager()


class Answer(models.Model):
    answer = models.CharField(max_length=30)
    compare = models.IntegerField(blank=True, null=True)
    parameter = models.ForeignKey(Parameter)
    parameter_value = models.ForeignKey(ParameterValue)
    question = models.ForeignKey(Question)


class Rule(models.Model):
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
