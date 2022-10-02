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
    main_dict = {
        "job": {"schedular": "None", "input": "None"},
        "config": {"commands": [], "schedular": [], "source": [], "scripts": []},
    }

    # Loop over individual files
    for jobtoml in jobtoml_list:

        # Load the toml file
        job_dict = toml.load(jobtoml)

        # parse `job` in job_dict
        # and update main_dict
        if "job" in job_dict:
            main_dict.update({"job": job_dict["job"]})

        # parse job config and loop
        # over items
        if "config" in job_dict:

            # looping over items
            for key, values in job_dict["config"].items():

                # special case for `source` assign
                # absolute path
                if key in ["source", "scripts"] and values:
                    values = [jobtoml.replace("job.toml", value) for value in values]

                # extend main dict
                main_dict["config"][key].extend(values)

    # Add basedir and workdir to main_dict
    # for future use
    main_dict["basedir"] = basedir
    main_dict["workdir"] = workdir

    return main_dict


def runConfigScripts(main_dict):
    """
    run configuration scripts

    `main_dict` : job dictionary
    """
    for script in main_dict["config"]["scripts"]:
        subprocess.run(f"{script}", shell=True, check=True)


def createInputFile(main_dict):
    """
    create an input file for a given simulation recursively using
    `job.input` between `basedir` and `workdir`

    `main_dict` : job dictionary
    """
    # get inputfile_list from internal method
    inputfile_list = _getFileList(
        main_dict["basedir"], main_dict["workdir"], "job.input"
    )

    # run a subprocess to build flash.par
    process = subprocess.run(
        f'rm -f {main_dict["job"]["input"]} && cat {" ".join(inputfile_list)} > {main_dict["job"]["input"]}',
        shell=True,
        check=True,
    )


def createJobFile(main_dict):
    """
    create `job.sh` for a given simulation recursively using configuration
    `job` dictionary

    `main_dict`       :  Job dictionary
    """
    # set header for the submit script
    with open(main_dict["workdir"] + "/" + "job.sh", "w") as jobfile:

        # write the header
        jobfile.write("#!/bin/bash\n\n")

        # Add schedular commands
        for entry in main_dict["config"]["schedular"]:
            jobfile.write(f"{entry}\n")

        # Add an extra space
        jobfile.write("\n")

        # Add commands to source scripts
        for entry in main_dict["config"]["source"]:
            jobfile.write(f"source {entry}\n")

        # Add an extra space
        jobfile.write("\n")

        # Add bash commands
        for entry in main_dict["config"]["commands"]:
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
        "/" + level for level in workdir.split("/") if level not in basedir.split("/")
    ]

    # Create an empty file list
    file_list = []

    # start with current level
    current_level = basedir

    # Loop over directory levels
    for level in [""] + dir_levels:

        # Set current level
        current_level = current_level + level

        # set file path
        file_path = current_level + "/" + filename

        # Append to file list if path exists
        if os.path.exists(file_path):
            file_list.append(file_path)

    return file_list
