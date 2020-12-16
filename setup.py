from setuptools import find_packages, setup

setup(
    name="django-mqtt",
    author="Paul Traylor",
    packages=find_packages(),
    version="0.0.1",
    license="MIT",
    install_requires=[
        "Django>=2.0",
        "paho-mqtt",
    ],
    url="http://github.com/kfdm/django-mqtt",
    project_urls={
        "Issues": "http://github.com/kfdm/django-mqtt/issues",
        "Source Code": "http://github.com/kfdm/django-mqtt",
    },
    keywords="django mqtt",
)
