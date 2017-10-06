#! /usr/bin/env python
# -*- coding: utf-8 -*-


from .common import *


class System:
    def __init__(self, name, s_id=None):
        self.name = name
        self.objs = []
        self.attributes = []
        self.params = []
        self.questions = []
        self.rules = []
        self.id = s_id

        if self.id is None and System.objects is not None:
            self.id = System.objects.create_system(self.name)

    def get_id(self):
        return self.id

    def add_object(self, obj):
        self.objs.append(obj)

        if obj.objects is not None:
            obj.objects.set_system(obj.get_id(), self.id)

    def get_objects(self):
        return self.objs

    def add_attribute(self, attribute):
        self.attributes.append(attribute)

        if attribute.objects is not None:
            attribute.objects.set_system(attribute.get_id(), self.id)

    def get_attribute_list(self):
        return [{'id': x.get_id(), 'value': x.get_name()} for x in self.attributes]

    def add_param(self, param):
        self.params.append(param)

        if param.objects is not None:
            param.objects.set_system(param.get_id(), self.id)

    def get_param_list(self):
        return [{'id': x.get_id(), 'value': x.get_name()} for x in self.params]

    def get_attribute_by_id(self, id):
        for x in self.attributes:
            if x.get_id() == id:
                return x

    def get_object_list(self):
        return [{'id': x.get_id(), 'value': x.get_name()} for x in self.objs]

    def get_object_by_id(self, id):
        for x in self.objs:
            if x.get_id() == id:
                return x

    def get_param_by_id(self, id):
        for x in self.params:
            if x.get_id() == id:
                return x

    def get_params(self):
        return self.params

    def get_questions(self):
        return self.questions

    def get_attrs(self):
        return self.attributes

    def add_rule(self, rule):
        self.rules.append(rule)
        rule.set_system(self)

        if rule.objects is not None:
            rule.objects.set_system(rule.get_id(), self.id)

    def get_rules(self):
        return self.rules

    def add_question(self, question):
        self.questions.append(question)

        if question.objects is not None:
            question.objects.set_system(question.get_id(), self.id)

    def print_tree(self):
        print(self.name)
        print('\n' + TAB + 'Атрибуты:')
        for attr in self.attributes:
            print(TAB * 2 + str(attr.get_id()) + ')  ' + attr.get_name())
            print(TAB * 3, attr.get_values())
        print('\n' + TAB + 'Параметры:')
        for param in self.params:
            print(TAB * 2 + str(param.get_id()) + ')  ' + param.get_name())
            print(TAB * 3, param.get_values())
            print(TAB * 4, 'Вопросы:')
            for question in param.get_questions():
                print(TAB * 5, question.get_id(), ')  ', question.get_text(), question.get_options())

        print('\n' + TAB + 'Объекты:')
        for obj in self.objs:
            print(TAB * 2 + str(obj.get_id()) + ')  ' + obj.get_name())
            print(TAB * 3, obj.get_attribute_pairs())


System.objects = None


def get_system(id):
    return System.objects.get_by_id(id)


def all():
    return System.objects.all()
