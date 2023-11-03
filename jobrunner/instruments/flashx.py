"""Script to create input files"""

import os
import toml


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

            # Indicate which key the following runtime parameters belong to
            parfile.write(f"\n# Runtime parameters for {group}\n")

            # Loop over values in the corresponding keys and start populating
            for key, value in input_dict[group].items():

                # Check if value is a dictionary or not. Dictionaries represent
                # more complex configuration which will not be handled.
                if type(value) == dict:
                    print(
                        f"[jobrunner] {group}.{key} is a dictionary and will not be handled "
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
