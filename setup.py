#!/usr/bin/env python
from os.path import dirname, abspath, join
from setuptools import setup

here = abspath(dirname(__file__))
readme = open(join(here, "README.rst"))

setup(
    name="mls",
    version="1.2.1",
    py_modules=["mls"],
    url="https://github.com/rembish/mls",
    license="BSD",
    author="Aleksey Rembish",
    author_email="alex@rembish.org",
    description="MultiLingualString",
    long_description="".join(readme.readlines()),
    test_suite="tests",
    install_requires=["six"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Internationalization",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ]
)
