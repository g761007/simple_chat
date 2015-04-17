import os

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

extra = {}
try:
    from simple_chat.scripts.setup_cmd import *
    extra['cmdclass'] = {
        'runapp': RunServerCommand,
        'initdb': InitDBCommand,
    }
except ImportError:
    pass

here = os.path.abspath(os.path.dirname(__file__))

def read_requirements(filename):
    content = open(os.path.join(here, filename)).read()
    requirements = map(lambda r: r.strip(), content.splitlines())
    return requirements

requirements = read_requirements('requirements.txt')
test_requirements = read_requirements('test-requirements.txt')

setup(
    name='simple_chat',
    version='0.0.0',
    author="Daniel Hsieh",
    packages=find_packages(),
    install_requires=requirements,
    tests_require=test_requirements,
    **extra
)