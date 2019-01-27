from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='Growatt API',
    description='A package to query the growatt server',
    version='0.0.1',
    author=['Sjord', 'Tim van Cann'],
    author_email="timvancann@gmail.com",
    long_description=long_description,
    packages=['growatt_api'],
    install_requires=[
        'requests==2.21.0'
    ],
    extras_require={
        'tests': [
            'pytest==4.1.1',
            'requests-mock==1.5.2'
        ]
    },
)
