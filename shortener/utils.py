import random
import string
from django.conf import settings

SHORT_CODE_MIN = getattr(settings, "SHORT_CODE_MIN", 6)


def code_generator(size=SHORT_CODE_MIN, char=string.ascii_letters + string.digits):
    return ''.join(random.SystemRandom().choice(char) for _ in range(size))


def create_short_code(instance, size=SHORT_CODE_MIN):
    new_code = code_generator(size=size)
    obj = instance.__class__
    qs_exists = obj.objects.filter(short_code=new_code).exists()
    if qs_exists:
        return create_short_code(instance, size=size)
    return new_code
