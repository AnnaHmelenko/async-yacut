from flask import Blueprint, jsonify, request, url_for

from yacut.models import URLMap
from yacut.utils import get_unique_short_id, is_valid_short_id

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({'message': 'Отсутствует тело запроса'}), 400

    if 'url' not in data:
        return jsonify({'message': '"url" является обязательным полем!'}), 400

    custom_id = data.get('custom_id')

    try:
        if custom_id:
            if not is_valid_short_id(custom_id):
                return jsonify(
                    {'message': 'Указано недопустимое имя для короткой ссылки'
                     }), 400

            if URLMap.query.filter_by(short=custom_id).first():
                return jsonify(
                    {'message':
                        'Предложенный вариант короткой ссылки уже существует.'
                     }), 400
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
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@bp.route('/id/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()

    if url_map is None:
        return jsonify({'message': 'Указанный id не найден'}), 404

    return jsonify({'url': url_map.original}), 200
