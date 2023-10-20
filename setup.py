"""Setup script for publishing package to PyPI"""

import setuptools

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="double-pendula",
    version="0.1.1",
    author="Chris Greening",
    author_email="chris@christophergreening.com",
    description="Library for animating double pendula in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chris-greening/double-pendula",
    packages=setuptools.find_packages(),
    install_requires=["numpy", "pandas", "scipy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
