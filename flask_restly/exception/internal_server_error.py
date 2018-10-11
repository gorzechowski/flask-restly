from werkzeug.exceptions import InternalServerError as WerkzeugInternalServerError


class InternalServerError(WerkzeugInternalServerError):
    description = "Internal server error"

    def __init__(self, description=None):
        if description is not None:
            self.description = description
