import argparse

from configurator.corelibs.argumentator import ArgumentHandler
from configurator.corelibs.secrets import SecretsFolder, Secrets


def main():
    parser = argparse.ArgumentParser()
    argumentator = ArgumentHandler(parser=parser)
    parser = argumentator.args_builder()
    args = parser.parse_args()

    interactive = bool(args.interactive)
    verbosity = bool(args.verbosity)

    # password = get_input(confirmation=True, msg='Are you sure? ')

    secret_folder = SecretsFolder(interactive, verbosity)
    secrets_dir = secret_folder.set_secrets_folder(args)

    if args.default and args.interactive:
        print('You can\'t use -i and -d at the same time.')
    elif args.default:
        print(f'Files will be stored in: {secrets_dir}')
        if not secrets_dir.exists():
            secrets_dir.mkdir()
            pass
        secrets = Secrets(interactive, verbosity)
        secrets.create_default()


if __name__ == '__main__':
    main()
