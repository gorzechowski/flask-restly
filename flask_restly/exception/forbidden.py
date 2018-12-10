from werkzeug.exceptions import Forbidden as WerkzeugForbidden


class Forbidden(WerkzeugForbidden):
    description = "Not authenticated"

    def __init__(self, description=None):
        if description is not None:
            self.description = description
