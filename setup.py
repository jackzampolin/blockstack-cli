from setuptools import setup 

setup(
    name="blockstack-cli",
    version="0.1",
    py_modules=['cli'],
    install_requires=[
        'Click',
        'requests',
        'toml',
        'json',
        'yaml',
    ],
    entry_points='''
        [console_scripts]
        blockstack-cli=cli:cli
    ''',
)