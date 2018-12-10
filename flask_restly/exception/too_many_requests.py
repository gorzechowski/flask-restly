from werkzeug.exceptions import TooManyRequests as WerkzeugTooManyRequests


class TooManyRequests(WerkzeugTooManyRequests):
    description = "Too many requests"

    def __init__(self, description=None):
        if description is not None:
            self.description = description
