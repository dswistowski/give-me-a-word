from abc import abstractmethod, ABCMeta

from typing import Any, Callable

from alexa.event import Request, Session, Event, LaunchRequest, IntentRequest, SessionEndedRequest
from alexa.exceptions import UnknownIntentError
from alexa.response import Response, Dictable


class Alexa(metaclass=ABCMeta):
    def __init__(self, app_id):
        self._app_id = app_id

        self.request_type_handlers = {
            LaunchRequest.type: self.on_launch,
            IntentRequest.type: self.on_intent,
            SessionEndedRequest.type: self.on_session_ended
        }
        self.intents = {}

    def intent(self, intent_name: str):
        def _register(intent: Callable[[Request, Session], Response]):
            self.intents[intent_name] = intent
            return intent

        return _register

    @abstractmethod
    def on_launch(self, request: LaunchRequest, session: Session) -> Response:
        pass

    def on_session_started(self, request_id, session: Session) -> Response:
        pass

    def on_session_ended(self, request: SessionEndedRequest, session: Session) -> None:
        pass

    def on_intent(self, request: Request, session: Session):
        try:
            intent = self.intents[request.intent.name]
        except KeyError:
            raise UnknownIntentError(request.intent.name)
        return intent(request, session)

    def __call__(self, event: dict, context: Any):
        event = Event(**event)
        assert event.session.application.id == self._app_id

        if event.session.new:
            self.on_session_started(event.request.id, event.session)

        if event.request.type in self.request_type_handlers:
            response = self.request_type_handlers[event.request.type](event.request, event.session)
        else:
            raise ValueError('Unknown request type: {}'.format(event.request.type))

        if isinstance(response, Dictable):
            return response.to_dict()
        return response
