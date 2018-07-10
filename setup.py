from setuptools import setup

setup(
    name = 'multiget',
    version = '1.0.0',
    packages = ['multiget'],
    entry_points = {
        'console_scripts': [
            'multiget = multiget.__main__:main'
        ]
    })
