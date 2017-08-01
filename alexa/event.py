from enum import Enum


class Request:
    type = None

    def __init__(self, locale: str, requestId: str, timestamp: str, type: str):
        self.locale = locale
        self.id = requestId
        self.timestamp = timestamp
        self.type = type

    @classmethod
    def for_type(cls, type: str, **kwargs):
        for subclass in cls.__subclasses__():
            if subclass.type == type:
                return subclass(type=type, **kwargs)


class LaunchRequest(Request):
    type = 'LaunchRequest'


class Error:
    def __init__(self, type: str, message: str):
        self.type = type
        self.message = message


class SessionEndedRequest(Request):
    type = 'SessionEndedRequest'

    def __init__(self, locale: str, requestId: str, timestamp: str, type: str, reason: str, error: dict = None):
        super().__init__(locale=locale, requestId=requestId, timestamp=timestamp, type=type)
        self.reason = reason
        if error is not None:
            self.error = Error(**error)
        else:
            self.error = None


class ConfirmationStatus(Enum):
    NONE = 'NONE'
    CONFIRMED = 'CONFIRMED'
    DENIED = 'DENIED'


class Slot:
    def __init__(self, name: str, value: str, confirmationStatus: str = None):
        self.name = name
        self.value = value
        if confirmationStatus is not None:
            self.confirmation_status = ConfirmationStatus(confirmationStatus)
        else:
            self.confirmation_status = None


class Intent:
    def __init__(self, name: str, confirmationStatus: dict = None, slots: dict = None):
        self.name = name
        if confirmationStatus is not None:
            self.confirmation_status = ConfirmationStatus(confirmationStatus)
        else:
            confirmationStatus = None
        self._slots = {}
        if slots is not None:
            for name, slot_data in slots.items():
                self._slots[name] = Slot(**slot_data)


class IntentRequest(Request):
    type = 'IntentRequest'

    def __init__(self, locale: str, requestId: str, timestamp: str, type: str, intent: dict, dialogState: dict = None):
        super().__init__(locale=locale, requestId=requestId, timestamp=timestamp, type=type)
        self.dialog_state = dialogState
        self.intent = Intent(**intent)


class Application:
    def __init__(self, applicationId: str):
        self.id = applicationId


class User:
    def __init__(self, userId: str):
        user_id = userId
        if callable(user_id):
            user_id = user_id()
        self.id = user_id


class Session:
    def __init__(self, application: dict, new: bool, sessionId: str, user: dict, attributes: dict=None):
        self.application = Application(**application)
        self.attributes = attributes
        self.new = new
        self.session_id = sessionId
        self.user = User(**user)


class Event:
    def __init__(self, request: dict, session: dict, version: str, context: dict = None):
        self.request = Request.for_type(**request)
        self.session = Session(**session)
        self.version = version
        self.context = context
