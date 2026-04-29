from flask import jsonify, current_app


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


def register_error_handlers(app):
    """Регистрация обработчиков ошибок"""

    @app.errorhandler(APIError)
    def handle_api_error(error):
        return jsonify({'message': error.message}), error.status_code

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({'message': 'Указанный id не найден'}), 404
