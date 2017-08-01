import pytest

from alexa.core import Alexa
from alexa.event import LaunchRequest, Session, IntentRequest, SessionEndedRequest
from alexa.response import Response, Body, Speech

LAUNCH_REQUEST_EXAMPLE = {
  "version": "1.0",
  "session": {
    "new": True,
    "sessionId": "amzn1.echo-api.session.0000000-0000-0000-0000-00000000000",
    "application": {
      "applicationId": "amzn1.echo-sdk-ams.app.000000-d0ed-0000-ad00-000000d00ebe"
    },
    "attributes": {},
    "user": {
      "userId": "amzn1.account.AM3B00000000000000000000000"
    }
  },
  "context": {
    "System": {
      "application": {
        "applicationId": "amzn1.echo-sdk-ams.app.000000-d0ed-0000-ad00-000000d00ebe"
      },
      "user": {
        "userId": "amzn1.account.AM3B00000000000000000000000"
      },
      "device": {
        "supportedInterfaces": {
          "AudioPlayer": {}
        }
      }
    },
    "AudioPlayer": {
      "offsetInMilliseconds": 0,
      "playerActivity": "IDLE"
    }
  },
  "request": {
    "type": "LaunchRequest",
    "requestId": "amzn1.echo-api.request.0000000-0000-0000-0000-00000000000",
    "timestamp": "2015-05-13T12:34:56Z",
    "locale": "string"
  }
}


INTENT_REQUEST_EXAMPLE = {
  "version": "1.0",
  "session": {
    "new": True,
    "sessionId": "amzn1.echo-api.session.0000000-0000-0000-0000-00000000000",
    "application": {
      "applicationId": "amzn1.echo-sdk-ams.app.000000-d0ed-0000-ad00-000000d00ebe"
    },
    "attributes": {
      "supportedHoroscopePeriods": {
        "daily": False,
        "weekly": False,
        "monthly": False
      }
    },
    "user": {
      "userId": "amzn1.account.AM3B00000000000000000000000"
    }
  },
  "context": {
    "System": {
      "application": {
        "applicationId": "amzn1.echo-sdk-ams.app.000000-d0ed-0000-ad00-000000d00ebe"
      },
      "user": {
        "userId": "amzn1.account.AM3B00000000000000000000000"
      },
      "device": {
        "supportedInterfaces": {
          "AudioPlayer": {}
        }
      }
    },
    "AudioPlayer": {
      "offsetInMilliseconds": 0,
      "playerActivity": "IDLE"
    }
  },
  "request": {
    "type": "IntentRequest",
    "requestId": " amzn1.echo-api.request.0000000-0000-0000-0000-00000000000",
    "timestamp": "2015-05-13T12:34:56Z",
    "dialogState": "COMPLETED",
    "locale": "string",
    "intent": {
      "name": "GetZodiacHoroscopeIntent",
      "confirmationStatus": "NONE",
      "slots": {
        "ZodiacSign": {
          "name": "ZodiacSign",
          "value": "virgo",
          "confirmationStatus": "NONE"
        }
      }
    }
  }
}

SESSION_ENDED_EXAMPLE = {
  "version": "1.0",
  "session": {
    "new": False,
    "sessionId": "amzn1.echo-api.session.0000000-0000-0000-0000-00000000000",
    "application": {
      "applicationId": "amzn1.echo-sdk-ams.app.000000-d0ed-0000-ad00-000000d00ebe"
    },
    "attributes": {
      "supportedHoroscopePeriods": {
        "daily": True,
        "weekly": False,
        "monthly": False
      }
    },
    "user": {
      "userId": "amzn1.account.AM3B00000000000000000000000"
    }
  },
  "context": {
    "System": {
      "application": {
        "applicationId": "amzn1.echo-sdk-ams.app.000000-d0ed-0000-ad00-000000d00ebe"
      },
      "user": {
        "userId": "amzn1.account.AM3B00000000000000000000000"
      },
      "device": {
        "supportedInterfaces": {
          "AudioPlayer": {}
        }
      }
    },
    "AudioPlayer": {
      "offsetInMilliseconds": 0,
      "playerActivity": "IDLE"
    }
  },
  "request": {
    "type": "SessionEndedRequest",
    "requestId": "amzn1.echo-api.request.0000000-0000-0000-0000-00000000000",
    "timestamp": "2015-05-13T12:34:56Z",
    "reason": "USER_INITIATED",
    "locale": "string"
  }
}


@pytest.fixture
def launch_request():
    return LAUNCH_REQUEST_EXAMPLE


@pytest.fixture
def intent_request():
    return INTENT_REQUEST_EXAMPLE

@pytest.fixture
def session_ended_request():
    return SESSION_ENDED_EXAMPLE

@pytest.fixture
def app():
    class MyAlexa(Alexa):
        def on_launch(self, request: LaunchRequest, session: Session) -> Response:
            return Response(Body(speech=Speech('on launch')))


    app = MyAlexa('amzn1.echo-sdk-ams.app.000000-d0ed-0000-ad00-000000d00ebe')

    @app.intent('GetZodiacHoroscopeIntent')
    def get_zodiac_horoscope_intent(request: IntentRequest, session: Session) -> Response:
        return Response(Body(speech=Speech('get zodiac horoscope intent')))

    return app