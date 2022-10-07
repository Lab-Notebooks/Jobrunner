# Standard libraries
import os
import subprocess

# Feature libraries
import toml

# local imports
from . import GetFileList


def CreateSetupFile(main_dict):
    """
    create a setup script

    `main_dict` : job dictionary
    """
    # set header for the setup script
    with open(main_dict["workdir"] + os.sep + "job.setup", "w") as setupfile:

        # write the header
        setupfile.write("#!/bin/bash\n")

        # set environment variable
        # to working directory
        setupfile.write(f'\nexport JOB_TARGET_HOME="{main_dict["workdir"]}"')

        # add commands to source run scripts
        for entry in main_dict["config"]["setup"]:
            setupfile.write(f'\n\nexport JOB_FILE_HOME="{os.path.dirname(entry)}"')
            setupfile.write(f"\nsource {entry}")

        # Add an extra space
        setupfile.write("\n")


def CreateInputFile(main_dict):
    """
    create an input file for a given simulation recursively using
    `job.input` between `basedir` and `workdir`

    `main_dict` : job dictionary
    """
    # get inputfile_list from internal method
    inputfile_list = GetFileList(
        main_dict["inputdir"], main_dict["workdir"], main_dict["config"]["input"]
    )

    # run a subprocess to build flash.par
    process = subprocess.run(
        f"rm -f job.input &&" + " " + f'cat {" ".join(inputfile_list)} > job.input',
        shell=True,
        check=True,
    )


def CreateSubmitFile(main_dict):
    """
    create `job.run` for a given simulation recursively using configuration
    `job` dictionary

    `main_dict`       :  Job dictionary
    """
    # set header for the submit script
    with open(main_dict["workdir"] + os.sep + "job.submit", "w") as jobfile:

        # write the header
        jobfile.write("#!/bin/bash\n")

        # add schedular commands
        for entry in main_dict["schedular"]["options"]:
            jobfile.write(f"\n{entry}")

        # set environment variable
        # to working directory
        jobfile.write(f'\n\nexport JOB_TARGET_HOME="{main_dict["workdir"]}"')

        # add commands to source run scripts
        for entry in main_dict["config"]["submit"]:
            jobfile.write(f'\n\nexport JOB_FILE_HOME="{os.path.dirname(entry)}"')
            jobfile.write(f"\nsource {entry}")

        # source `job.sh`
        if os.path.exists(main_dict["config"]["target"]):
            jobfile.write(f'\n\nsource {main_dict["config"]["target"]}')
        else:
            raise ValueError(
                f'[jobrunner] {main_dict["config"]["target"]} not present in path'
            )

        # add an extra space
        jobfile.write("\n")
