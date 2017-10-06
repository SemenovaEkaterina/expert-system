class Object:
    def __init__(self, name, id=None):

        self.name = name
        self.attributes = {}
        self.id = id

        if self.id is None:
            if Object.objects is not None:
                self.id = Object.objects.create_obj(self.name)
            else:
                self.id = Object.id
                Object.id += 1

    def get_name(self):
        return self.name

    def set_attribute(self, attr, value_id):
        self.attributes[attr] = value_id

    def get_attribute_pairs(self):
        return [{'attr': x.get_name(), 'value': self.attributes[x]} for x in self.attributes]

    def get_id(self):
        return self.id

    def get_attributes(self):
        return self.attributes


Object.id = 0
Object.objects = None
