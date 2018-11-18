Installation
====================================

Messages is **Python 3.5+ ONLY!**

Simply install by:

``$ pip install messages``

**Or**

``$ pip3 install messages``

Notes
---------------

The following are notes that may be pertinent to your understanding of various installation dependencies.

* `jsonconfig <https://github.com/json-transformations/jsonconfig>`_ is a package written to make reading/writing configuration files easy. This package will be used to save user-defined parameters and account information to make sending messages easier since fewer arguments will need to be provided for message creation. All credentials, such as passwords, API keys, etc. are encrypted via your system's resident *keyring* backend, with **Linux** default to `SecretStorage <https://github.com/mitya57/secretstorage>`_.