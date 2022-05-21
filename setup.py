from distutils.core import setup
from typing import List

try:
    from pip.req import parse_requirements
except ImportError:  # pip >= 10.0.0
    from pip._internal.req import parse_requirements
from setuptools import find_packages

PACKAGE_NAME = "service_base"


def get_requirements(filename: str) -> List[str]:
    """
    Read requirements from 'requirements.txt'
    """
    requirements = parse_requirements(filename, session="hack")
    return [str(requirement.requirement) for requirement in requirements]


def get_version() -> str:
    with open("version", "r") as f:
        return f.read()


setup(
    name=PACKAGE_NAME,
    version=get_version(),
    description="Base abstraction for Services.",
    author="SuperStack, Zilberman Rafael",
    packages=find_packages(include=[PACKAGE_NAME, f"{PACKAGE_NAME}.*"]),
    include_package_data=True,
    install_requires=get_requirements("requirements.txt"),
    tests_require=get_requirements("test-requirements.txt"),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ]
)
