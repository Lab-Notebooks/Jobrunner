# Standard libraries
import os
import subprocess

# Feature libraries
import click

from . import jobrunner
from .. import lib


@jobrunner.command(name="setup")
@click.argument("workdir_list", required=True, nargs=-1, type=str)
def setup(workdir_list):
    """
    \b
    Command to run setup scripts in a directory

    \b
    Jobfile(s) in a directory tree provide a list of
    setup scripts which are composed into a job.setup
    file and executed in the directories defined in
    WORKDIR_LIST. A job.setup file is created as
    a result of this command

    \b
    Environment variables
    -------------------------------------------------
    JOB_TARGET_HOME - Path to target working directory
    JOB_FILE_HOME - Path to directory containing a file
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
        print(f"Creating setup file: job.setup")
        lib.CreateSetupFile(main_dict)

        # Run setup
        print(f"Running setup")
        subprocess.run(f"bash job.setup", shell=True, check=True)

        # Return to base directory
        os.chdir(basedir)

    print(f"-------------------------------------------------------------")

    # TODO: Saving this useful piece of code
    # Remove duplicates and sort setup_list
    # setup_list = [*set(setup_list)]
    # setup_list.sort(key=len)


@jobrunner.command(name="submit")
@click.argument("workdir_list", required=True, nargs=-1, type=str)
def submit(workdir_list):
    """
    \b
    Command to submit a job from a directory

    \b
    Jobfile(s) in a directory tree provide a list of
    submit scripts which are composed into a job.submit
    file and executed in the directories defined in
    WORKDIR_LIST. A job.submit file is created as
    a result of this command

    \b
    Environment variables
    -------------------------------------------------
    JOB_TARGET_HOME - Path to target working directory
    JOB_FILE_HOME - Path to directory containing a file

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
        print(f'Creating input file: job.input, basedir: {main_dict["inputdir"]}')
        lib.CreateInputFile(main_dict)

        # Build jobfile
        print(f"Creating submit file: job.submit")
        lib.CreateSubmitFile(main_dict)

        # Submit job
        print(f"Submitting job")
        subprocess.run(
            f'{main_dict["schedular"]["command"]} job.submit', shell=True, check=True
        )

        # Return to base directory
        os.chdir(basedir)


@jobrunner.command(name="clean")
@click.argument("workdir_list", required=True, nargs=-1, type=str)
def clean(workdir_list):
    """
    \b
    Command to clean artifacts in a directory

    \b
    This command removes job.input, job.setup, and
    job.submit files in working directories provided
    in WORKDIR_LIST
    """
    # Get base directory
    basedir = os.getcwd()

    # run cleanup
    for workdir in workdir_list:

        process = subprocess.run(
            f'rm -vf {workdir + "/" + "job.input"}',
            shell=True,
            check=True,
        )

        process = subprocess.run(
            f'rm -vf {workdir + "/" + "job.submit"}',
            shell=True,
            check=True,
        )

        process = subprocess.run(
            f'rm -vf {workdir + "/" + "job.setup"}',
            shell=True,
            check=True,
        )
