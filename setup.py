from setuptools import setup

requirements = ["requests"]
try:
    import enum
except:
    requirements += ["enum34"]

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='Growatt API',
    description='A package to query the growatt server',
    version='0.0.3',
    author=['Sjoerd Langkemper', 'Tim van Cann'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/timvancann/growatt_api_client",
    license="OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
    packages=['growatt_api'],
    install_requires=requirements,
    extras_require={
        'tests': [
            'pytest==4.1.1',
            'requests-mock==1.5.2'
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Programming Language :: Python",
    ],
)
