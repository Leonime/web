from pathlib import Path

version_info = (0, 0, 1)
version = '.'.join(str(c) for c in version_info)

BASE_DIR = Path.cwd().parent
ENV_SECRETS_DIR = 'secrets'
