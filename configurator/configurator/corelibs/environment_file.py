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
                if line and line.strip():
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

    def replace_environment_variable(self, key=str(), value=str(), secret=True):
        temp_file, abs_path = mkstemp()
        with open(temp_file, 'w') as new_file:
            with open(self.path, 'r') as old_file:
                for line in old_file:
                    if line and line.strip():
                        name, data = line.split('=', 1)
                        if name == key:
                            if secret:
                                new_file.write(f'{key}={{{{DOCKER_SECRET:{value}}}}}\n')
                            else:
                                new_file.write(f'{key}={value}\n')
                        else:
                            new_file.write(f'{name}={data}')
                    else:
                        new_file.write(line)
        tmp_path = Path(abs_path)
        move(tmp_path, self.path)

    def save_environment_variable(self, key=str(), value=str(), secret=True):
        with open(self.path, 'a') as file:
            if secret:
                file.write(f'{key}={{{{DOCKER_SECRET:{value}}}}}\n')
            else:
                file.write(f'{key}={value}\n')

    def save_blank_line(self):
        with open(self.path, 'a') as file:
            file.write(f'\n')

    def set_environment_variable(self, key=str(), value=str(), secret=True):
        if self.exist_in_file(key):
            self.replace_environment_variable(key, value, secret)
        else:
            self.save_environment_variable(key, value, secret)
            pass
        pass

