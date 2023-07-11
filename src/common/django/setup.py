from setuptools import setup, find_packages

setup(
    name='shared',
    version='0.0.1',
    description='common library for django services.',
    author='Jay ',
    author_email='jaykishan@playcent.com',
    packages=find_packages(),
    python_requires='>=3.9',
    install_requires=[
        'Django>=4.1',
        'confluent-kafka>=2.1.1'
    ],
)