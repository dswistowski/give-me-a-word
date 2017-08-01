from alexa.core import Alexa


def test_handle_launch_request(app: Alexa, launch_request: dict):
    response = app(launch_request, None)
    assert response['response']['outputSpeech']['text'] == 'on launch'


def test_handle_intent_request(app: Alexa, intent_request: dict):
    response = app(intent_request, None)
    assert response['response']['outputSpeech']['text'] == 'get zodiac horoscope intent'


def test_session_ended_request(app: Alexa, session_ended_request: dict):
    assert app(session_ended_request, None) is None