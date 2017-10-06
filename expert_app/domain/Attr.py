class Attr:
    def __init__(self, name, values, a_id=None):
        self.name = name
        self.values = []
        self.id = a_id

        if self.id is None:
            if Attr.objects is not None:
                self.id = Attr.objects.create_attr(self.name)
                for x in values:
                    self.values.append({'id': Attr.objects.add_attr_value(self.id, x), 'value': x})

            else:
                self.id = Attr.id
                Attr.id += 1
                self.values_count = 0
                for x in values:
                    self.values.append({'id': self.values_count, 'value': x})
                    self.values_count += 1
        else:
            self.values = values

    def add_value(self, value):
        self.values.append({'id': self.values_count, 'value': value})
        self.values_count += 1

    def get_values(self):
        return [x for x in self.values]

    def get_value_id(self, value):
        for x in self.values:
            if x['value'] == value:
                return x['id']

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def get_value_by_id(self, value_id):
        for x in self.values:
            if x['id'] == value_id:
                return x['value']


Attr.id = 0
Attr.objects = None
