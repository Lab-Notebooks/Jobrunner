# Standard libraries
import os
import subprocess

import toml


def ParseJobToml(basedir, workdir):
    """
    `basedir` : base directory
    `workdir` : work directory
    """
    # Build a list of all toml files in the directory structure
    jobtoml_list = GetFileList(basedir, workdir, "job.toml")

    # Create an empty dictionary for job object
    main_dict = {
        "job": {
            "schedular": "None",
            "input": "None",
            "exec": "None",
        },
        "config": {
            "schedular": [],
            "submit": [],
            "setup": [],
        },
    }

    # Loop over individual files
    for jobtoml in jobtoml_list:

        # Load the toml file
        job_dict = toml.load(jobtoml)

        # parse `job` in job_dict
        # and update main_dict
        if "job" in job_dict:

            # looping over items
            for key, value in job_dict["job"].items():
                main_dict["job"].update({key: value})

        # set path to job.sh script
        job_sh = jobtoml.replace("job.toml", "job.sh")

        # update dictionary if job_sh in path
        if os.path.exists(job_sh):
            main_dict["job"].update({"exec": job_sh})

        # parse job config and loop
        # over items
        if "config" in job_dict:

            # looping over items
            for key, value_list in job_dict["config"].items():

                # special case for `run`, `scripts`,
                # and `setup', assign absolute path
                if key in ["submit", "setup"] and value_list:
                    value_list = [
                        jobtoml.replace("job.toml", value) for value in value_list
                    ]

                # Extend main dictionary in bottom-up order
                main_dict["config"][key].extend(value_list)

    # Add basedir and workdir to main_dict
    # for future use
    main_dict["basedir"] = basedir
    main_dict["workdir"] = workdir

    return main_dict


def CreateSetupFile(main_dict):
    """
    create a setup script

    `main_dict` : job dictionary
    """
    # set header for the setup script
    with open(main_dict["workdir"] + "/" + "job_setup.sh", "w") as setupfile:

        # write the header
        setupfile.write("#!/bin/bash\n")

        # set environment variable
        # to working directory
        setupfile.write(f'\nexport JOB_WORKDIR="{main_dict["workdir"]}"')

        # add commands to source run scripts
        for entry in main_dict["config"]["setup"]:
            setupfile.write(f'\n\nexport JOB_FILEDIR="{os.path.dirname(entry)}"')
            setupfile.write(f"\nsource {entry}")

        # Add an extra space
        setupfile.write("\n")


def CreateInputFile(main_dict):
    """
    create an input file for a given simulation recursively using
    `job.input` between `basedir` and `workdir`

    `main_dict` : job dictionary
    """
    # get inputfile_list from internal method
    inputfile_list = GetFileList(
        main_dict["basedir"], main_dict["workdir"], "job.input"
    )

    # run a subprocess to build flash.par
    process = subprocess.run(
        f'rm -f {main_dict["job"]["input"]} &&'
        + " "
        + f'cat {" ".join(inputfile_list)} > {main_dict["job"]["input"]}',
        shell=True,
        check=True,
    )


def CreateJobFile(main_dict):
    """
    create `job.run` for a given simulation recursively using configuration
    `job` dictionary

    `main_dict`       :  Job dictionary
    """
    # set header for the submit script
    with open(main_dict["workdir"] + "/" + "job_submit.sh", "w") as jobfile:

        # write the header
        jobfile.write("#!/bin/bash\n")

        # add schedular commands
        for entry in main_dict["config"]["schedular"]:
            jobfile.write(f"\n{entry}")

        # set environment variable
        # to working directory
        jobfile.write(f'\n\nexport JOB_WORKDIR="{main_dict["workdir"]}"')

        # add commands to source run scripts
        for entry in main_dict["config"]["submit"]:
            jobfile.write(f'\n\nexport JOB_FILEDIR="{os.path.dirname(entry)}"')
            jobfile.write(f"\nsource {entry}")

        # source `job.sh`
        if os.path.exists(main_dict["job"]["exec"]):
            jobfile.write(
                f'\n\nexport JOB_FILEDIR="{os.path.dirname(main_dict["job"]["exec"])}"'
            )
            jobfile.write(f'\nsource {main_dict["job"]["exec"]}')
        else:
            raise ValueError("[jobrunner] `job.sh` not present in path")

        # add an extra space
        jobfile.write("\n")


def GetFileList(basedir, workdir, filename):
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

    # get a list of directory levels
    # between `basedir` and `workdir`
    dir_levels = [
        "/" + level for level in workdir.split("/") if level not in basedir.split("/")
    ]

    # create an empty
    # file list
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
