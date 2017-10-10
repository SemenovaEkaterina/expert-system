from .common import *


class Question:
    def __init__(self, text, question_type, options, q_id=None, param=None):
        self.type = question_type
        self.text = text
        self.options = []
        self.id = q_id
        self.param = param

        if self.id is None:
            if Question.objects is not None:
                self.id = Question.objects.create_question(self.text, self.type)
                for option in options:
                    option['id'] = Question.objects.add_answer(self.id, option)
                    self.options.append(option)
            else:
                self.count = 0
                self.id = Question.id
                Question.id += 1
                for option in options:
                    option['id'] = self.count
                    self.count += 1
                    self.options.append(option)
        else:
            self.options = options

    def get_options(self):
        return self.options

    def get_text(self):
        return self.text

    def get_id(self):
        return self.id

    def get_param_value_by_answer(self, answer_id, user_answer):
        for option in self.options:
            if int(option['id']) == int(answer_id):
                return option['param_value']
            if int(answer_id) is -1:
                if operations[option['compare']](user_answer, option['answer']):
                    return option['param_value']

    def get_param_id_by_answer(self, answer_id, user_answer):
        for option in self.options:
            if int(option['id']) == int(answer_id):
                return option['param_id']
            if answer_id is None:
                if operations[option['compare']](user_answer, option['answer']):
                    return option['param_id']

    def get_type(self):
        return self.type

    def get_param(self):
        return self.param


Question.id = 0
Question.objects = None
