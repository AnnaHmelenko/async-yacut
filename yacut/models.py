from datetime import datetime
from yacut import db
from yacut.exceptions import BadRequestError
from yacut.constants import SHORT_ID_LENGTH, MAX_CUSTOM_ID_LENGTH, SYMBOLS


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False, index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def create_short_link(original, custom_id=None):
        """
        Метод для создания короткой ссылки
        - Если указан custom_id, проверяем его на валидность
        - Если custom_id не указан, генерируем уникальный
        """
        if custom_id:
            if not URLMap.is_valid_short_id(custom_id):
                raise BadRequestError(
                    'Указано недопустимое имя для короткой ссылки')

            if URLMap.query.filter_by(short=custom_id).first():
                raise BadRequestError(
                    'Предложенный вариант короткой ссылки уже существует.')
        else:
            custom_id = URLMap.get_unique_short_id()

        url_map = URLMap(
            original=original,
            short=custom_id
        )

        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def get_by_short(short_id):
        """
        Метод для получения URL по короткому ID.
        Возвращает None, если не найдено.
        """
        return URLMap.query.filter_by(short=short_id).first()

    @staticmethod
    def get_unique_short_id():
        """
        Генерирует уникальный короткий ID.
        """
        from random import choices

        while True:
            short_id = ''.join(choices(SYMBOLS, k=SHORT_ID_LENGTH))

            if URLMap.query.filter_by(short=short_id).first() is None:
                return short_id

    @staticmethod
    def is_valid_short_id(short_id):
        """
        Проверяет, является ли short_id валидным.
        """
        return len(short_id) <= MAX_CUSTOM_ID_LENGTH and all(
            symbol in SYMBOLS for symbol in short_id)
