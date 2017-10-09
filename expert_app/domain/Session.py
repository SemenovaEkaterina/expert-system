#! /usr/bin/env python
# -*- coding: utf-8 -*-


from .common import *


class Session:
    def __init__(self, system, user, params=None, questions=None, attrs=None, s_id=None):
        self.system = system
        self.user = user
        self.id = s_id

        self.params = {}
        self.questions = {}

        self.current_question_id = None

        for param in system.get_params():
            self.params[param] = None
        for question in system.get_questions():
            self.questions[question] = None

        self.attrs = {}

        self.objects_stat = {}

        if self.id is None:
            if Session.objects is not None:
                self.id = Session.objects.create_session(self.system.get_id(), self.user, self.params, self.questions)
        else:
            self.questions = questions
            self.params = params
            self.attrs = attrs

    def is_asked(self, question_id):
        for question in self.questions.keys():
            if question.get_id() == question_id and self.questions[question] is None:
                return 0
        return 1

    def set_asked(self, question_id):
        for question in self.questions.keys():
            if question.get_id() == question_id:
                self.questions[question] = -2
                if Session.objects is not None:
                    Session.objects.change_question_state(self.id, self.current_question_id, -2)

    def next_question(self):
        for question in self.system.get_questions():
            if not self.is_asked(question.get_id()):
                self.current_question_id = question.get_id()
                if Session.objects is not None:
                    Session.objects.set_current_question(self.id, self.current_question_id)
                self.set_asked(self.current_question_id)
                return {'type': question.type, 'text': question.text, 'answers': question.get_options() }
        return None

    def answer(self, value_id, user_answer=None):
        for question in self.questions.keys():
            if question.get_id() == self.current_question_id:
                self.questions[question] = value_id

                if Session.objects is not None:
                    Session.objects.change_question_state(self.id, self.current_question_id, value_id)

                self.current_question_id = None

                param = self.system.get_param_by_id(question.get_param_id_by_answer(value_id, user_answer))

                param_value = question.get_param_value_by_answer(value_id, user_answer)
                self.params[param] = param_value

                if param and Session.objects is not None:
                    Session.objects.change_param_state(self.id, param.get_id(), param_value)

                for rule in self.system.rules:
                    result = rule.get_func()(self.params)
                    if result is not None:
                        self.attrs[result['attr']] = result['value_id']

                        if Session.objects is not None:
                            Session.objects.define_attr(self.id, result['attr'].get_id(), result['value_id'])

                        self.update_stat()

    def update_stat(self):
        self.objects_stat.clear()
        for obj in self.system.get_objects():
            self.objects_stat[obj] = 0;
            for attr in self.attrs.keys():
                if attr in obj.get_attributes() and obj.get_attributes()[attr] == self.attrs[attr]:
                    self.objects_stat[obj] += 1

    def print_tree(self):
        print(LINE)
        print('Cостояние сессии:')
        print(TAB, 'Параметры:')
        for param in self.params.keys():
            print(TAB * 2, param.get_id(), ')  ', param.get_name(), ': ', param.get_value_by_id(self.params[param]))

        print(TAB, 'Определенные атрибуты:')
        for attr in self.attrs.keys():
            print(TAB * 2, attr.get_id(), ')  ', attr.get_name(), ': ', attr.get_value_by_id(self.attrs[attr]))

        print(TAB, 'Объекты:')
        for obj in self.objects_stat.keys():
            print(TAB * 2, obj.get_name(), round(100 * self.objects_stat[obj] / len(obj.get_attributes())))

        print(LINE)

    def get_stat(self):
        self.update_stat()
        result = []
        for obj in self.objects_stat.keys():
            result.append({'name': obj.get_name(), 'value': round(100 * self.objects_stat[obj] / (len(obj.get_attributes()) + 0.0001))})

        return result


Session.objects = None

def get_session(id):
    return Session.objects.get_by_id(id)
