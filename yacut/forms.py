from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, URL

from yacut.constants import MAX_CUSTOM_ID_LENGTH


class URLForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            URL(message='Введите корректный URL')
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(
                max=MAX_CUSTOM_ID_LENGTH,
                message=(
                    f'Короткая ссылка не должна превышать '
                    f'{MAX_CUSTOM_ID_LENGTH} символов'
                )
            )
        ]
    )
    submit = SubmitField('Создать')


class FileUploadForm(FlaskForm):
    files = FileField(
        'Файлы',
        validators=[
            FileRequired(message='Выберите хотя бы один файл'),
            FileAllowed(
                [
                    'txt', 'pdf', 'png', 'jpg', 'jpeg',
                    'doc', 'docx', 'xls', 'xlsx', 'zip'
                ],
                message='Недопустимый формат файла'
            )
        ]
    )
    submit = SubmitField('Загрузить')
