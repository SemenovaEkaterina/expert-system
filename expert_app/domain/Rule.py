from .common import *


class Rule:
    def __init__(self, type, condition, second_id, second_value_id, r_id=None):
        self.type = type
        self.condition = condition
        self.second_id = second_id
        self.second_value_id = second_value_id
        self.system = None
        self.id = r_id

        if self.id is None:
            if Rule.objects is not None:
                self.id = Rule.objects.create_rule({'type': self.type,
                                                    'condition': self.condition,
                                                    'second_id': self.second_id,
                                                    'second_value_id': self.second_value_id})
            else:
                self.id = 0

    def get_func(self):
        if self.type == PARAMETER_TO_ATTRIBUTE:
            def get_attribute_value(params):
                count = 0
                for x in self.condition:
                    if 'operation' not in x:
                        x['operation'] = EQ
                    operation = operations[x['operation']]
                    param = self.system.get_param_by_id(x['param_id'])

                    if x['param_value_id']:
                        value = param.get_value_by_id(x['param_value_id'])
                    else:
                        value = x['param_value_any']
                    if x['operation'] == EQ or x['operation'] ==NQ:
                        result = operation(str(params[param.id]), (value))
                    else:
                        result = operation(int(params[param.id]), int(value))
                    if param.id in params and result:
                        count += 1

                if count == len(self.condition):
                    return {'attr': self.system.get_attribute_by_id(self.second_id), 'value_id': self.second_value_id}

            return get_attribute_value
        else:
            pass

    def set_system(self, system):
        self.system = system

    def get_id(self):
        return self.id


Rule.objects = None
