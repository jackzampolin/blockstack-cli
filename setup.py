from setuptools import setup 

setup(
    name="blockstack-cli",
    version="0.1",
    py_modules=['cli'],
    install_requires=[
        'Click',
        'blockstack',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        blockstack-cli=cli:cli
    ''',
)