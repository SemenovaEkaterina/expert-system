from django.db import models
from expert_app.models_domain import Rule
import json


class RuleManager(models.Manager):

    @staticmethod
    def create_rule(data):
        rule = Rule.objects.create(data=json.dumps(data))
        return rule.id

    @staticmethod
    def set_system(rule_id, system_id):
        rule = Rule.objects.get(id=rule_id)
        Rule.objects.filter(id=rule.id).update(system=system_id)





