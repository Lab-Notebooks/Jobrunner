"""Script for Flash-X specific instrumentation"""

import os
import toml
import numpy
import h5py
from scipy.stats import qmc

PREFERRED_KEYWORDS = ["Heater"]

UNIT_KEYWORDS = [
    "Simulation",
    "Grid",
    "Driver",
    "IncompNS",
    "HeatAD",
    "Multiphase",
    "Hydro",
    "Eos",
    "SolidMechanics",
    "ImBound",
    "Gravity",
    "RadTrans",
    "Spacetime",
    "TimeAdvance",
    "IO",
    "Particles",
    "PhysicalConstants",
    "Logfile",
    "Timers",
    "Profiler",
    "Burn",
]


def Run(config):
    """
    This is the public call for Flash-X specific instrumentation which is called indirectly
    from instruments.Run dictionary. The method invokes private methods that enforce constraints
    and perform book keeping for experiments
    """

    # Get the dictionary from Flash-X setup_params file to enforce TOML file design
    params_dict = __GetInputDict(config)

    # Now create input files use params dictionary to enforce design of TOML files
    __CreateParfile(config, params_dict)
    __CreateHeater(config, params_dict)


def __GetInputDict(config):
    """
    Build a dictionary to map runtime parameters to keywords for units and verify that
    input dictionary follows the required rules. This is done to enforce constraints on
    TOML file design. Setting up experiments that exactly map parameters to unit keywords
    contribute towards overall understanding of the computational experiment
    """
    target_dir = os.path.dirname(config.job.target)
    setup_params = target_dir + os.sep + "setup_params"

    if not os.path.exists(setup_params):
        raise FileNotFoundError(
            "[jobrunner] Cannot find Flash-X setup_params file in "
            + f'{target_dir.replace(config.job.basedir,"<ROOT>")}'
        )

    # Start with opening the parameter file generated by the setup
    # script and reading lines as a list of strings
    with open(setup_params, "r") as params_file:
        params = params_file.readlines()

    # Set default range for indices and counter
    index_range = numpy.zeros([100, 2], dtype=int)
    index_counter = -1

    # Loop over the list of lines and start applying logic to find indices
    # of lines that store runtime parameters for individual units
    for index, line in enumerate(params):

        # Skip the first index
        if index == 0:
            continue

        # Logic for populating ranges for runtime parameters, based on
        # their relative location to a new line character
        if line[0] != " ":
            if line[0] != "\n" and params[index - 1][0] == "\n":
                index_counter = index_counter + 1
                index_range[index_counter, 0] = index

            if line[0] == "\n" and params[index - 1][0] != "\n":
                index_range[index_counter, 1] = index - 1

    # Now create an empty dictionary for parameters. This dictionary will be compared to
    # input dictionary to enforce design rules.
    params_dict = {}

    # Loop over number of units identified above. We will deal with each unit separately
    for unit_index in range(index_counter):

        # Empty group key to associate the unit with (this will be populated below), and
        # relative path to parsed from the list of lines in params file
        group_key = []
        unit_path = params[index_range[unit_index, 0]].strip("\n")

        # Loop over individual group in specified keywords and then perform checks to see
        # if the group name is present in the relative path to the unit
        for group in UNIT_KEYWORDS:
            if group in unit_path:
                group_key = group

        # Handle exceptions here for preferred keywords
        for group in PREFERRED_KEYWORDS:
            if group in unit_path:
                group_key = group

        # If by this point group_key does not have any value, then we have encountered
        # a an unregistered Flash-X unit which will require updates in jobrunner
        if not group_key:
            raise ValueError(
                f"[jobrunner] Cannot find a matching keyword for {unit_path}. "
                + "This unit should be registered as keyword under jobrunner/instruments/flashx"
            )

        # If we are here then we have associated the unit with a registered group. Now
        # parse between the index ranges to populate params_dict
        for index in range(
            index_range[unit_index, 0] + 1, index_range[unit_index, 1] + 1
        ):
            if len(params[index]) > 4:
                if params[index][:4] == " " * 4 and params[index][4] != " ":
                    if group_key in params_dict:
                        params_dict[group_key].append(params[index].split()[0])
                    else:
                        params_dict[group_key] = [params[index].split()[0]]

    return params_dict


