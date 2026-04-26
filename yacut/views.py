from flask import Blueprint, flash, redirect, render_template, request, url_for

from yacut import db
from yacut.forms import FileUploadForm, URLForm
from yacut.models import URLMap
from yacut.utils import get_unique_short_id, is_valid_short_id
from yacut.yandex_disk import upload_file_and_get_download_link


bp = Blueprint('views', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()

    if form.validate_on_submit():
        original = form.original_link.data
        custom_id = form.custom_id.data

        if custom_id:
            if not is_valid_short_id(custom_id):
                flash('Указано недопустимое имя для короткой ссылки')
                return render_template('index.html', form=form)

            if custom_id == 'files' or URLMap.query.filter_by(
                    short=custom_id).first():
                flash('Предложенный вариант короткой ссылки уже существует.')
                return render_template('index.html', form=form)

            short = custom_id
        else:
            short = get_unique_short_id()

        url_map = URLMap(
            original=original,
            short=short,
        )

        db.session.add(url_map)
        db.session.commit()

        short_link = url_for(
            'views.redirect_view',
            short_id=short,
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
            short = get_unique_short_id()

            url_map = URLMap(
                original=download_link,
                short=short,
            )

            db.session.add(url_map)
            db.session.commit()

            short_link = url_for(
                'views.redirect_view',
                short_id=short,
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
