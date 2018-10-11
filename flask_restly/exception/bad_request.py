from werkzeug.exceptions import BadRequest as WerkzeugBadRequest


class BadRequest(WerkzeugBadRequest):
    description = "Bad request"

    def __init__(self, description=None):
        if description is not None:
            self.description = description
