import os
from setuptools import setup, find_packages

package = "src"

def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]

setup(
    name='shared',
    version='0.0.1',
    description='common library for django services.',
    author='Jay ',
    author_email='jaykishan@playcent.com',
    packages=find_packages(),
    install_requires=[
        'Django>=4.1',
        'confluent-kafka>=2.1.1'
    ],
)
