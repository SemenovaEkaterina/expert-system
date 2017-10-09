from django.db import models
from expert_app.models_domain import Attribute
from expert_app.models_domain import AttributeAllowedValue


class AttrManager(models.Manager):

    @staticmethod
    def create_attr(name):
        attr = Attribute.objects.create(name=name)
        return attr.id

    @staticmethod
    def set_system(attr_id, system_id):
        Attribute.objects.filter(id=attr_id).update(system=system_id)

    @staticmethod
    def add_attr_value(attr_id, value):
        attr = Attribute.objects.get(id=attr_id)
        value = AttributeAllowedValue.objects.create(value=value, attribute=attr)
        return value.id


