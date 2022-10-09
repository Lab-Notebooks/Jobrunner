# Standard libraries
import os

# local imports
from . import GetTreeList


def CreateSetupFile(main_dict):
    """
    Create a job.setup file using the list of
    config.setup scripts from main dictionary

    Arguments
    ---------
    main_dict : Dictionary containing details of the
                job configuration in directory tree
    """
    # open job.setup in write mode this
    # will replace existing job.setup
    # in the working directory
    with open(main_dict["workdir"] + os.sep + "job.setup", "w") as setupfile:

        # write the header for bash script
        setupfile.write("#!/bin/bash\n")

        # set environment variable for
        # base directory
        setupfile.write(f'\nJobBaseDir="{main_dict["basedir"]}"\n')

        # set environment variable for
        # working directory
        setupfile.write(f'\nJobWorkDir="{main_dict["workdir"]}"\n')

        # add commands from config.setup script
        # and set environment variable for tree
        # directory to the location of script
        for sourcefile in main_dict["config"]["setup"]:
            setupfile.write(f'\nJobTreeDir="{os.path.dirname(sourcefile)}"\n')

            # add some spaces
            setupfile.write(f"\n")

            # open sourcefile in read mode
            # and write lines to setup script
            with open(sourcefile, "r") as entry:
                for line in entry:
                    setupfile.write(line)

            # chdir into working directory
            setupfile.write(f"\ncd $JobWorkDir\n")


def CreateInputFile(main_dict):
    """
    Create an input file for a given simulation
    recursively using job.input between basedir
    and workdir using config.input

    main_dict : Dictionary containing details of the
                job configuration in directory tree
    """
    # check to see if input file is
    # defined in the main dictionary
    if main_dict["config"]["input"]:

        # get a list of all config.input
        # files in the directory tree
        # between basedir and workdir
        sourcefile_list = GetTreeList(
            main_dict["basedir"],
            main_dict["workdir"],
            tree_object=main_dict["config"]["input"],
        )

        # open a job.input file in write mode
        # and replace existing
        with open(main_dict["workdir"] + os.sep + "job.input", "w") as inputfile:

            # loop through the list of
            # source file from config.input
            for sourcefile in sourcefile_list:

                # open sourcefile in read mode
                # write entries to inputfile
                with open(sourcefile, "r") as entry:
                    for line in entry:
                        inputfile.write(line)

                # add two spaces for the next file
                inputfile.write(f"\n")


def CreateSubmitFile(main_dict):
    """
    Create a job.submit for a given simulation
    using values from config.submit

    Arguments
    ---------
    main_dict : Dictionary containing details of the
                job configuration in directory tree
    """
    # open job.submit in write mode
    # and start populating
    with open(main_dict["workdir"] + os.sep + "job.submit", "w") as submitfile:

        # write the header
        submitfile.write("#!/bin/bash\n")

        # add commands from
        # schedular.options
        submitfile.write(f"\n")
        for entry in main_dict["schedular"]["options"]:
            submitfile.write(f"{entry}\n")

        # set environment variable for
        # base directory
        setupfile.write(f'\nJobBaseDir="{main_dict["basedir"]}"\n')

        # set environment variable
        # to working directory
        submitfile.write(f'\nJobWorkDir="{main_dict["workdir"]}"\n')

        # add commands from config.submit script
        # and set environment variable for tree
        # directory to the location of script
        for sourcefile in main_dict["config"]["submit"]:
            submitfile.write(f'\nJobTreeDir="{os.path.dirname(sourcefile)}"\n')

            # add some spaces
            submitfile.write(f"\n")

            # open sourcefile in read mode
            # and start populating contents
            with open(sourcefile, "r") as entry:
                for line in entry:
                    submitfile.write(line)

            # chdir into working directory
            setupfile.write(f"\ncd $JobWorkDir\n")

        # set target file from config.target
        targetfile = main_dict["config"]["target"]

        # check if path to targetfile
        # exists and handle execptions
        if os.path.exists(targetfile):

            # if path to targetfile exists
            # open it in read mode and start
            # writing lines
            with open(targetfile, "r") as entry:
                for line in entry:
                    submitfile.write(line)
        else:

            # else raise exception
            raise ValueError(f"[jobrunner] {targetfile} not present in path")
