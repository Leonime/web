from setuptools import setup

import configurator

setup(
    name='configurator',
    version=configurator.version,
    packages=['configurator', 'configurator.corelibs'],
    package_dir={'': './'},
    url='https://github.com/Leonime/codeshepherds',
    license='MIT',
    author='Leopoldo Parra',
    author_email='lparra.dev@gmail.com',
    description='An application to configure docker.',
    entry_points={
        'console_scripts': [
            'configurator = configurator.app:main',
        ],
    },
    install_requires=['colorama', 'docker']
)
