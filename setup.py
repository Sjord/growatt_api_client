from setuptools import setup

requirements = ["requests"]
try:
    import enum
except:
    requirements += ["enum34"]

setup(
    name="growatt",
    version="0.0.2",
    description="Growatt API for photovoltaic statistics",
    url="https://github.com/Sjord/growatt_api_client",
    author="Sjoerd Langkemper",
    packages=["growatt"],
    install_requires=requirements,
    license="OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
)
