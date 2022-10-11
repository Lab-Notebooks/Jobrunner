# Standard libraries
import os

# local imports
from . import GetNodeList


def CreateSetupFile(main_dict):
    """
    Create a job.setup file using the list of
    job.setup scripts from main dictionary

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
        # working directory
        setupfile.write(f'\nJobWorkDir="{main_dict["workdir"]}"\n')

        # add commands from job.setup script
        # and place a command to chdir into
        # the node directory
        for nodefile in main_dict["job"]["setup"]:

            # get node directory from nodefile
            nodedir = os.path.dirname(nodefile)

            # chdir into node directory
            setupfile.write(f"\ncd {nodedir}\n")

            # add some spaces
            setupfile.write(f"\n")

            # open nodefile in read mode
            # and write lines to setup script
            with open(nodefile, "r") as entry:
                for line in entry:
                    setupfile.write(line)


def CreateInputFile(main_dict):
    """
    Create an input file for a given simulation
    recursively using job.input between basedir
    and workdir using job.input

    main_dict : Dictionary containing details of the
                job configuration in directory tree
    """
    # check to see if input file is
    # defined in the main dictionary
    if main_dict["job"]["input"]:

        # get a list of all job.input
        # files in the directory tree
        # between basedir and workdir
        nodefile_list = GetNodeList(
            main_dict["basedir"],
            main_dict["workdir"],
            node_object=main_dict["job"]["input"],
        )

        # open a job.input file in write mode
        # and replace existing
        with open(main_dict["workdir"] + os.sep + "job.input", "w") as inputfile:

            # loop through the list of
            # source file from job.input
            for nodefile in nodefile_list:

                # open nodefile in read mode
                # write entries to inputfile
                with open(nodefile, "r") as entry:
                    for line in entry:
                        inputfile.write(line)

                # add two spaces for the next file
                inputfile.write(f"\n")


def CreateSubmitFile(main_dict):
    """
    Create a job.submit for a given simulation
    using values from job.submit

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

        # set environment variable
        # to working directory
        submitfile.write(f'\nJobWorkDir="{main_dict["workdir"]}"\n')

        # add commands from job.submit script
        # and chdir into node directory given by
        # the location of script
        for nodefile in main_dict["job"]["submit"]:

            # get node directory from nodefile
            nodedir = os.path.dirname(nodefile)

            # chdir into node directory
            submitfile.write(f"\ncd {nodedir}\n")

            # add some spaces
            submitfile.write(f"\n")

            # open nodefile in read mode
            # and start populating contents
            with open(nodefile, "r") as entry:
                for line in entry:
                    submitfile.write(line)

        # set target file from job.target
        targetfile = main_dict["job"]["target"]

        # check if path to targetfile
        # exists and handle execptions
        if targetfile:
            if os.path.exists(targetfile):

                # get target directory from targetfile
                targetdir = os.path.dirname(targetfile)

                # chdir into target directory
                submitfile.write(f"\ncd {targetdir}\n")

                # add an extra space
                submitfile.write(f"\n")

                # if path to targetfile exists
                # open it in read mode and start
                # writing lines
                with open(targetfile, "r") as entry:
                    for line in entry:
                        submitfile.write(line)
            else:

                # else raise exception
                raise ValueError(f"[jobrunner] {targetfile} not present in path")
