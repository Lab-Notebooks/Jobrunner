# Standard libraries
import os
import subprocess

# Feature libraries
import toml
import click

from . import jobrunner
from .. import lib


@jobrunner.command(name="setup")
@click.argument("workdir_list", default=None, nargs=-1, type=str)
def setup(workdir_list):
    """
    Command to setup a job in working directory
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
        print(f"Parsing job configuration")
        main_dict = lib.ParseJobToml(basedir, workdir)

        # Build setupfile
        print(f"Creating setup file: job_setup.sh")
        lib.CreateSetupFile(main_dict)

        # Run setup
        print(f"Running setup")
        subprocess.run(f"bash job_setup.sh", shell=True, check=True)

        # Return to base directory
        os.chdir(basedir)

    print(f"-------------------------------------------------------------")

    # TODO: Saving this useful piece of code
    # Remove duplicates and sort setup_list
    # setup_list = [*set(setup_list)]
    # setup_list.sort(key=len)


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
        print(f"Parsing job configuration")
        main_dict = lib.ParseJobToml(basedir, workdir)

        # Build inputfile
        print(f'Creating job input file: {main_dict["job"]["input"]}')
        lib.CreateInputFile(main_dict)

        # Build jobfile
        print(f"Creating job file: job_submit.sh")
        lib.CreateJobFile(main_dict)

        # Submit job
        print(f"Submitting job")
        subprocess.run(
            f'{main_dict["job"]["schedular"]} job_submit.sh', shell=True, check=True
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

        if main_dict["job"]["input"]:
            process = subprocess.run(
                f'rm -vf {workdir + "/" + main_dict["job"]["input"]}',
                shell=True,
                check=True,
            )

        process = subprocess.run(
            f'rm -vf {workdir + "/" + "job_submit.sh"}',
            shell=True,
            check=True,
        )

        process = subprocess.run(
            f'rm -vf {workdir + "/" + "job_setup.sh"}',
            shell=True,
            check=True,
        )
