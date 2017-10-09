from django.db import models
from expert_app.models_domain import Question
from expert_app.models_domain import Answer
from expert_app.models_domain import Parameter
from expert_app.models_domain import ParameterAllowedValue


class QuestionManager(models.Manager):

    @staticmethod
    def create_question(text, type):
        question = Question.objects.create(text=text, type=type)
        return question.id

    @staticmethod
    def set_system(question_id, system_id):
        Question.objects.filter(id=question_id).update(system=system_id)

    @staticmethod
    def add_answer(question_id, option):
        question = Question.objects.get(id=question_id)
        parameter = Parameter.objects.get(id=option['param_id'])
        param_value = ParameterAllowedValue.objects.get(id=option['param_value_id'])
        if 'compare' in option:
            compare = option['compare']
        else:
            compare = None
        answer = Answer.objects.create(compare=compare,
                                       answer=option['answer'],
                                       parameter=parameter,
                                       parameter_value=param_value,
                                       question=question)
        return answer.id


