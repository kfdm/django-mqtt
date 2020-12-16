"""
MQTT tools for Django
"""

from setuptools import find_packages, setup

readme_file = open("README.md", "rt").read()

setup(
    name="django-mqtt",
    author="Paul Traylor",
    packages=find_packages(exclude=["test"]),
    version="0.0.1",
    license="MIT License",
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
    description=" ".join(__doc__.splitlines()).strip(),
    long_description=readme_file,
    long_description_content_type="text/markdown",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP",
    ],
)
