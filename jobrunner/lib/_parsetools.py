# Standard libraries
import os
import glob
from types import SimpleNamespace

# Feature libraries
import toml
import yaml

from jobrunner import options


class __YamlLoader(yaml.SafeLoader):
    """
    Class YamlLoader for YAML
    """

    def __init__(self, stream):
        """
        Constructor
        """
        super().__init__(stream)
        self._stream = stream

    def construct_mapping(self, node, deep=False):
        """
        Mapping function
        """
        mapping = set()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in mapping:
                print(f"ERROR:   Duplicate {key!r} key found in {self._stream.name!r}.")
                raise ValueError()
            mapping.add(key)
        return super().construct_mapping(node, deep)


def ParseJobConfig(basedir, workdir):
    """
    basedir : base directory
    workdir : work directory
    """

    if basedir not in workdir:
        raise ValueError(f"[jobrunner] {workdir} not a sub-directory of {basedir}")

    # build a list of all toml files in a directory tree between basedir and workdir
    jobfile_list = GetNodeList(basedir, workdir, node_object="Jobfile")

    # create an empty dictionary to set default values for configuration variables
    config = {
        "instrument": "",
        "schedular": {
            "command": "",
            "options": [],
        },
        "job": {
            "input": [],
            "target": "",
            "submit": [],
            "setup": [],
            "clean": [],
            "archive": [],
            "basedir": basedir,
            "workdir": workdir,
        },
    }

    # loop over individual files
    for jobfile in jobfile_list:

        # load the job configuration both toml and yaml formats supported
        # try toml load
        try:
            work_dict = toml.load(jobfile)

        # if error try yaml load
        except:
            with open(jobfile, "r") as stream:
                try:
                    work_dict = yaml.load(stream, Loader=__YamlLoader)
                except yaml.YAMLError as exc:
                    print(exc)

        # loop over keys in work_dict, parse configuration and handle exceptions
        for key in work_dict:

            if key == "instrument":
                # some checks to enforce design consistency
                if isinstance(work_dict[key], list):
                    raise ValueError(f"[jobrunner] {key} cannot be a list")

                # check if main dictionary already contains definitions for instrument
                if config[key]:
                    raise ValueError(
                        f"[jobrunner] Found duplicates for {key} in directory tree"
                    )

                # set values if instrument not already set
                if options.INSTRUMENTS == 1:
                    config[key] = work_dict[key]

                else:
                    raise NotImplementedError(
                        "[jobrunner] Not configured with instruments. Please reinstall with releveant options"
                    )

                continue

            # loop over subkey and values
            for subkey, work_obj in work_dict[key].items():

                # test combination of values here to get absolute path for setup and submit scripts
                if f"{key}.{subkey}" in [
                    "job.setup",
                    "job.submit",
                    "job.input",
                ]:

                    # convert to a list if single entry
                    if not isinstance(work_obj, list):
                        raise ValueError(f"[jobrunner] {key}.{subkey} should be a list")

                    # set absolute paths
                    work_obj = [
                        os.path.dirname(jobfile) + os.sep + value for value in work_obj
                    ]

                    # check paths and raise error as appropriate
                    # for value in work_obj:
                    #    if not os.path.exists(value):
                    #        raise ValueError(f"[jobrunner]: {value} does not exist")

                # absolute path for job.target
                if f"{key}.{subkey}" in [
                    "job.target",
                ]:
                    # some checks to enforce design consistency
                    if isinstance(work_obj, list):
                        raise ValueError(f"[jobrunner] {key}.{subkey} cannot be a list")

                    work_obj = os.path.dirname(jobfile) + os.sep + work_obj

                    # check paths and raise error as appropriate
                    # if not os.path.exists(work_obj):
                    #    raise ValueError(f"[jobrunner]: {work_obj} does not exist")

                if f"{key}.{subkey}" in [
                    "job.archive",
                    "job.clean",
                ]:
                    # convert to a list
                    # if single entry
                    if not isinstance(work_obj, list):
                        raise ValueError(f"[jobrunner] {key}.{subkey} should be a list")

                    # set absolute paths
                    work_obj = [
                        os.path.dirname(jobfile) + os.sep + value for value in work_obj
                    ]

                    temp_obj = []
                    for value in work_obj:
                        temp_obj.extend(glob.glob(value))

                    work_obj = [*set(temp_obj)]

                # test combination of values here to handle exceptions
                if f"{key}.{subkey}" in [
                    "schedular.command",
                    "job.target",
                ]:

                    # some checks to enforce design consistency
                    if isinstance(work_obj, list):
                        raise ValueError(f"[jobrunner] {key}.{subkey} cannot be a list")

                    # check if main dictionary already contains definitions for [key][subkey]
                    # and enforce design requirements
                    if config[key][subkey]:
                        raise ValueError(
                            f"[jobrunner] Found duplicates for {key}.{subkey} in directory tree"
                        )

                    # set values if [key][subkey] not already set
                    config[key][subkey] = work_obj

                else:
                    # extend main dictionary
                    config[key][subkey].extend(work_obj)

    # perform checks to enforce design constraints for job.input and job.target
    if config["job"]["input"] and config["job"]["target"]:

        targetdir = os.path.dirname(config["job"]["target"])
        inputdir = os.path.dirname(config["job"]["input"][0])

        if len(targetdir) < len(inputdir):
            raise ValueError(
                f'[jobrunner] job.target: {config["job"]["target"]} should not exist'
                + "before job.input is defined in Jobfile"
            )

    for key in config.keys():
        if key != "instrument":
            config[key] = SimpleNamespace(**config[key])

    config = SimpleNamespace(**config)

    return config


def GetNodeList(basedir, workdir, node_object=""):
    """
    Get a list of paths containing an object
    with name node_object between basedir and workdir

    Arguments
    ---------
    basedir     :  Base directory (top level) of a project
    workdir     :  Current job directory
    node_object :  Name of the directory object

    Returns
    --------
    object_list :   A list of path containing the object
    """

    # get a list of directory levels between `basedir` and `workdir`
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
        object_path = current_level + os.sep + node_object

        # append to object_list
        # if path exists
        if os.path.exists(object_path):
            object_list.append(os.path.abspath(object_path))

    return object_list
