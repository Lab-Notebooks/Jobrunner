"""Command line interface for Jobrunner"""

# Standard libraries
import os
from datetime import date

from jobrunner import lib
from jobrunner import options

if options.INSTRUMENTS == 1:
    from jobrunner import instruments


def setup(dirlist, verbose=False):
    """
    Run setup scripts in a directory
    """
    # get base directory
    basedir = os.getcwd()

    # set variable to determine console separator
    separator = False

    # loop over dirlist
    for workdir in dirlist:

        # add separator to improve output readiblity
        if separator:
            lib.ConsoleSeparator()

        # chdir to working directory and display tree
        os.chdir(workdir)
        workdir = os.getcwd()
        lib.DisplayTree(basedir, workdir)

        # parse main dictionary
        config = lib.ParseJobConfig(basedir, workdir)

        # create setup file and display configuration
        lib.CreateSetupFile(config)
        print(f"\n{lib.Color.purple}SCRIPTS: {lib.Color.end}")
        for value in config.job.setup:
            if value:
                print(f'{" "*4}- {value.replace(basedir,"<ROOT>")}')

        # run a bash process
        lib.BashProcess(basedir, workdir, "job.setup", verbose)

        # set separator value
        separator = True

        # Return to base directory
        os.chdir(basedir)


def submit(dirlist, verbose=False):
    """
    Submit a job from a directory
    """
    # get base directory
    basedir = os.getcwd()

    # set variable to determine console separator
    separator = False

    # loop over dirlist
    for workdir in dirlist:

        # add separator to improve output readiblity
        if separator:
            lib.ConsoleSeparator()

        # chdir to working directory and display tree
        os.chdir(workdir)
        workdir = os.getcwd()
        lib.DisplayTree(basedir, workdir)

        # parse main dictionary
        config = lib.ParseJobConfig(basedir, workdir)

        # Build inputfile
        lib.CreateInputFile(config)
        if config.job.input:
            print(f"\n{lib.Color.purple}INPUT: {lib.Color.end}")
            for value in config.job.input:
                print(f'{" "*4}- {value.replace(basedir,"<ROOT>")}')

        # Build targetfile
        lib.CreateTargetFile(config)
        if config.job.target:
            print(
                f"\n{lib.Color.purple}TARGET:{lib.Color.end} "
                + f'{config.job.target.replace(basedir,"<ROOT>")}'
            )

        # Build submitfile
        lib.CreateSubmitFile(config)
        print(f"\n{lib.Color.purple}SCRIPTS: {lib.Color.end}")
        for value in config.job.submit:
            print(f'{" "*4}- {value.replace(basedir,"<ROOT>")}')

        # Instrument specific work
        if options.INSTRUMENTS == 1 and config.instrument:
            if config.instrument in instruments.Run:
                print(
                    f"\n{lib.Color.purple}INSTRUMENT:{lib.Color.end} "
                    + f"{config.instrument}"
                )
                instruments.Run[config.instrument](config)

            else:
                raise ValueError(
                    f'[jobrunner] Instrument "{config.instrument}" not present in '
                    + f"available instruments {list(instruments.Run.keys())}"
                )

        # Submit job
        if config.schedular.command == "bash":
            lib.BashProcess(basedir, workdir, "job.submit", verbose)

        else:
            lib.SchedularProcess(
                basedir, workdir, config.schedular.command, "job.submit"
            )

        # set separator value
        separator = True

        # Return to base directory
        os.chdir(basedir)


def clean(dirlist):
    """
    Remove artifacts from a directory
    """
    # get base directory
    basedir = os.getcwd()

    # print root directory
    print(f"{lib.Color.purple}ROOT:{lib.Color.end} {basedir}")
    print(f"\n{lib.Color.purple}CLEAN:{lib.Color.end}")

    # run cleanup
    for workdir in dirlist:

        # chdir to working directory and display tree
        os.chdir(workdir)
        workdir = os.getcwd()

        # parse main dictionary
        config = lib.ParseJobConfig(basedir, workdir)

        # clean the directory
        print(f'{" "*4}- {workdir.replace(basedir,"<ROOT>")}')
        lib.RemoveNodeFiles(config, workdir)

        os.chdir(basedir)


def archive(tag, dirlist):
    """
    Create an archive along a directory tree
    """
    # get base directory
    basedir = os.getcwd()

    # print root directory
    print(f"{lib.Color.purple}ROOT:{lib.Color.end} {basedir}")
    print(f"\n{lib.Color.purple}ARCHIVE:{lib.Color.end}")

    archive_list = []

    # loop over dirlist
    for workdir in dirlist:

        # chdir to working directory and display tree
        os.chdir(workdir)
        workdir = os.getcwd()

        # parse main dictionary
        config = lib.ParseJobConfig(basedir, workdir)

        # create directory tree for archive
        dirtree = workdir.replace(basedir, "<ROOT>").split(os.sep)

        # print directories that will be archived
        pathdir = ""
        for nodedir in dirtree:
            pathdir = pathdir + nodedir

            if pathdir not in archive_list:
                print(f'{" "*4}- {pathdir}/jobnode.archive/{tag}')
                archive_list.append(pathdir)

            pathdir = pathdir + os.sep

        lib.CreateArchive(config, tag)

        # Return to base directory
        os.chdir(basedir)


def export(dest, dirlist):
    """
    \b
    Export directory tree to an external folder
    \b
    """
    # get base directory
    basedir = os.getcwd()

    # print root directory
    print(f"{lib.Color.purple}ROOT:{lib.Color.end} {basedir}")
    print(f"\n{lib.Color.purple}EXPORT:{lib.Color.end}")

    export_list = []

    # loop over dirlist
    for workdir in dirlist:

        # chdir to working directory and display tree
        os.chdir(workdir)
        workdir = os.getcwd()

        # parse main dictionary
        config = lib.ParseJobConfig(basedir, workdir)

        # create directory tree for archive
        dirtree = workdir.replace(basedir, "<ROOT>").split(os.sep)

        # print directories that will be archived
        pathdir = ""
        for nodedir in dirtree:
            pathdir = pathdir + nodedir

            if pathdir not in export_list:
                print(f'{" "*4}- {pathdir}')
                export_list.append(pathdir)

            pathdir = pathdir + os.sep

        # create archive
        lib.ExportTree(config, dest)

        # Return to base directory
        os.chdir(basedir)

    print(f"\n{lib.Color.purple}DEST:{lib.Color.end} {dest}")
