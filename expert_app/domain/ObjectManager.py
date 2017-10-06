from django.db import models
from expert_app.models_domain import Object


class ObjectManager(models.Manager):

    @staticmethod
    def create_obj(name):
        obj = Object.objects.create(name=name)
        return obj.id

    @staticmethod
    def set_system(object_id, system_id):
        Object.objects.filter(id=object_id).update(system=system_id)

