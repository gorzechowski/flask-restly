from werkzeug.exceptions import NotFound as WerkzeugNotFound


class NotFound(WerkzeugNotFound):
    description = "Entity not found"

    def __init__(self, description=None):
        if description is not None:
            self.description = description
