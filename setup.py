from setuptools import find_packages, setup

setup(
    name="django-mqtt",
    author="Paul Traylor",
    url="http://github.com/kfdm/django-mqtt",
    install_requires=[
        "Django>-2.0",
        "paho-mqtt",
    ],
)
