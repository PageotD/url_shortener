"""
Setup script for the shortener_app package.

This script uses setuptools to package the application and manage its dependencies.
It includes metadata about the package and specifies the packages and dependencies 
to be included. This script is necessary for installing the package and its dependencies 
using pip.

To install the package, run:
    pip install -e .

To include dependencies from requirements.txt, use the parse_requirements function.
"""

from setuptools import setup, find_packages

def parse_requirements(filename):
    """
    Parse a requirements file into a list of dependencies.
    
    Args:
        filename (str): The path to the requirements file.
        
    Returns:
        list: A list of dependencies.
    """
    with open(filename, "r") as f:
        return f.read().splitlines()

setup(
    name="shortener-app",
    version="0.1.2",
    description="A URL shortener application",
    author="Damien Pageot",
    #author_email="your.email@example.com",
    url="https://github.com/PageotD/url_shortener",
    packages=find_packages(where="sources"),
    package_dir={"": "sources"},
    install_requires=parse_requirements("requirements.txt"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