def __CreateParfile(config, params_dict):
    """
    Create a runtime parameter file for Flash-X by parsing
    the dictionary contained in job.input. This functionality
    will only be available when the "instrument" flag is present
    in Jobfile.
    """
    # Load TOML dictionary for JobWorkDir/job.input, JobWorkDir is a
    # reserved environment variable for
    input_dict = toml.load(config.job.workdir + os.sep + "job.input")

    # Open flash.par in write mode in JobWorkDir, reserved environment
    # variable for working node along the directory tree.
    with open(config.job.workdir + os.sep + "flash.par", "w") as parfile:

        # Add a comment to the parfile to indicate that this was generated
        # using a tool. Add warning to note that this can be replaced and should
        # be copied to a new location or renamed before making changes.
        parfile.write(
            "# Programmatically generated parfile for Flash-X. Copy before editing.\n"
        )

        # Loop over keys in the input dictionary to and start building the parfile
        for group in input_dict:

            if group not in UNIT_KEYWORDS + PREFERRED_KEYWORDS:
                raise ValueError(
                    f'[jobrunner] Group "{group}" does not belong to Flash-X unit keywords\n'
                    + f"{UNIT_KEYWORDS + PREFERED_KEYWORDS}"
                )

            # Indicate which key the following runtime parameters belong to
            parfile.write(f"\n# Runtime parameters for {group}\n")

            # Loop over values in the corresponding keys and start populating
            for key, value in input_dict[group].items():

                for param_group in params_dict:
                    for param_key in params_dict[param_group]:
                        if key == param_key:
                            ref_group = param_group

                if not ref_group:
                    raise ValueError(
                        f'[jobrunner] Cannot match "{group}.{key}" to setup_params'
                    )

                # Check if value is a dictionary or not. Dictionaries represent
                # more complex configuration which will not be handled.
                if type(value) == dict:
                    print(
                        f'{" "*4}[jobrunner] {group}.{key} is a dictionary and will not be handled '
                        + "during Flash-X parfile generation"
                    )

                elif group != ref_group:
                    raise ValueError(
                        f'[jobrunner] parameter "{key}" associated with "{group}" belongs '
                        + f'to "{ref_group}". Please fix your toml files along the directory tree.'
                    )

                else:
                    # Deal with True/False values
                    if isinstance(value, bool):
                        parfile.write(f"{key} = .{str(value).upper()}.\n")

                    # Deal with strings
                    elif type(value) == str:
                        parfile.write(f'{key} = "{value}"\n')

                    # Deal with rest
                    else:
                        parfile.write(f"{key} = {value}\n")


