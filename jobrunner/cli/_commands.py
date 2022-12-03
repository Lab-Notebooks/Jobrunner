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
            f"------------------------------------------------------------------------------------------------------"
        )
        os.chdir(workdir)
        workdir = os.getcwd()
        print(f"Working directory: {workdir}")

        # Build main dictionary
        print(f"Parsing Jobfiles in directory tree")
        main_dict = lib.ParseJobConfig(basedir, workdir)

        if show:
            # Print configuration details
            print(f"")
            print(f"job.setup: [")
            for value in main_dict["job"]["setup"]:
                print(f"\t{value}")
            print(f"\t]")

        else:
            # Build setupfile
            print(f"Creating setup file: job.setup")
            lib.CreateSetupFile(main_dict)

            # Run setup
            print(f"Running setup")
            subprocess.run(f"bash job.setup", shell=True, check=True)

        # Return to base directory
        os.chdir(basedir)


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
        print(
            f"------------------------------------------------------------------------------------------------------"
        )
        os.chdir(workdir)
        workdir = os.getcwd()
        print(f"Working directory: {workdir}")

        # Build main dictionary
        print(f"Parsing Jobfiles in directory tree")
        main_dict = lib.ParseJobConfig(basedir, workdir)

        if show:
            # Print configuration details
            print(f"")
            print(f"schedular.command:")
            print(f'\t{main_dict["schedular"]["command"]}')
            print(f"schedular.options: [")
            for value in main_dict["schedular"]["options"]:
                print(f"\t{value}")
            print(f"\t]")
            print(f"job.input: [")
            for value in main_dict["job"]["input"]:
                print(f"\t{value}")
            print(f"\t]")
            print(f"job.target:")
            print(f'\t{main_dict["job"]["target"]}')
            print(f"job.submit: [")
            for value in main_dict["job"]["submit"]:
                print(f"\t{value}")
            print(f"\t]")

        else:
            # Build inputfile
            print(f"Creating input file: job.input")
            lib.CreateInputFile(main_dict)

            # Build targetfile
            print(f"Creating target file: job.target")
            lib.CreateTargetFile(main_dict)

            # Build submitfile
            print(f"Creating submit file: job.submit")
            lib.CreateSubmitFile(main_dict)

            # Submit job
            print(f"Submitting job")
            if main_dict["schedular"]["command"] == "bash":
                subprocess.run(
                    f'{main_dict["schedular"]["command"]} job.submit > job.output > 2>&1',  # > /dev/null 2>&1 &',
                    shell=True,
                    check=True,
                )

            else:
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

    # run cleanup
    for workdir in workdir_list:

        # chdir to working directory
        print(
            f"------------------------------------------------------------------------------------------------------"
        )
        os.chdir(workdir)
        workdir = os.getcwd()
        print(f"Working directory: {workdir}")

        # Build main dictionary
        print(f"Parsing Jobfiles in directory tree")
        main_dict = lib.ParseJobConfig(basedir, workdir)

        print(f"Cleaning up working directory")
        lib.RemoveNodeFiles(main_dict, workdir)

        os.chdir(basedir)


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
        print(
            f"------------------------------------------------------------------------------------------------------"
        )
        os.chdir(workdir)
        workdir = os.getcwd()
        print(f"Working directory: {workdir}")

        # Build main dictionary
        print(f"Parsing Jobfile configuration")
        main_dict = lib.ParseJobConfig(basedir, workdir)

        # Create archive
        print(f"Creating archive tag: {tag}")
        lib.CreateArchive(main_dict, tag)

        # Return to base directory
        os.chdir(basedir)


@jobrunner.command(name="diff")
@click.argument("file1", type=str, required=True)
@click.argument("file2", type=str, required=True)
def diff(file1, file2):
    """
    Run diff on two files
    """
    subprocess.run(
        f"export PATH=~/.local/bin:/usr/local/bin:$PATH && logdiff {file1} {file2}",
        shell=True,
        check=True,
    )
