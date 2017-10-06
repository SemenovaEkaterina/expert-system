#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .Object import Object
from .System import System
from .Attr import Attr
from .Parameter import Parameter
from .Question import Question
from .Session import Session
from .Rule import Rule

from .common import *

system = System('Сериалы')

obj1 = Object('Универ')
obj2 = Object('Менты 5')
obj3 = Object('Глухарь')

attr1 = Attr('жанр', ['комедия', 'криминал', 'драма'])
attr2 = Attr('длительность', ['долго', 'недолго'])
attr3 = Attr('возраст', ['старый', 'ребенок'])

par1 = Parameter('смешной', ['да', 'нет'])
par2 = Parameter('взрослый', ['да', 'нет'])
par3 = Parameter('долгий', ['да', 'нет'])

q1 = Question('Любите смеяться?', CHOICE,
              [{'answer': 'да', 'param_id': par1.get_id(), 'param_value_id': par1.get_value_id('да')},
               {'answer': 'нет', 'param_id': par1.get_id(), 'param_value_id': par1.get_value_id('нет')}])

q2 = Question('Сколько лет?', INPUT,
              [{'compare': LT, 'answer': 13, 'param_id': par2.get_id(), 'param_value_id': par2.get_value_id('нет')},
               {'compare': GQ, 'answer': 13, 'param_id': par2.get_id(), 'param_value_id': par2.get_value_id('да')}])
q3 = Question('Много времени?', CHOICE,
              [{'answer': 'да', 'param_id': par3.get_id(), 'param_value_id': par3.get_value_id('да')},
               {'answer': 'нет', 'param_id': par3.get_id(), 'param_value_id': par3.get_value_id('нет')}])
q3 = Question('Сколько минут потратить на просмотр серии?', INPUT,
              [{'compare': LT, 'answer': 30, 'param_id': par3.get_id(), 'param_value_id': par3.get_value_id('нет')},
               {'compare': GT, 'answer': 30, 'param_id': par3.get_id(), 'param_value_id': par3.get_value_id('да')}])

rule1 = Rule(PARAMETER_TO_ATTRIBUTE,
             [{'param': par1.get_id(), 'param_value': par1.get_value_id('да'), 'operation': EQ}],
             attr1.get_id(), attr1.get_value_id('комедия'))
rule2 = Rule(PARAMETER_TO_ATTRIBUTE,
             [{'param': par1.get_id(), 'param_value': par1.get_value_id('нет')}],
             attr1.get_id(), attr1.get_value_id('драма'))
rule3 = Rule(PARAMETER_TO_ATTRIBUTE, [{'param': par3.get_id(), 'param_value': par3.get_value_id('да')}],
             attr2.get_id(), attr2.get_value_id('долго'))
rule4 = Rule(PARAMETER_TO_ATTRIBUTE, [{'param': par3.get_id(), 'param_value': par3.get_value_id('нет')}],
             attr2.get_id(), attr2.get_value_id('недолго'))
rule5 = Rule(PARAMETER_TO_ATTRIBUTE, [{'param': par2.get_id(), 'param_value': par2.get_value_id('да')}],
             attr3.get_id(), attr3.get_value_id('старый'))
rule6 = Rule(PARAMETER_TO_ATTRIBUTE, [{'param': par2.get_id(), 'param_value': par2.get_value_id('нет')}],
             attr3.get_id(), attr3.get_value_id('ребенок'))

system.add_attribute(attr1)
system.add_attribute(attr2)
system.add_attribute(attr3)

system.add_object(obj1)
system.add_object(obj2)
system.add_object(obj3)

system.add_param(par1)
system.add_param(par2)
system.add_param(par3)

system.add_rule(rule1)
system.add_rule(rule2)
system.add_rule(rule3)
system.add_rule(rule4)
system.add_rule(rule5)
system.add_rule(rule6)

system.add_question(q1)
system.add_question(q2)
system.add_question(q3)

system.get_object_by_id(0).set_attribute(system.get_attribute_by_id(0), 0)
system.get_object_by_id(0).set_attribute(system.get_attribute_by_id(1), 1)
system.get_object_by_id(0).set_attribute(system.get_attribute_by_id(2), 1)

system.get_object_by_id(1).set_attribute(system.get_attribute_by_id(0), 1)
system.get_object_by_id(1).set_attribute(system.get_attribute_by_id(1), 0)
system.get_object_by_id(1).set_attribute(system.get_attribute_by_id(2), 0)

system.get_object_by_id(2).set_attribute(system.get_attribute_by_id(0), 0)
system.get_object_by_id(2).set_attribute(system.get_attribute_by_id(1), 0)
system.get_object_by_id(2).set_attribute(system.get_attribute_by_id(2), 0)

# system.print_tree()
# print(LINE, '\n')

session = Session(system, 'kate')

session.print_tree()

next_q = session.next_question()
while next_q is not None:

    print(next_q.get_id(), ')  ', next_q.get_text())

    if next_q.get_type() == CHOICE:
        for option in next_q.get_options():
            print(TAB, option['id'], ')  ', option['answer'])
        print(LINE)
        print('Выберете ответ')
        answer = input()
        session.answer(int(answer))
    else:
        print(LINE)
        print('Введите ответ')
        answer = input()
        session.answer(-1, int(answer))

    session.print_tree()
    next_q = session.next_question()
