from flask import Blueprint, jsonify, request, url_for

from yacut.models import URLMap
from yacut.exceptions import APIError


bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)

    if not data:
        raise APIError('Отсутствует тело запроса', 400)

    if 'url' not in data:
        raise APIError('"url" является обязательным полем!', 400)

    custom_id = data.get('custom_id')

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
        raise APIError('Указанный id не найден', 404)

    return jsonify({'url': url_map.original}), 200
