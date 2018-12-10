from werkzeug.exceptions import NotImplemented as WerkzeugNotImplemented


class NotImplemented(WerkzeugNotImplemented):
    description = "Not implemented"

    def __init__(self, description=None):
        if description is not None:
            self.description = description
