from pathlib import Path
from shutil import move
from tempfile import mkstemp


class DotEnv:
    def __init__(self, base_dir=Path().cwd().parent, env_file='.env'):
        self.base_dir = base_dir
        self.env_file = env_file
        self.path = Path(base_dir / env_file)
        if not self.path.exists():
            self.path.touch()

    def exist_in_file(self, key=str()):
        with open(self.path, 'r') as file:
            for line in file:
                name, value = line.split('=', 1)
                if name == key:
                    print(f'Found "{key}"')
                    return True
        return False

    def is_set_in_file(self, key=str()):
        with open(self.path, 'r') as file:
            for line in file:
                name, value = line.split('=', 1)
                if value:
                    print(f'Found "{key}", with value: "{value}"')
                    return True
        return False

    def replace_environment_variable(self, key=str(), value=str()):
        temp_file, abs_path = mkstemp()
        with open(temp_file, 'w') as new_file:
            with open(self.path, 'r') as old_file:
                for line in old_file:
                    name, data = line.split('=', 1)
                    if name == key:
                        new_file.write(f'{key}={value}')
                    else:
                        new_file.write(f'{name}={data}')
        tmp_path = Path(abs_path)
        move(tmp_path, self.path)

    def save_environment_variable(self, key=str(), value=str()):
        with open(self.path, 'a') as file:
            file.write(f'\n{key}={{{{{value}}}}}')

    def set_environment_variable(self, key=str(), value=str()):
        if self.exist_in_file(key):
            self.replace_environment_variable(key, value)
        else:
            self.save_environment_variable(key, value)
            pass
        pass

