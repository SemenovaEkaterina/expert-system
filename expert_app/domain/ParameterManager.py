from django.db import models
from expert_app.models_domain import Parameter
from expert_app.models_domain import ParameterAllowedValue


class ParameterManager(models.Manager):

    @staticmethod
    def create_par(name):
        par = Parameter.objects.create(name=name)
        return par.id

    @staticmethod
    def set_system(par_id, system_id):
        Parameter.objects.filter(id=par_id).update(system=system_id)

    @staticmethod
    def add_par_value(par_id, value):
        par = Parameter.objects.get(id=par_id)
        value = ParameterAllowedValue.objects.create(value=value, parameter=par)
        return value.id


