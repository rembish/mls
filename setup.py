#!/usr/bin/env python
from os.path import dirname, abspath, join
from setuptools import setup

here = abspath(dirname(__file__))
readme = open(join(here, "README.rst"))

setup(
    name="mls",
    version="1.1.0",
    py_modules=["mls"],
    url="https://github.com/rembish/mls",
    license="BSD",
    author="Aleksey Rembish",
    author_email="alex@rembish.org",
    description="MultiLingualString",
    long_description="".join(readme.readlines()),
    test_suite="tests",
    install_requires=["six"]
)
