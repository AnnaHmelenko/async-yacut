class APIError(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(APIError):
    def __init__(self, message="Not Found"):
        super().__init__(message, 404)


class BadRequestError(APIError):
    def __init__(self, message="Bad Request"):
        super().__init__(message, 400)
