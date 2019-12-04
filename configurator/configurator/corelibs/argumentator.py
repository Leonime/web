import argparse

from configurator import version


class ArgumentHandler:
    def __init__(self, parser=None):
        self.parser = parser
        pass

    def args_builder(self):
        if self.parser is None:
            self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-d', '--default', help='Configure everything with default values.',
                                 action='store_true')
        self.parser.add_argument('-i', '--interactive', help='You will be asked what to do', action='store_true')
        self.parser.add_argument('-v', '--verbosity', help='Increases output information', action='store_true')
        self.parser.add_argument('-p', '--path', help='Changes path where the secrets folder will be created', type=str)
        self.parser.add_argument('-f', '--folder', help='Change secrets folder name, default is secrets', type=str)
        self.parser.add_argument('--version', action='version', version=f'%(prog)s {version}',
                                 help='show the version number and exit')
        return self.parser
