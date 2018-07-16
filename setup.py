from setuptools import setup, find_packages

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
