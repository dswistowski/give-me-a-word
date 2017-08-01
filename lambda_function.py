import config
from alexa.core import Alexa
from alexa.event import LaunchRequest, Session, IntentRequest
from alexa.response import Response, Body, Speech, StandardCard
from dictionary import get_random_word


class MyAlexa(Alexa):
    def on_launch(self, request: LaunchRequest, session: Session) -> Response:
        word, definition = get_random_word()
        return Response(Body(speech=Speech('Definition for word: {} is: {}'.format(word, definition)), card=StandardCard(title=word.capitalize(), body=definition.capitalize())))

app = MyAlexa(config.APP_ID)


@app.intent('GiveMeAWord')
def give_me_a_word(request: IntentRequest, session: Session) -> Response:
    word, definition = get_random_word()
    return Response(Body(speech=Speech('Definition for word: {} is: {}'.format(word, definition)),
                         card=StandardCard(title=word.capitalize(), body=definition.capitalize())))


@app.intent('AMAZON.HelpIntent')
def help(request: IntentRequest, session: Session) -> Response:
    return Response(Body(speech=Speech('Give me a word provides you a random English word with it definition')))


bye_bye_message = Response(Body(speech=Speech('Give me a word is going sleep, Bye bye!')))


@app.intent('AMAZON.CancelIntent')
def cancel(request: IntentRequest, session: Session) -> Response:
    return bye_bye_message


@app.intent('AMAZON.StopIntent')
def stop(request: IntentRequest, session: Session) -> Response:
    return bye_bye_message

lambda_handler = app
