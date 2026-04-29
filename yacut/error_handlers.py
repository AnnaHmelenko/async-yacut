from flask import jsonify, render_template, request

from yacut import db
from yacut.exceptions import APIError


def register_error_handlers(app):
    @app.errorhandler(APIError)
    def handle_api_error(error):
        return jsonify({'message': error.message}), error.status_code

    @app.errorhandler(404)
    def page_not_found(error):
        if request.path.startswith('/api/'):
            return jsonify({'message': 'Указанный id не найден'}), 404
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        if request.path.startswith('/api/'):
            return jsonify({'message': 'Внутренняя ошибка сервера'}), 500
        return render_template('500.html'), 500
