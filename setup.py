"""Setup script for PyDuckDB."""
import setuptools
from pyduckdb import __version__

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name="pyduckdb",
    version=__version__,
    author="Travis Hesketh",
    author_email="travis@hesketh.scot",
    description="A wrapper around DuckDB to add some convenience.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 4 - Beta",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Typing :: Typed",
    ],
    python_requires=">=3.7",
    install_requires=[
        "duckdb==0.2.5",
        "pep249>=0.0.1b3"
    ]
)
