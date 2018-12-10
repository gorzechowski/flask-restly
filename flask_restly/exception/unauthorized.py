from werkzeug.exceptions import Unauthorized as WerkzeugUnauthorized


class Unauthorized(WerkzeugUnauthorized):
    description = "Not authorized"

    def __init__(self, description=None):
        if description is not None:
            self.description = description
