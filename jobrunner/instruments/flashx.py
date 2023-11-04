"""Script to create input files"""

import os
import toml
import numpy
import h5py
from scipy.stats import qmc


def CreateParfile(workdir):
    """
    Create a runtime parameter file for Flash-X by parsing
    the dictionary contained in job.input. This functionality
    will only be available when the "instrument" flag is present
    in Jobfile.
    """
    # Load TOML dictionary for JobWorkDir/job.input, JobWorkDir is a
    # reserved environment variable for
    input_dict = toml.load(workdir + os.sep + "job.input")

    # Open flash.par in write mode in JobWorkDir, reserved environment
    # variable for working node along the directory tree.
    with open(workdir + os.sep + "flash.par", "w") as parfile:

        # Add a comment to the parfile to indicate that this was generated
        # using a tool. Add warning to note that this can be replaced and should
        # be copied to a new location or renamed before making changes.
        parfile.write(
            "# Programmatically generated parfile for Flash-X. Copy before editing.\n"
        )

        # Loop over keys in the input dictionary to and start building the parfile
        for group in input_dict:

            if not group.isupper():
                raise ValueError(f'[jobrunner] Group "{group}" should be uppercase')

            # Indicate which key the following runtime parameters belong to
            parfile.write(f"\n# Runtime parameters for {group}\n")

            # Loop over values in the corresponding keys and start populating
            for key, value in input_dict[group].items():

                # Check if value is a dictionary or not. Dictionaries represent
                # more complex configuration which will not be handled.
                if type(value) == dict:
                    print(
                        f'{" "*4}[jobrunner] {group}.{key} is a dictionary and will not be handled '
                        + "during Flash-X parfile generation"
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


def CreateHeater(workdir):
    """
    Create hdf5 input files based on heater configuration. This functionality
    is only available when "instrument" is defined in the Jobfile, and jobrunner
    is installed with the option --with-instrument
    """
    # Load TOML dictionary for JobWorkDir/job.input, JobWorkDir is a
    # reserved environment variable for
    input_dict = toml.load(workdir + os.sep + "job.input")

    # Return immediately if HEATER not present in input dictionary
    if "HEATER" not in input_dict.keys():
        return

    # If we are here then HEATER is present in the input dictionary
    # and we can safely load the corresponding heater dictionary
    heater_dict = input_dict["HEATER"]

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
                workdir + os.sep + heater_dict["sim_heaterName"] + "_hdf5_htr_" + key
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
                f'{" "*4}[jobrunner] Wrote heater information to file {filename.replace(workdir + os.sep,"")}'
            )

    if num_heaters != heater_dict["sim_numHeaters"]:
        raise ValueError(
            f"[jobrunner] Number of heater files not equal to sim_numHeaters"
        )
