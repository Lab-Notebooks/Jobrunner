# Standard libraries
import os
import sys
import subprocess
from datetime import date

# Feature libraries
import click

from . import jobrunner
from .. import lib


@jobrunner.command(name="setup")
@click.argument("workdir_list", required=True, nargs=-1, type=str)
@click.option("--show", is_flag=True, help="only show configuration details")
def setup(workdir_list, show):
    """
    \b
    Run setup scripts in a directory
    \b

    \b
    Jobfiles in a directory tree provide a list of
    setup scripts which are composed into a job.setup
    file and run along the directory tree
    \b

    \b
    Bash Variables
    --------------
    JobWorkDir - Path to working directory of the job
    """
    # Get base directory
    basedir = os.getcwd()

    # loop over workdir_list
    for workdir in workdir_list:

        # chdir to working directory
        print(
            f"[jobrunner]-------------------------------------------------------------"
        )
        os.chdir(workdir)
        workdir = os.getcwd()
        print(f"[jobrunner] Working directory: {workdir}")

        # Build main dictionary
        print(f"[jobrunner] Parsing Jobfiles in directory tree")
        main_dict = lib.ParseJobToml(basedir, workdir)

        if show:
            # Print configuration details
            print(f"[jobrunner] ---- Parsed Configuration ----")
            print(f"[jobrunner] job.setup: [")
            for value in main_dict["job"]["setup"]:
                print(f"[jobrunner] \t{value}")
            print(f"[jobrunner] \t]")

        else:
            # Build setupfile
            print(f"[jobrunner] Creating setup file: job.setup")
            lib.CreateSetupFile(main_dict)

            # Run setup
            print(f"[jobrunner] Running setup")
            subprocess.run(f"bash job.setup", shell=True, check=True)

        # Return to base directory
        os.chdir(basedir)

    print(f"[jobrunner]-------------------------------------------------------------")


@jobrunner.command(name="submit")
@click.argument("workdir_list", required=True, nargs=-1, type=str)
@click.option("--show", is_flag=True, help="only show configuration details")
def submit(workdir_list, show):
    """
    \b
    Submit a job from a directory
    \b

    \b
    Jobfiles in a directory tree provide a list of
    submit scripts which are composed into a job.submit
    file for linux schedulars
    \b

    \b
    Bash Variables
    --------------
    JobWorkDir - Path to working directory of the job
    """
    # Get base directory
    basedir = os.getcwd()

    # loop over workdir_list
    for workdir in workdir_list:

        # chdir to working directory
        print(f"-------------------------------------------------------------")
        os.chdir(workdir)
        workdir = os.getcwd()
        print(f"[jobrunner] Working directory: {workdir}")

        # Build main dictionary
        print(f"[jobrunner] Parsing Jobfiles in directory tree")
        main_dict = lib.ParseJobToml(basedir, workdir)

        if show:
            # Print configuration details
            print(f"[jobrunner] ---- Parsed Configuration ----")
            print(f"[jobrunner] job.input: [")
            for value in main_dict["job"]["input"]:
                print(f"[jobrunner] \t{value}")
            print(f"[jobrunner] \t]")
            print(f"[jobrunner] job.target:")
            print(f'[jobrunner] \t{main_dict["job"]["target"]}')
            print(f"[jobrunner] job.submit: [")
            for value in main_dict["job"]["submit"]:
                print(f"[jobrunner] \t{value}")
            print(f"[jobrunner] \t]")

        else:
            # Build inputfile
            print(f"[jobrunner] Creating input file: job.input")
            lib.CreateInputFile(main_dict)

            # Build targetfile
            print(f"[jobrunner] Creating target file: job.target")
            lib.CreateTargetFile(main_dict)

            # Build submitfile
            print(f"[jobrunner] Creating submit file: job.submit")
            lib.CreateSubmitFile(main_dict)

            # Submit job
            print(f"[jobrunner] Submitting job")
            subprocess.run(
                f'{main_dict["schedular"]["command"]} job.submit',
                shell=True,
                check=True,
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
    This command removes job.input, job.target,
    job.setup, and job.submit files from a
    working directory
    \b
    """
    # Get base directory
    basedir = os.getcwd()

    print(f"[jobrunner] Cleaning up working directory")

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

        process = subprocess.run(
            f'rm -vf {workdir + "/" + "job.target"}',
            shell=True,
            check=True,
        )


@jobrunner.command(name="archive")
@click.option(
    "--tag", "-t", help="name of the archive", default=str(date.today()), type=str
)
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
        print(f"[jobrunner] Working directory: {workdir}")

        # Build main dictionary
        print(f"[jobrunner] Parsing Jobfile configuration")
        main_dict = lib.ParseJobToml(basedir, workdir)

        # Create archive
        print(f"[jobrunner] Creating archive tag: {tag}")
        lib.CreateArchive(main_dict, tag)

        # Return to base directory
        os.chdir(basedir)
