"""Command line interface for Jobrunner"""

# Standard libraries
import os
from datetime import date

from jobrunner import lib


def setup(workdir_list, verbose=False):
    """
    Run setup scripts in a directory
    """
    # Get base directory
    basedir = os.getcwd()

    # loop over workdir_list
    for workdir in workdir_list:

        # chdir to working directory and display tree
        os.chdir(workdir)
        workdir = os.getcwd()
        lib.DisplayTree(workdir, basedir)

        # parse main dictionary
        main_dict = lib.ParseJobConfig(basedir, workdir)

        # create setup file and display configuration
        lib.CreateSetupFile(main_dict)
        print(f"\n{lib.Color.purple}SCRIPTS: {lib.Color.end}")
        for value in main_dict["job"]["setup"]:
            if value:
                print(
                    f'- {lib.Color.blue}{value.replace(basedir,"ROOT")} {lib.Color.end}'
                )

        # run a bash process
        lib.BashProcess(basedir, workdir, "job.setup", verbose)

        # Return to base directory
        os.chdir(basedir)


def submit(workdir_list, verbose=False):
    """
    Submit a job from a directory
    """
    # Get base directory
    basedir = os.getcwd()

    # loop over workdir_list
    for workdir in workdir_list:

        # chdir to working directory and display tree
        os.chdir(workdir)
        workdir = os.getcwd()
        lib.DisplayTree(workdir, basedir)

        # parse main dictionary
        main_dict = lib.ParseJobConfig(basedir, workdir)

        # Build inputfile
        lib.CreateInputFile(main_dict)
        if main_dict["job"]["input"]:
            print(f"\n{lib.Color.purple}INPUT: {lib.Color.end}")
            for value in main_dict["job"]["input"]:
                print(
                    f'- {lib.Color.blue}{value.replace(basedir,"ROOT")} {lib.Color.end}'
                )

        # Build targetfile
        lib.CreateTargetFile(main_dict)
        if main_dict["job"]["target"]:
            print(
                f"\n{lib.Color.purple}TARGET: "
                + f'{lib.Color.blue}{main_dict["job"]["target"].replace(basedir,"ROOT")} {lib.Color.end}'
            )

        # Build submitfile
        lib.CreateSubmitFile(main_dict)
        print(f"\n{lib.Color.purple}SCRIPTS: {lib.Color.end}")
        for value in main_dict["job"]["submit"]:
            print(f'- {lib.Color.blue}{value.replace(basedir,"ROOT")} {lib.Color.end}')

        # Submit job
        if main_dict["schedular"]["command"] == "bash":
            lib.BashProcess(basedir, workdir, "job.submit", verbose)

        else:
            lib.SchedularProcess(
                basedir, workdir, main_dict["schedular"]["command"], "job.submit"
            )

        # Return to base directory
        os.chdir(basedir)


def clean(workdir_list):
    """
    Remove artifacts from a directory
    """
    # Get base directory
    basedir = os.getcwd()

    # run cleanup
    for workdir in workdir_list:

        # chdir to working directory and display tree
        os.chdir(workdir)
        workdir = os.getcwd()
        lib.DisplayTree(workdir, basedir)

        # parse main dictionary
        main_dict = lib.ParseJobConfig(basedir, workdir)

        print(f"\n{lib.Color.purple}CLEANING {lib.Color.end}")
        lib.RemoveNodeFiles(main_dict, workdir)

        os.chdir(basedir)


def archive(tag, workdir_list):
    """
    Create an archive along a directory tree
    """
    # Get base directory
    basedir = os.getcwd()

    # loop over workdir_list
    for workdir in workdir_list:

        # chdir to working directory and display tree
        os.chdir(workdir)
        workdir = os.getcwd()
        lib.DisplayTree(workdir, basedir)

        # parse main dictionary
        main_dict = lib.ParseJobConfig(basedir, workdir)

        # Create archive
        print(
            f"\n➤ {lib.Color.purple}ARCHIVE: {lib.Color.blue}jobnode.archive/{tag} {lib.Color.end}"
        )

        lib.CreateArchive(main_dict, tag)

        # Return to base directory
        os.chdir(basedir)


def export(tag, workdir_list):
    """
    \b
    Export directory tree to an external folder
    \b
    """
    # Get base directory
    basedir = os.getcwd()

    # loop over workdir_list
    for workdir in workdir_list:

        # chdir to working directory and display tree
        os.chdir(workdir)
        workdir = os.getcwd()
        lib.DisplayTree(workdir, basedir)

        # parse main dictionary
        main_dict = lib.ParseJobConfig(basedir, workdir)

        # Create archive
        print(f"\n➤ {lib.Color.purple}EXPORT: {lib.Color.blue}{tag} {lib.Color.end}")
        lib.ExportTree(main_dict, tag)

        # Return to base directory
        os.chdir(basedir)
