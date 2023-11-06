# Standard libraries
import os
import shutil
import toml
import subprocess
from collections import OrderedDict

# local imports
from jobrunner import lib


def CreateSetupFile(config):
    """
    Create a job.setup file using the list of
    job.setup scripts from main dictionary

    Arguments
    ---------
    config : Dictionary containing details of the
                job configuration in directory tree
    """
    # open job.setup in write mode this will replace existing job.setup in the working directory
    with open(config.job.workdir + os.sep + "job.setup", "w") as setupfile:

        # write the header for bash script
        setupfile.write("#!/bin/bash\n")

        # set -e to return when error is detected
        setupfile.write("\nset -e\n")

        # set environment variable for working directory
        setupfile.write(f'\nexport JobWorkDir="{config.job.workdir}"\n')

        # add commands from job.setup script and place a command to chdir into the node directory
        for nodefile in config.job.setup:

            # get node directory from nodefile
            nodedir = os.path.dirname(nodefile)

            # chdir into node directory
            setupfile.write(f"\ncd {nodedir}\n")

            # add some spaces
            setupfile.write(f"\n")

            # open nodefile in read mode and write lines to setup script
            with open(nodefile, "r") as entry:
                for line in entry:
                    setupfile.write(line)


def CreateInputFile(config):
    """
    Create an input file for a given simulation
    recursively using job.input between basedir
    and workdir defined in config

    config : Dictionary containing details of the
                job configuration in directory tree
    """
    # check to see if input files are defined in the main dictionary
    if config.job.input:

        # define main dictionary
        job_toml = {}

        # loop through the list of source files from job.input
        for nodefile in config.job.input:

            # Read toml configuration from the nodefile and iterator over groups
            node_toml = toml.load(nodefile)
            for group in node_toml.keys():

                # update main dictionary with information from node_toml
                if group in job_toml:
                    job_toml[group].update(node_toml[group])
                else:
                    job_toml[group] = node_toml[group]

        # start writing the job.input file
        with open(config.job.workdir + os.sep + "job.input", "w") as inputfile:

            # write a comment to note how this file is being generated
            inputfile.write("# job.input generated from config.job.input files\n")

            # DEVNOTE (11/03/2023): This replaces the legacy code below.
            toml.dump(job_toml, inputfile)

            # DEVNOTE (11/03/2023): This is loop below was written to sort and indent
            #                       job.input file but was not useful with dealing with
            #                       nested toml configurations. Commenting it and leaving
            #                       it here for legacy.
            #
            # Iterate over groups and start looping over items and populate the main dictionary
            # for group in job_toml.keys():
            #
            #    # write group for toml file
            #    inputfile.write(f"\n[{group}]\n")
            #
            #    for variable, value in OrderedDict(
            #        sorted(job_toml[group].items())
            #    ).items():
            #        if type(value) == str:
            #            inputfile.write(f'{" "*2}{variable} = "{value}"\n')
            #        else:
            #            inputfile.write(f'{" "*2}{variable} = {value}\n')


def CreateTargetFile(config):
    """
    Create a job.target for a given simulation
    using values from job.target in config

    Arguments
    ---------
    config : Dictionary containing details of the
                job configuration in directory tree
    """
    # set target file from job.target
    targetfile = config.job.target

    # check if path to targetfile exists and handle execptions
    if targetfile:
        if os.path.exists(targetfile):

            subprocess.run(
                f"rm -f job.target && ln -s {targetfile} job.target",
                shell=True,
                check=True,
            )

        else:

            # else raise exception
            raise FileNotFoundError(f"[jobrunner] {targetfile} not present in path")


def CreateSubmitFile(config):
    """
    Create a job.submit file for using values
    from job.submit list define in config

    Arguments
    ---------
    config : Dictionary containing details of the
                job configuration in directory tree
    """
    # open job.submit in write mode and start populating
    with open(config.job.workdir + os.sep + "job.submit", "w") as submitfile:

        # write the header
        submitfile.write("#!/bin/bash\n")

        # add commands from schedular.options
        submitfile.write(f"\n")
        for entry in config.schedular.options:
            submitfile.write(f"{entry}\n")

        # set -e to return when error is detected
        submitfile.write("\nset -e\n")

        # set environment variable to working directory
        submitfile.write(f'\nexport JobWorkDir="{config.job.workdir}"\n')

        # add commands from job.submit script and chdir into node
        # directory given by the location of script
        for nodefile in config.job.submit:

            # get node directory from nodefile
            nodedir = os.path.dirname(nodefile)

            # chdir into node directory
            submitfile.write(f"\ncd {nodedir}\n")

            # add some spaces
            submitfile.write(f"\n")

            # open nodefile in read mode and start populating contents
            with open(nodefile, "r") as entry:

                # loop over lines in entry
                for line in entry:

                    # if job.input and job.target used in nodefile.
                    # Make sure they are defined in the directory tree
                    if "job.target" in line.split("#")[0] and not config.job.target:
                        raise ValueError(
                            f"[jobrunner]: job.target used in {nodefile} but not defined in Jobfile"
                        )

                    if "job.input" in line.split("#")[0] and not config.job.input:
                        raise ValueError(
                            f"[jobrunner]: job.input used in {nodefile} but not defined in Jobfile"
                        )

                    # write to submit file if checks passed
                    submitfile.write(line)


def RemoveNodeFiles(config, nodedir):
    """
    Arguments
    ---------
    config : Dictionary containing details of the
                job configuration in directory node

    nodedir : path to node directory
    """
    # get a list of directories along the node between basedir and workdir
    node_list = lib.GetNodeList(config.job.basedir, config.job.workdir)

    # perform checks
    if nodedir not in node_list:
        raise ValueError(f"Node {nodedir} directory does not exists in tree")

    # chdir into node directory
    os.chdir(nodedir)

    # create an empty list of file to be removed
    remove_list = []

    # get the list of files in nodedir
    nodefile_list = [
        os.path.abspath(nodefile)
        for nodefile in next(os.walk("."), (None, None, []))[2]
    ]

    # create a reference file list to test which nodefile should be archived
    ref_list = config.job.clean + [
        nodedir + os.sep + "job.input",
        nodedir + os.sep + "job.setup",
        nodedir + os.sep + "job.submit",
        nodedir + os.sep + "job.target",
        nodedir + os.sep + "job.output",
    ]

    # loop over list of files in nodedir and append to
    # archive_list if file is present in job.archive
    for filename in nodefile_list:
        if filename in ref_list:
            remove_list.append(filename)

    if remove_list:

        # loop over archive_list and archive contents
        for filename in remove_list:
            os.remove(filename)

    # return back to working directory
    os.chdir(config.job.workdir)
