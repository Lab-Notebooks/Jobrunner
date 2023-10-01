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
        lib.DisplayTree(basedir, workdir)

        # parse main dictionary
        main_dict = lib.ParseJobConfig(basedir, workdir)

        # create setup file and display configuration
        lib.CreateSetupFile(main_dict)
        print(f"\n{lib.Color.purple}SCRIPTS: {lib.Color.end}")
        for value in main_dict["job"]["setup"]:
            if value:
                print(f'{" "*4}- {value.replace(basedir,"<ROOT>")}')

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
        lib.DisplayTree(basedir, workdir)

        # parse main dictionary
        main_dict = lib.ParseJobConfig(basedir, workdir)

        # Build inputfile
        lib.CreateInputFile(main_dict)
        if main_dict["job"]["input"]:
            print(f"\n{lib.Color.purple}INPUT: {lib.Color.end}")
            for value in main_dict["job"]["input"]:
                print(f'{" "*4}- {value.replace(basedir,"<ROOT>")}')

        # Build targetfile
        lib.CreateTargetFile(main_dict)
        if main_dict["job"]["target"]:
            print(
                f"\n{lib.Color.purple}TARGET:{lib.Color.end} "
                + f'{main_dict["job"]["target"].replace(basedir,"<ROOT>")}'
            )

        # Build submitfile
        lib.CreateSubmitFile(main_dict)
        print(f"\n{lib.Color.purple}SCRIPTS: {lib.Color.end}")
        for value in main_dict["job"]["submit"]:
            print(f'{" "*4}- {value.replace(basedir,"<ROOT>")}')

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
    print(os.get_terminal_size().columns * "—")

    # run cleanup
    for workdir in workdir_list:

        # chdir to working directory and display tree
        os.chdir(workdir)
        workdir = os.getcwd()

        # parse main dictionary
        main_dict = lib.ParseJobConfig(basedir, workdir)

        print(f"{lib.Color.purple}CLEAN:{lib.Color.end} {workdir}")
        lib.RemoveNodeFiles(main_dict, workdir)

        os.chdir(basedir)


def archive(tag, workdir_list):
    """
    Create an archive along a directory tree
    """
    # Get base directory
    basedir = os.getcwd()
    print(os.get_terminal_size().columns * "—")

    # loop over workdir_list
    for workdir in workdir_list:

        # chdir to working directory and display tree
        os.chdir(workdir)
        workdir = os.getcwd()

        # parse main dictionary
        main_dict = lib.ParseJobConfig(basedir, workdir)

        # Create archive
        print(
            f"{lib.Color.purple}ARCHIVE:{lib.Color.end} {workdir}/jobnode.archive/{tag}"
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
        lib.DisplayTree(basedir, workdir)

        # parse main dictionary
        main_dict = lib.ParseJobConfig(basedir, workdir)

        # Create archive
        print(f"{lib.Color.purple}EXPORT:{lib.Color.end} {tag}")
        lib.ExportTree(main_dict, tag)

        # Return to base directory
        os.chdir(basedir)
