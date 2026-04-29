from flask import Blueprint, flash, redirect, render_template, request, url_for

from yacut import db
from yacut.forms import FileUploadForm, URLForm
from yacut.models import URLMap
from yacut.yandex_disk import upload_file_and_get_download_link
from yacut.exceptions import BadRequestError


bp = Blueprint('views', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()

    if form.validate_on_submit():
        original = form.original_link.data
        custom_id = form.custom_id.data

        # Проверка на зарезервированное имя 'files'
        if custom_id and custom_id == 'files':
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)

        try:
            url_map = URLMap.create_short_link(
                original=original,
                custom_id=custom_id if custom_id else None
            )
        except BadRequestError as e:
            flash(str(e))
            return render_template('index.html', form=form)

        short_link = url_for(
            'views.redirect_view',
            short_id=url_map.short,
            _external=True
        )

        return render_template(
            'index.html',
            form=form,
            short_link=short_link
        )

    return render_template('index.html', form=form)


@bp.route('/files', methods=['GET', 'POST'])
async def files_view():
    form = FileUploadForm()
    uploaded_files = []

    if form.validate_on_submit():
        files = request.files.getlist('files')

        for file in files:
            download_link = await upload_file_and_get_download_link(file)

            try:
                url_map = URLMap.create_short_link(
                    original=download_link,
                    custom_id=None
                )
            except BadRequestError as e:
                flash(str(e))
                continue

            short_link = url_for(
                'views.redirect_view',
                short_id=url_map.short,
                _external=True
            )

            uploaded_files.append({
                'filename': file.filename,
                'short_link': short_link
            })

    return render_template(
        'files.html',
        form=form,
        uploaded_files=uploaded_files
    )


@bp.route('/<short_id>')
def redirect_view(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original)
