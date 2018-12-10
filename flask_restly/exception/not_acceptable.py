from werkzeug.exceptions import NotAcceptable as WerkzeugNotAcceptable


class NotAcceptable(WerkzeugNotAcceptable):
    description = "Not acceptable"

    def __init__(self, description=None):
        if description is not None:
            self.description = description
