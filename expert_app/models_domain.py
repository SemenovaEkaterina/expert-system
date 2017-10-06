# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class System(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User)  # пользователь-создатель
    author = models.CharField(max_length=100)  # как отображать автора


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


class Question(models.Model):
    text = models.CharField(max_length=60)
    type = models.IntegerField()
    system = models.ForeignKey(System, blank=True, null=True)


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
