from werkzeug.exceptions import UnprocessableEntity as WerkzeugUnprocessableEntity


class UnprocessableEntity(WerkzeugUnprocessableEntity):
    description = "Unprocessable entity"

    def __init__(self, description=None):
        if description is not None:
            self.description = description
