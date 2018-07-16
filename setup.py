import sys
from setuptools import setup, find_packages

# immediately bail for incorrect python
if sys.version_info[:2] != (2, 7):
    raise RuntimeError("Multiget requires python == 2.7")

setup(
    name = 'multiget',
    version = '1.0.0',
    packages = find_packages(),
    install_requires=[
        'click',
        'validators',
        'requests'
        ],
    include_package_data=True,
    entry_points = {
        'console_scripts': [
            'multiget = multiget.__main__:cli'
        ]
    }
)
