# Standard libraries
import os
import subprocess

# Feature libraries
import toml


def ParseJobToml(basedir, workdir):
    """
    basedir : base directory
    workdir : work directory
    """
    # Build a list of all toml files in
    # a directory tree between basedir and workdir
    jobfile_list = GetFileList(basedir, workdir, "Jobfile")

    # Create an empty dictionary to set default
    # values for configuration variables
    main_dict = {
        "schedular": {
            "command": None,
            "options": [],
        },
        "config": {
            "input": None,
            "target": None,
            "submit": [],
            "setup": [],
        },
    }

    # Loop over individual files
    for jobfile in jobfile_list:

        # Load the toml file
        work_dict = toml.load(jobfile)

        # loop over keys in work_dict, parse
        # configuration and handle exceptions
        for key in work_dict:

            # loop over subkey and values
            for subkey, value_obj in work_dict[key].items():

                # test combination of values here to get
                # absolute path for setup and submit scripts
                if f"{key}.{subkey}" in [
                    "config.setup",
                    "config.submit",
                ]:
                    value_obj = [
                        os.path.dirname(jobfile) + os.sep + value for value in value_obj
                    ]

                # absolute path for config.target
                if f"{key}.{subkey}" in [
                    "config.target",
                ]:
                    value_obj = os.path.dirname(jobfile) + os.sep + value_obj

                # test combination of values
                # here to handle exceptions
                if f"{key}.{subkey}" in [
                    "schedular.command",
                    "config.input",
                    "config.target",
                ]:

                    # check if main dictionary already contains
                    # definitions for [key][subkey] and enforce
                    # design requirements
                    if main_dict[key][subkey]:
                        raise ValueError(
                            f"[jobrunner] {key}.{subkey} already defined in directory tree"
                        )
                    else:
                        # set values if [key][subkey]
                        # not already set
                        main_dict[key][subkey] = value_obj

                        # store directory name
                        # where input is defined
                        if subkey in ["input"]:
                            main_dict[subkey + "dir"] = os.path.dirname(jobfile)

                else:
                    # extend main dictionary
                    main_dict[key][subkey].extend(value_obj)

    # Add basedir and workdir to
    # main_dict for future use
    main_dict["basedir"] = basedir
    main_dict["workdir"] = workdir

    return main_dict


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
        os.sep + level
        for level in workdir.split(os.sep)
        if level not in basedir.split(os.sep)
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
        file_path = current_level + os.sep + filename

        # Append to file list if path exists
        if os.path.exists(file_path):
            file_list.append(file_path)

    return file_list
