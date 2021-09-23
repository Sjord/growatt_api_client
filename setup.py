#!/usr/bin/env python

from setuptools import setup

requirements = ["requests"]
try:
    import enum
except:
    requirements += ["enum34"]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="growatt",
    version="0.0.4",
    description="Growatt API for photovoltaic statistics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sjord/growatt_api_client",
    author="Sjoerd Langkemper",
    packages=["growatt"],
    install_requires=requirements,
    license="OSI Approved :: MIT License",
    test_suite="test",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
    ],
)
