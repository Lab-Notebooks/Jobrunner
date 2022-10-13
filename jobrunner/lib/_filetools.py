# Standard libraries
import os
import subprocess


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
    with open(main_dict["job"]["workdir"] + os.sep + "job.setup", "w") as setupfile:

        # write the header for bash script
        setupfile.write("#!/bin/bash\n")

        # set environment variable for
        # working directory
        setupfile.write(f'\nJobWorkDir="{main_dict["job"]["workdir"]}"\n')

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
    and workdir defined in main_dict

    main_dict : Dictionary containing details of the
                job configuration in directory tree
    """
    # check to see if input files are
    # defined in the main dictionary
    if main_dict["job"]["input"]:

        # open a job.input file in write mode
        # and replace existing
        with open(main_dict["job"]["workdir"] + os.sep + "job.input", "w") as inputfile:

            # loop through the list of
            # source file from job.input
            for nodefile in main_dict["job"]["input"]:

                # open nodefile in read mode
                # write entries to inputfile
                with open(nodefile, "r") as entry:
                    for line in entry:
                        inputfile.write(line)

                # add two spaces for the next file
                inputfile.write(f"\n")


def CreateTargetFile(main_dict):
    """
    Create a job.target for a given simulation
    using values from job.target in main_dict

    Arguments
    ---------
    main_dict : Dictionary containing details of the
                job configuration in directory tree
    """
    # set target file from job.target
    targetfile = main_dict["job"]["target"]

    # check if path to targetfile
    # exists and handle execptions
    if targetfile:
        if os.path.exists(targetfile):

            subprocess.run(
                f"rm -f job.target && ln -s {targetfile} job.target",
                shell=True,
                check=True,
            )

        else:

            # else raise exception
            raise ValueError(f"[jobrunner] {targetfile} not present in path")


def CreateSubmitFile(main_dict):
    """
    Create a job.submit file for using values
    from job.submit list define in main_dict

    Arguments
    ---------
    main_dict : Dictionary containing details of the
                job configuration in directory tree
    """
    # open job.submit in write mode
    # and start populating
    with open(main_dict["job"]["workdir"] + os.sep + "job.submit", "w") as submitfile:

        # write the header
        submitfile.write("#!/bin/bash\n")

        # add commands from
        # schedular.options
        submitfile.write(f"\n")
        for entry in main_dict["schedular"]["options"]:
            submitfile.write(f"{entry}\n")

        # set environment variable
        # to working directory
        submitfile.write(f'\nJobWorkDir="{main_dict["job"]["workdir"]}"\n')

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

                # loop over lines in entry
                for line in entry:

                    # if job.input and job.target used
                    # in nodefile. Make sure they are
                    # defined in the directory tree
                    if (
                        "job.target" in line.split("#")[0]
                        and not main_dict["job"]["target"]
                    ):
                        raise ValueError(
                            f"[jobrunner]: job.target used in {nodefile} but not defined in Jobfile"
                        )

                    if (
                        "job.input" in line.split("#")[0]
                        and not main_dict["job"]["input"]
                    ):
                        raise ValueError(
                            f"[jobrunner]: job.input used in {nodefile} but not defined in Jobfile"
                        )

                    # write to submit file if checks passed
                    submitfile.write(line)
