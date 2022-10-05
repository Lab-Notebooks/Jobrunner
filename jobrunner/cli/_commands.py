# Standard libraries
import os
import subprocess

# Feature libraries
import toml
import click

from . import jobrunner
from .. import lib


@jobrunner.command(name="submit")
@click.argument("workdir_list", default=None, nargs=-1, type=str)
def submit(workdir_list):
    """
    Command to submit a job from a working directory
    """
    # Get base directory
    basedir = os.getcwd()

    # loop over workdir_list
    for workdir in workdir_list:

        # chdir to working directory
        print(f"-------------------------------------------------------------")
        os.chdir(workdir)
        workdir = os.getcwd()
        print(f"Working directory: {workdir}")

        # Build `job` dictionary
        print(f"Parsing job configuration and running config scripts")
        main_dict = lib.ParseJobToml(basedir, workdir)
        # config scripts
        lib.RunConfigScripts(main_dict)

        # Build inputfile
        print(f'Creating job input file: {main_dict["job"]["input"]}')
        lib.CreateInputFile(main_dict)

        # Build jobfile
        print(f"Creating job file: job.sh")
        lib.CreateJobFile(main_dict)

        # Submit job
        print(f"Submitting job")
        subprocess.run(
            f'{main_dict["job"]["schedular"]} job.sh', shell=True, check=True
        )

        # Return to base directory
        os.chdir(basedir)


@jobrunner.command(name="clean")
@click.argument("workdir_list", default=None, nargs=-1, type=str)
def clean(workdir_list):
    """
    Command to clean artifacts from working directory
    """
    # Get base directory
    basedir = os.getcwd()

    # run cleanup
    for workdir in workdir_list:

        main_dict = lib.ParseJobToml(basedir, workdir)

        process = subprocess.run(
            f'rm -vf {workdir + "/" + main_dict["job"]["input"]} {workdir + "/" + "job.sh"}',
            shell=True,
            check=True,
        )
