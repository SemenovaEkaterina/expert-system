import json

from django.db import models
from expert_app.models_domain import System
from expert_app.domain.System import System as OwnSystem
from expert_app.models_domain import Object
from expert_app.domain.Object import Object as OwnObject
from expert_app.models_domain import Attribute
from expert_app.domain.Attr import Attr as OwnAttr
from expert_app.models_domain import AttributeAllowedValue
from expert_app.models_domain import Parameter
from expert_app.domain.Parameter import Parameter as OwnParameter
from expert_app.models_domain import ParameterAllowedValue
from expert_app.models_domain import Question
from expert_app.domain.Question import Question as OwnQuestion
from expert_app.models_domain import Answer
from expert_app.models_domain import Rule
from expert_app.domain.Rule import Rule as OwnRule
from expert_app.models_domain import ObjectAttributeValue

from .common import *

import ast


class SystemManager(models.Manager):
    @staticmethod
    def create_system(name):
        system = System.objects.create(name=name)
        return system.id

    @staticmethod
    def all():
        systems = []
        for s in System.objects.all():
            system = OwnSystem(s.name, s.id)
            systems.append(system)
        return systems

    @staticmethod
    def get_by_id(s_id):
        system = System.objects.get(id=s_id)
        own_system = OwnSystem(system.name, system.id)
        for obj in Object.objects.filter(system=system):
            own_object = OwnObject(obj.name, obj.id)
            own_system.add_object(own_object)
            for attr in ObjectAttributeValue.objects.filter(object=obj):
                own_object.set_attribute(attr.attribute.id, attr.attribute_value_id)

        for attr in Attribute.objects.filter(system=system):
            values = []
            for v in AttributeAllowedValue.objects.filter(attribute=attr):
                values.append({'id': v.id, 'value': v.value})
            own_system.add_attribute(OwnAttr(attr.name, values, attr.id))
        for param in Parameter.objects.filter(system=system):
            values = []
            for p in ParameterAllowedValue.objects.filter(parameter=param):
                values.append({'id': p.id, 'value': p.value})
            own_system.add_param(OwnParameter(param.name, values, param.id))
        for question in Question.objects.filter(system=system):
            options = []
            for o in Answer.objects.filter(question=question):
                options.append({'id': o.id, 'compare': EQ, 'answer': o.name, 'param_id': o.question.parameter.id,
                                'param_value_id': o.parameter_value.id})
            own_system.add_question(OwnQuestion(question.name, question.type, options, question.id))
        for rule in Rule.objects.filter(system=system):
            data = json.loads(rule.data)
            own_system.add_rule(OwnRule(data['type'], data['condition'], data['second_id'], data['second_value_id'], rule.id))
        return own_system
