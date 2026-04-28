from flask import Blueprint, jsonify, request, url_for
from yacut import db
from yacut.models import URLMap
from yacut.utils import get_unique_short_id, is_valid_short_id
from yacut.exceptions import BadRequestError, NotFoundError
from yacut.constants import MAX_CUSTOM_ID_LENGTH


bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)

    if not data:
        raise BadRequestError('Отсутствует тело запроса')

    if 'url' not in data:
        raise BadRequestError('"url" является обязательным полем!')

    custom_id = data.get('custom_id')

    if custom_id:
        if not is_valid_short_id(custom_id):
            raise BadRequestError(
                'Указано недопустимое имя для короткой ссылки')

        if (
            custom_id == 'files'
            or URLMap.query.filter_by(short=custom_id).first()
        ):
            raise BadRequestError(
                'Предложенный вариант короткой ссылки уже существует.')
    else:
        custom_id = get_unique_short_id()

    url_map = URLMap.create_short_link(
        original=data['url'],
        custom_id=custom_id
    )

    return jsonify({
        'url': url_map.original,
        'short_link': url_for(
            'views.redirect_view',
            short_id=url_map.short,
            _external=True
        )
    }), 201


@bp.route('/id/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    url_map = URLMap.get_by_short(short_id)

    if url_map is None:
        raise NotFoundError('Указанный id не найден')

    return jsonify({'url': url_map.original}), 200
