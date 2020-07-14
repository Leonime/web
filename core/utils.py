import base64
import json
import logging
import os
from pathlib import Path

from cryptography.fernet import InvalidToken, Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.contrib import messages
from django.shortcuts import redirect, render
from django.template.loader import get_template
from django.urls import reverse
from rest_framework import status

from core.send_mail import SendEmail


def create_encryptor():
    crypt_key = os.environ.get('CRYPT_KEY')
    password = str.encode(crypt_key)
    crypt_salt = str(os.environ.get('CRYPT_SALT'))
    salt = str.encode(crypt_salt)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return Fernet(key)


def save_config_file(config_file='development.json',
                     name='codeshepherds',
                     user='leonime',
                     password='nomas123',
                     host='localhost',
                     port=''):
    base_dir = os.environ.get('CODESHEPHERDS_BASE_DIR')
    path = Path(base_dir).joinpath(config_file)
    f = create_encryptor()

    json_data = {'DB': {}}

    json_data['DB']['NAME'] = f.encrypt(str.encode(name)).decode('utf-8')
    json_data['DB']['USER'] = f.encrypt(str.encode(user)).decode('utf-8')
    json_data['DB']['PASSWORD'] = f.encrypt(str.encode(password)).decode('utf-8')
    json_data['DB']['HOST'] = f.encrypt(str.encode(host)).decode('utf-8')
    json_data['DB']['PORT'] = f.encrypt(str.encode(port)).decode('utf-8')

    with path.open('w') as file:
        json.dump(json_data, file, sort_keys=True, indent=4)


def load_config_file():
    config_file = os.environ.get('CONFIG_FILE')
    base_dir = os.environ.get('CODESHEPHERDS_BASE_DIR')
    path = Path(base_dir).joinpath(config_file)

    if path.exists():
        with path.open() as cfg:
            config = json.load(cfg)
    else:
        save_config_file(config_file, 'codeshepherds', 'leonime', 'nomas123', 'localhost', '')
        config = load_config_file()
    return config


def load_config(base_dir=None):
    f = create_encryptor()
    config = {
        'DB': {
            'NAME': os.environ.get("SQL_DATABASE",
                                   f.encrypt(str.encode(os.path.join(base_dir, "db.sqlite3"))).decode('utf-8')),
            'USER': os.environ.get('SQL_USER'),
            'PASSWORD': os.environ.get('SQL_PASSWORD'),
            'HOST': os.environ.get('SQL_HOST'),
            'PORT': os.environ.get('SQL_PORT'),
            'ENGINE': os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        }
    }
    return config


def load_db_config(base_dir=None):
    load_from_environment = bool(os.environ.get('LOAD_FROM_ENVIRONMENT', True))
    if load_from_environment:
        config = load_config(base_dir)
    else:
        config = load_config_file()
    f = create_encryptor()

    try:
        config = {
            key: {
                key: f.decrypt(str(value).encode('utf-8')).decode('utf-8')
                for key, value in value.items()
            }
            for key, value in config.items()
        }
    except InvalidToken:
        raise InvalidToken

    return config


def get_boolean(value):
    is_boolean = True if isinstance(value, bool) else False
    is_int = False
    try:
        value = int(value)
    except ValueError:
        is_int = False
    if is_boolean:
        return value
    elif isinstance(value, str) and is_int is False:
        return True if value.lower() == 'true' else False
    elif isinstance(value, int):
        return bool(value) if 1 >= value >= 0 else False
    else:
        return False


def send_confirmation_email(request, user, user_id, token, context, success_url, resend=False):
    logger = logging.getLogger(__name__)
    url = request.build_absolute_uri(reverse('accounts:confirm_email', kwargs={'user_id': user_id, 'token': token}))
    message = get_template('account/register_email.html').render({
        'confirm_url': url
    })
    kwargs = {
        'from_email': 'no-reply@codeshepherds.com',
        'to_emails': user.email,
        'subject': 'Codeshepherds email confirmation',
        'html_content': message
    }
    email = SendEmail(**kwargs)
    code = email.send()
    if code == status.HTTP_202_ACCEPTED:
        if resend:
            messages.success(request, "Confirmation email send, check your spambox.")
        else:
            messages.success(request, "Please confirm your email.")
        return redirect(success_url)
    else:
        logger.error('Email failed', code)
        messages.error(request, 'Something went wrong please try again.')
        return render(request, 'account/auth.html', context)
