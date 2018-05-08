import ast
import os
import re
import sys
from setuptools import setup, find_packages


# get __version__ from __init__.py
_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open('messages/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


# load README.rst
with open('README.rst', 'r', encoding='utf-8') as f:
    readme = f.read()


setup(
    name='messages',
    version=version,
    url='https://github.com/trp07/messages',
    keywords=['message', 'messages', 'email', 'text', 'SMS', 'MMS',
              'chat', 'chats', 'slack', 'twilio', 'async', 'asynchronous'],

    author='Tim Phillips',
    author_email='phillipstr@gmail.com',

    description=('A package designed to make sending messages '
                 'easy and efficient!'),
    long_description=readme,

    packages=find_packages(include=['messages']),
    include_package_data=True,
    zipsafe=False,

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ],

    python_requires='>=3.5',

    install_requires=[
        'click>=6.0',
        'requests',
        'jsonconfig-tool',
        'twilio',
        'validus',
    ],

    test_suite='tests',
    test_requires=[
        'pytest-cov',
        'flake8',
        'tox',
    ],

    setup_requires=['pytest-runner'],

    entry_points={
        'console_scripts': ['messages=messages.cli:main']
    },

)
