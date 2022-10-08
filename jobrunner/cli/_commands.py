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
    Run setup scripts in a directory
    \b

    \b
    Jobfiles in a directory tree provide a list of
    setup scripts which are composed into a job.setup
    file and executed in the directories defined in
    WORKDIR_LIST. A job.setup file is created as
    a result of this command
    \b

    \b
    Environment variables
    ----------------------------------------------------
    JOB_WORKDIR - Path to working directory, can be used
                  for reference in bash scripts
    \b
    JOB_TREEDIR - Path to local tree directory, can be used
                  to reference directory containing a bash
                  script
    \b
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

        # Build main dictionary
        print(f"Parsing Jobfiles in directory tree")
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


@jobrunner.command(name="submit")
@click.argument("workdir_list", required=True, nargs=-1, type=str)
def submit(workdir_list):
    """
    \b
    Submit a job from a directory
    \b

    \b
    Jobfiles in a directory tree provide a list of
    submit scripts which are composed into a job.submit
    file and executed in the directories defined in
    WORKDIR_LIST. A job.submit file is created as
    a result of this command
    \b

    \b
    Environment variables
    ----------------------------------------------------
    JOB_WORKDIR - Path to working directory, can be used
                  for reference in bash scripts
    \b
    JOB_TREEDIR - Path to local tree directory, can be used
                  to reference directory containing a bash
                  script
    \b
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

        # Build main dictionary
        print(f"Parsing Jobfiles in directory tree")
        main_dict = lib.ParseJobToml(basedir, workdir)

        # Build inputfile
        print(f"Creating input file: job.input")
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
    Remove artifacts from a directory
    \b

    \b
    This command removes job.input, job.setup, and
    job.submit files in working directories provided
    in WORKDIR_LIST
    \b
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


@jobrunner.command(name="archive")
@click.option("--tag", "-t", help="name of the archive", required=True, type=str)
@click.argument("workdir_list", required=True, nargs=-1, type=str)
def archive(tag, workdir_list):
    """
    \b
    Create an archive along a directory tree
    \b
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

        # Build main dictionary
        print(f"Parsing Jobfile configuration")
        main_dict = lib.ParseJobToml(basedir, workdir)

        # Create archive
        print(f"Creating archive tag: {tag}")
        lib.CreateArchive(main_dict, tag)

        # Return to base directory
        os.chdir(basedir)
