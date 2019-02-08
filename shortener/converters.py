from codeshepherds import settings

SHORT_CODE_MAX = getattr(settings, "SHORT_CODE_MAX", 16)
SHORT_CODE_MIN = getattr(settings, "SHORT_CODE_MIN", 8)


class ShortCodeConverter:
    regex = f'[a-zA-z0-9]{{{SHORT_CODE_MIN},{SHORT_CODE_MAX}}}'

    def to_python(self, value):
        return f'{value}'

    def to_url(self, value):
        return f'{value}'
