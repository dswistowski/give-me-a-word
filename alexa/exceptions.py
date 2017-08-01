class UnknownIntentError(Exception):
    def __init__(self, intent_name):
        self.intent_name = intent_name