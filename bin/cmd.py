"""Custom commands for BoxKit setup."""
import os
import sys
import subprocess
from setuptools.command.install import install
from setuptools.command.develop import develop

# custom command
class CustomCmd:
    """Custom command."""

    user_options = [
        ("with-instruments", None, "Install additional modules for instruments"),
    ]

    def initialize_options(self):
        """
        Initialize options
        """
        self.with_instruments = None  # pylint: disable=attribute-defined-outside-init

    def finalize_options(self):
        """
        Finalize options
        """
        for option in [
            "with_instruments",
        ]:
            if getattr(self, option) not in [None, 1]:
                raise ValueError(f"{option} is a flag")

    def run(self, user):
        """
        Run command
        """
        if user:
            with_user = "--user"
        else:
            with_user = ""

        if self.with_instruments:
            subprocess.run(
                f"{sys.executable} -m pip install -r requirements/instruments.txt {with_user}",
                shell=True,
                check=True,
                executable="/bin/bash",
            )

        with open("jobrunner/options.py", "w", encoding="ascii") as optfile:

            optfile.write(f"INSTRUMENTS={self.with_instruments}\n")


# replaces the default build command for setup.py
class InstallCmd(install, CustomCmd):
    """Custom build command."""

    user_options = install.user_options + CustomCmd.user_options

    def initialize_options(self):
        install.initialize_options(self)
        CustomCmd.initialize_options(self)

    def finalize_options(self):
        install.finalize_options(self)
        CustomCmd.finalize_options(self)

    def run(self):

        CustomCmd.run(self, self.user)
        install.run(self)


# replaces custom develop command for setup.py
class DevelopCmd(develop, CustomCmd):
    """Custom develop command."""

    user_options = develop.user_options + CustomCmd.user_options

    def initialize_options(self):
        develop.initialize_options(self)
        CustomCmd.initialize_options(self)

    def finalize_options(self):
        develop.finalize_options(self)
        CustomCmd.finalize_options(self)

    def run(self):

        develop.run(self)
        CustomCmd.run(self, self.user)
