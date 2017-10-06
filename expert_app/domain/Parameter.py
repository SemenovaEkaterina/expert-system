class Parameter:
    def __init__(self, name, values, p_id=None):
        self.name = name
        self.values = []
        self.questions = []
        self.id = p_id

        if self.id is None:
            if Parameter.objects is not None:
                self.id = Parameter.objects.create_par(self.name)
                for x in values:
                    self.values.append({'id': Parameter.objects.add_par_value(self.id, x), 'value': x})

            else:
                self.id = Parameter.id
                Parameter.id += 1
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

    def get_value_by_id(self, id):
        for x in self.values:
            if x['id'] == id:
                return x['value']

    def add_question(self, question):
        self.questions.append(question)

    def get_questions(self):
        return self.questions


Parameter.id = 0
Parameter.objects = None
