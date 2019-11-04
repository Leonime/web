from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


def validate_url(value):
    if not value:
        raise ValidationError('Missing url')

    try:
        validate = URLValidator()

        scheme = value.split('://')[0].lower()
        if scheme not in validate.schemes:
            value = f'http://{value}'

        validate(value)
    except ValidationError:
        raise ValidationError('Invalid URL for this field')

    return value
