# Standard libraries
import os
import subprocess

import toml


def parseJobToml(basedir, workdir):
    """
    `basedir` : base directory
    `workdir` : work directory
    """
    # Build a list of all toml files in the directory structure
    jobtoml_list = _getFileList(basedir, workdir, "job.toml")

    # Create an empty dictionary for job object
    job = {
        "info": {"schedular": "None", "input": "None"},
        "config": {"commands": [], "schedular": []},
    }

    # Loop over individual files
    for jobtoml in jobtoml_list:

        # Load the toml file
        jobdict = toml.load(jobtoml)

        if "info" in jobdict:
            job.update({"info": jobdict["info"]})

        if "config" in jobdict:
            for key, values in jobdict["config"].items():
                job["config"][key].extend(values)

    job["basedir"] = basedir
    job["workdir"] = workdir

    return job


def createInputFile(job):
    """
    create an input file for a given simulation recursively using
    `job.inf.input` between `basedir` and `workdir`

    """
    # get inputfile_list from internal method
    inputfile_list = _getFileList(job["basedir"], job["workdir"], "job.input")

    # run a subprocess to build flash.par
    process = subprocess.run(
        f'rm -f {job["info"]["input"]} && cat {" ".join(inputfile_list)} > {job["info"]["input"]}',
        shell=True,
        check=True,
    )


def createJobFile(job):
    """
    create `job.sh` for a given simulation recursively using configuration
    `job` dictionary

    `job`       :  Job dictionary
    """
    # set header for the submit script
    with open(job["workdir"] + "/" + "job.sh", "w") as jobfile:

        # write the header
        jobfile.write("#!/bin/bash\n\n")

        # Add schedular commands
        for entry in job["config"]["schedular"]:
            jobfile.write(f"{entry}\n")

        # Add an extra space
        jobfile.write("\n")

        for entry in job["config"]["commands"]:
            jobfile.write(f"{entry}\n")


def _getFileList(basedir, workdir, filename):
    """
    Get a list of paths containing a file with name
    `filename` between `basedir` and `workdir`

    Arguments
    ---------
    `basedir`  :  Base directory (top level) of a project
    `workdir`  :  Current job directory
    `filename` :  Name of the file to query

    Returns
    --------
    file_list :   A list of path containing the file
    """

    # Get a list of directory levels between `basedir` and `workdir`
    dir_levels = [
        level for level in workdir.split("/") if level not in basedir.split("/")
    ]

    # Create an empty file list
    file_list = []

    # start with current level
    current_level = basedir

    # Loop over directory levels
    for level in [""] + dir_levels:

        # Set current level
        current_level = current_level + "/" + level

        # set file path
        file_path = current_level + "/" + filename

        # Append to file list if path exists
        if os.path.exists(file_path):
            file_list.append(file_path)

    return file_list
