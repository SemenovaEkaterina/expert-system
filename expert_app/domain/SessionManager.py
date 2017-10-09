from django.db import models
from expert_app.models_domain import Session
from expert_app.domain.Session import Session as OwnSession
from expert_app.models_domain import System
from expert_app.models_domain import SessionParamState
from expert_app.models_domain import SessionQuestionState
from expert_app.models_domain import SessionAttributeState
from expert_app.models_domain import Parameter
from expert_app.models_domain import Question
from expert_app.models_domain import Attribute
from expert_app.domain.System import get_system


class SessionManager(models.Manager):

    @staticmethod
    def create_session(system_id, user, params, questions):
        system = System.objects.get(id=system_id)
        session = Session.objects.create(user=user, system=system)

        for q in questions.keys():
            question = Question.objects.get(id=q)
            SessionQuestionState.objects.create(session=session, question=question, value=questions[q])

        for p in params.keys():
            param = Parameter.objects.get(id=p)
            SessionParamState.objects.create(session=session, param=param, value=params[p])

        return session.id

    @staticmethod
    def set_current_question(session_id, question_id):
        Session.objects.filter(id=session_id).update(current_question_id=question_id)

    @staticmethod
    def change_question_state(session_id, question_id, value):
        session = Session.objects.get(id=session_id)
        question = Question.objects.get(id=question_id)
        SessionQuestionState.objects.filter(session=session, question=question).update(value=value)

    @staticmethod
    def change_param_state(session_id, param_id, value):
        session = Session.objects.get(id=session_id)
        param = Parameter.objects.get(id=param_id)
        SessionQuestionState.objects.filter(session=session, param=param).update(value=value)

    @staticmethod
    def define_attr(session_id, attr_id, value):
        session = Session.objects.get(id=session_id)
        attr = Attribute.objects.get(id=attr_id)
        SessionAttributeState.objects.create(session=session, attr=attr, value=value)

    @staticmethod
    def get_by_id(s_id):
        session = Session.objects.get(id=s_id)
        system = get_system(session.system.id)
        params = {}
        questions = {}
        attrs = {}

        for p in SessionParamState.objects.filter(session=session):
            params[p.param.id] = p.value

        for a in SessionAttributeState.objects.filter(session=session):
            attrs[a.attr.id] = a.value

        for q in SessionQuestionState.objects.filter(session=session):
            questions[q.question.id] = q.value

        own_session = OwnSession(system, session.user, params, questions, attrs, session.current_question_id, session.id)
        return own_session


    @staticmethod
    def save(own_session):
        session = Session.objects.get(id=own_session.id)
        session.current_question_id = own_session.current_question_id
        session.save()

        for q in own_session.questions.keys():
            if q:
                SessionQuestionState.objects.update_or_create(session=session, question_id=q, value=own_session.questions[q])

        for p in own_session.params.keys():
            if p:
                SessionParamState.objects.update_or_create(session=session, param_id=p, value=own_session.params[p])




