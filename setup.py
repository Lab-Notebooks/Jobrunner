"""Build and installation script for jobrunner."""

# standard libraries
import os
import sys
import re
from setuptools import setup, find_packages

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import bin from current working directory
# sys.path.insert makes sure that current file path is searched
# first to find this module
import bin.cmd as bin_cmd  # pylint: disable=wrong-import-position

# get long description from README.rst
with open("README.rst", mode="r") as readme:
    long_description = readme.read()

# get package metadata by parsing __meta__ module
with open("jobrunner/__meta__.py", mode="r") as source:
    content = source.read().strip()
    metadata = {
        key: re.search(key + r'\s*=\s*[\'"]([^\'"]*)[\'"]', content).group(1)
        for key in [
            "__pkgname__",
            "__version__",
            "__authors__",
            "__license__",
            "__description__",
        ]
    }

# core dependancies
DEPENDENCIES = ["click", "toml", "pyyaml", "alive-progress==3.1.4"]

# core dependancies for the package
with open("requirements/core.txt", mode="r", encoding="ascii") as core_reqs:
    DEPENDENCIES = core_reqs.read()


setup(
    name=metadata["__pkgname__"],
    version=metadata["__version__"],
    author=metadata["__authors__"],
    description=metadata["__description__"],
    license=metadata["__license__"],
    packages=find_packages(where="./"),
    package_dir={"": "./"},
    scripts=[
        "jobrunner/scripts/jobrunner",
        "jobrunner/scripts/logdiff",
        "jobrunner/scripts/catlog",
        "jobrunner/scripts/catloglast",
    ],
    package_data={
        "": [
            "options.py",
        ]
    },
    include_package_data=True,
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
    ],
    install_requires=DEPENDENCIES,
    cmdclass={
        "develop": bin_cmd.DevelopCmd,
        "install": bin_cmd.InstallCmd,
    },
)
