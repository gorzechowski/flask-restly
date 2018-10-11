from werkzeug.exceptions import Conflict as WerkzeugConflict


class Conflict(WerkzeugConflict):
    description = "Conflict"

    def __init__(self, description=None):
        if description is not None:
            self.description = description
