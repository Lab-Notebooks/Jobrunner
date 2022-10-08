# Standard libraries
import os
import glob

# Feature libraries
import toml


def ParseJobToml(basedir, workdir):
    """
    basedir : base directory
    workdir : work directory
    """

    if basedir not in workdir:
        raise ValueError(f"[jobrunner] {workdir} not a sub-directory of {basedir}")

    # build a list of all toml files in
    # a directory tree between basedir and workdir
    jobfile_list = GetTreeList(basedir, workdir, tree_object="Jobfile")

    # create an empty dictionary to set default
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
            "archive": [],
        },
    }

    # loop over individual files
    for jobfile in jobfile_list:

        # load the toml file
        work_dict = toml.load(jobfile)

        # loop over keys in work_dict, parse
        # configuration and handle exceptions
        for key in work_dict:

            # loop over subkey and values
            for subkey, work_obj in work_dict[key].items():

                # test combination of values here to get
                # absolute path for setup and submit scripts
                if f"{key}.{subkey}" in [
                    "config.setup",
                    "config.submit",
                ]:
                    work_obj = [
                        os.path.dirname(jobfile) + os.sep + value for value in work_obj
                    ]

                # absolute path for config.target
                if f"{key}.{subkey}" in [
                    "config.target",
                ]:
                    work_obj = os.path.dirname(jobfile) + os.sep + work_obj

                if f"{key}.{subkey}" in [
                    "config.archive",
                ]:
                    work_obj = [
                        os.path.dirname(jobfile) + os.sep + value for value in work_obj
                    ]

                    archive_obj = []
                    for value in work_obj:
                        archive_obj.extend(glob.glob(value))

                    work_obj = [*set(archive_obj)]

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
                            f"[jobrunner] Found duplicates for {key}.{subkey} in directory tree"
                        )
                    else:
                        # set values if [key][subkey]
                        # not already set
                        main_dict[key][subkey] = work_obj

                        # store directory name
                        # where input is defined
                        if subkey in ["input"]:
                            main_dict[subkey + "dir"] = os.path.dirname(jobfile)

                else:
                    # extend main dictionary
                    main_dict[key][subkey].extend(work_obj)

    # add basedir and workdir to
    # main_dict for future use
    main_dict["basedir"] = basedir
    main_dict["workdir"] = workdir

    # perform checks to enforce desgin
    # constraints for config.input and config.target
    if main_dict["config"]["input"]:

        # create a list of input files to perform checks
        # along the directory tree
        inputfile_list = GetTreeList(
            main_dict["basedir"],
            main_dict["workdir"],
            tree_object=main_dict["config"]["input"],
        )

        targetfile = main_dict["config"]["target"]

        # loop over input files and start comparing length of directories
        for inputfile in inputfile_list:
            if len(os.path.dirname(inputfile)) < len(main_dict["inputdir"]):
                raise ValueError(
                    f"[jobrunner] config.input: {inputfile} should not exist before it is defined in Jobfile"
                )

            if targetfile and len(os.path.dirname(targetfile)) < len(
                main_dict["inputdir"]
            ):
                raise ValueError(
                    f"[jobrunner] config.target: {targetfile} should not exist before config.input is defined in Jobfile"
                )

    return main_dict


def GetTreeList(basedir, workdir, tree_object=""):
    """
    Get a list of paths containing an object
    with name tree_object between basedir and workdir

    Arguments
    ---------
    basedir     :  Base directory (top level) of a project
    workdir     :  Current job directory
    tree_object :  Name of the directory object

    Returns
    --------
    object_list :   A list of path containing the object
    """

    # get a list of directory levels
    # between `basedir` and `workdir`
    dir_levels = [
        os.sep + level
        for level in workdir.split(os.sep)
        if level not in basedir.split(os.sep)
    ]

    # create an empty list of objects
    object_list = []

    # start with current level
    current_level = basedir

    # loop over directory levels
    for level in [""] + dir_levels:

        # set current level
        current_level = current_level + level

        # set object path
        object_path = current_level + os.sep + tree_object

        # append to object_list
        # if path exists
        if os.path.exists(object_path):
            object_list.append(os.path.abspath(object_path))

    return object_list
