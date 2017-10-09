from .Session import Session
from .SessionManager import SessionManager
from .System import System
from .SystemManager import SystemManager
from .Question import Question
from .QuestionManager import QuestionManager
from .Object import Object
from .ObjectManager import ObjectManager
from .Attr import Attr
from .AttrManager import AttrManager


def enableManagers():
    Session.objects = SessionManager
    System.objects = SystemManager
    Question.objects = QuestionManager
    Object.objects = ObjectManager
    Attr.objects = AttrManager
