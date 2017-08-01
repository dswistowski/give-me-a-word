from abc import ABCMeta, abstractmethod

from typing import List, Optional


class Dictable(metaclass=ABCMeta):
    @abstractmethod
    def to_dict(self) -> dict:
        return {}


class Session(Dictable):
    def __init__(self, data):
        self.data = data

    def to_dict(self):
        return self.data


class Speech(Dictable):
    def __init__(self, body: str):
        self.body = body

    def to_dict(self):
        return {
            'type': 'PlainText',
            'text': self.body
        }


class SSMLSpeech(Speech):
    def to_dict(self):
        return {
            'type': 'SSML',
            'ssml': self.body
        }


class Card(Dictable):
    @abstractmethod
    def get_type(self):
        pass

    @abstractmethod
    def to_dict(self):
        return {'type': self.get_type()}


class LinkAccountCard(Card):
    def get_type(self):
        return "LinkAccount"

    def to_dict(self):
        return super().to_dict()


class SimpleCard(Card):
    def __init__(self, title: str = None, body: str = ''):
        self.title = title
        self.body = body

    def get_type(self):
        return "Simple"

    def to_dict(self):
        ret = super().to_dict()
        if self.title is not None:
            ret['title'] = self.title
        ret['content'] = self.body
        return ret


class Image(Dictable):
    def __init__(self, small_url: str, large_url: str):
        self.small_url = small_url
        self.large_url = large_url

    def to_dict(self):
        return {
            'smallImageUrl': self.small_url,
            'largeImageUrl': self.large_url
        }


class StandardCard(Card):
    def __init__(self, title: str = None, body: str = '', image: Image = None):
        self.title = title
        self.body = body
        self.image = image

    def get_type(self):
        return "Standard"

    def to_dict(self):
        ret = super().to_dict()
        if self.title is not None:
            ret['title'] = self.title
        ret['text'] = self.body
        if self.image is not None:
            ret['image'] = self.image.to_dict()
        return ret


class Reprompt(Dictable):
    def __init__(self, speech: Speech = None):
        self.speech = speech

    def to_dict(self):
        ret = {}
        if self.speech is not None:
            ret['outputSpeech'] = self.speech.to_dict()
        return ret


class Directive(Dictable):
    def to_dict(self) -> dict:
        return {}


class Body(Dictable):
    def __init__(self, speech: Speech = None, card: Card = None, reprompt: Reprompt = None,
                 should_end_session: bool = True, directives: Optional[List[Directive]] = None):
        self.speech = speech
        self.card = card
        self.reprompt = reprompt
        self.should_end_session = should_end_session
        self.directives = directives

    def to_dict(self) -> dict:
        ret = {
            "shouldEndSession": self.should_end_session
        }
        if self.speech:
            ret['outputSpeech'] = self.speech.to_dict()
        if self.card:
            ret['card'] = self.card.to_dict()
        if self.reprompt:
            ret['reprompt'] = self.reprompt.to_dict()
        if self.directives:
            ret['directives'] = [d.to_dict() for d in self.directives]
        return ret


class Response(Dictable):
    def __init__(self, body: Body, session: Session = None, version: str = "1.0"):
        self.session = session
        self.version = version
        self.body = body

    def to_dict(self):
        ret = {
            'version': self.version,
            'response': self.body.to_dict()
        }
        if self.session is not None:
            ret['sessionAttributes'] = self.session.to_dict()
        return ret