def __CreateHeater(config, params_dict):
    """
    Create hdf5 input files based on heater configuration. This functionality
    is only available when "instrument" is defined in the Jobfile, and jobrunner
    is installed with the option --with-instrument
    """
    # Load TOML dictionary for JobWorkDir/job.input, JobWorkDir is a
    # reserved environment variable for
    input_dict = toml.load(config.job.workdir + os.sep + "job.input")

    # Loop over keys in the input dictionary and handle errors based
    # on case sensitivity and group definitions. Set an exit flag to
    # determin if we need to safely exit out of this subroutine
    exit_flag = False
    for group in input_dict:

        # Check case sensitivity first and raise value error
        if group.upper() == "HEATER" and group != "Heater":
            raise ValueError(f'[jobrunner] Group "{group}" should be "Heater"')

        # If group exactly matches heater then set exit flag to false
        # and break the loop and continue with rest of the computations
        elif group == "Heater":
            exit_flag = False
            break

        # If above conditions do not meet then set exit flag to true
        # and continue the loop to check for rest of the groups
        else:
            exit_flag = True
            continue

    # Return immediately if exit flag is true
    if exit_flag:
        return

    # If we are here then Heater is present in the input dictionary
    # and we can safely load the corresponding heater dictionary
    heater_dict = input_dict["Heater"]

    # Set a counter to track how many heater files are being written
    # and then loop over items in heater dictionary
    num_heaters = 0
    for key, info in heater_dict.items():

        # if info is of type dictionary we have hit a heater configuration
        # that needs to be written to a file. Start implementing that logic
        if type(info) == dict:

            # Increase heater counter to track number of heaters
            num_heaters = num_heaters + 1

            # Raise error if the heater key does not match
            # expected naming convention
            if str(num_heaters).zfill(4) != key:
                raise ValueError(
                    f'[jobrunner] Heater "{key}" does not match "{str(num_heaters).zfill(4)}"'
                )

            # Set filename and open the hdf5 file in write mode
            filename = (
                config.job.workdir
                + os.sep
                + heater_dict["sim_heaterName"]
                + "_hdf5_htr_"
                + key
            )
            hfile = h5py.File(filename, "w")

            xsite = numpy.ndarray([info["numSites"]], dtype=float)
            ysite = numpy.ndarray([info["numSites"]], dtype=float)
            zsite = numpy.ndarray([info["numSites"]], dtype=float)
            radii = numpy.ndarray([info["numSites"]], dtype=float)

            if info["numSites"] == 1:
                xsite[:] = 0.0
                ysite[:] = 1e-13
                zsite[:] = 0.0
                radii[:] = 0.2

            else:
                halton = qmc.Halton(d=2, seed=1)
                sample = halton.random(info["numSites"])

                xsite[:] = info["xmin"] + sample[:, 0] * (info["xmax"] - info["xmin"])
                ysite[:] = 1e-13
                radii[:] = 0.2

                if info["dim"] == 1:
                    zsite[:] = 0.0
                elif info["dim"] == 2:
                    zsite[:] = info["zmin"] + sample[:, 1] * (
                        info["zmax"] - info["zmin"]
                    )
                else:
                    raise ValueError(f"[jobrunner] Error in HEATER.{key}.dim")

            hfile.create_dataset(
                "heater/xMin", data=info["xmin"], shape=(1), dtype="float32"
            )
            hfile.create_dataset(
                "heater/xMax", data=info["xmax"], shape=(1), dtype="float32"
            )
            hfile.create_dataset(
                "heater/zMin", data=info["zmin"], shape=(1), dtype="float32"
            )
            hfile.create_dataset(
                "heater/zMax", data=info["zmax"], shape=(1), dtype="float32"
            )
            hfile.create_dataset(
                "heater/yMin", data=info["ymin"], shape=(1), dtype="float32"
            )
            hfile.create_dataset(
                "heater/yMax", data=info["ymax"], shape=(1), dtype="float32"
            )
            hfile.create_dataset(
                "heater/wallTemp",
                data=info["wallTemp"],
                shape=(1),
                dtype="float32",
            )
            hfile.create_dataset(
                "heater/advAngle",
                data=info["advAngle"],
                shape=(1),
                dtype="float32",
            )
            hfile.create_dataset(
                "heater/rcdAngle",
                data=info["rcdAngle"],
                shape=(1),
                dtype="float32",
            )
            hfile.create_dataset(
                "heater/velContact",
                data=info["velContact"],
                shape=(1),
                dtype="float32",
            )
            hfile.create_dataset(
                "heater/nucWaitTime",
                data=info["nucWaitTime"],
                shape=(1),
                dtype="float32",
            )
            hfile.create_dataset(
                "site/num", data=info["numSites"], shape=(1), dtype="int32"
            )
            hfile.create_dataset(
                "site/x", data=xsite, shape=(info["numSites"]), dtype="float32"
            )
            hfile.create_dataset(
                "site/y", data=ysite, shape=(info["numSites"]), dtype="float32"
            )
            hfile.create_dataset(
                "site/z", data=zsite, shape=(info["numSites"]), dtype="float32"
            )
            hfile.create_dataset(
                "init/radii",
                data=radii,
                shape=(info["numSites"]),
                dtype="float32",
            )
            hfile.close()

            print(
                f'{" "*4}[jobrunner] Wrote Heater information to file '
                + f'{filename.replace(config.job.workdir + os.sep,"")}'
            )

    if num_heaters != heater_dict["sim_numHeaters"]:
        raise ValueError(
            f"[jobrunner] Number of heater files not equal to sim_numHeaters"
        )
