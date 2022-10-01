# Standard libraries
import os
import subprocess

# Feature libraries
import toml
import click


@click.group(name="jobrunner")
def jobrunner():
    """
    CLI for managing simulations jobs
    """
    pass


@jobrunner.command(name="submit")
@click.argument("workdir", default=None, type=str)
def submit(workdir):
    """
    Command to submit a job from a working directory
    """
    # Read TOML file and replace
    job = toml.load("job.toml")
    jobscript = "job.sh"

    # Get current directory
    os.chdir(workdir)
    workdir = os.getcwd()

    # Build inputfile
    print(f'Creating input file: {workdir + "/" + job["inputfile"]}')

    return_code = _createInputFile(job, workdir)
    if return_code != 0:
        raise ValueError()

    # Build jobfile
    print(f'Creating job file: {workdir + "/" + jobscript}')

    return_code = _createJobFile(job, jobscript, workdir)
    if return_code != 0:
        raise ValueError()

    # Submit job
    print("Submitting job")

    subprocess.run(f'{job["schedular"]} {jobscript}', shell=True, check=True)


@jobrunner.command(name="clean")
@click.argument("workdir", default=None, type=str, nargs=-1)
def clean(workdir):
    """
    Command to clean artifacts from working directory
    """
    job = toml.load("job.toml")
    jobscript = "job.sh"

    # run cleanup
    for dir_ in workdir:
        job["name"] = dir_.split("/")[-1] + ".sh"
        process = subprocess.run(
            f'rm -vf {dir_ + "/" + job["inputfile"]} {dir_ + "/" + jobscript}',
            shell=True,
            check=True,
        )


def _createInputFile(job, workdir):
    """
    create an input file for a given simulation recursively using
    `job.input` between `basedir` and `workdir`

    `job`     :  Job dictionary
    `workdir` :  Current job directory
    """
    # get inputfile_list from internal method
    inputfile_list = _getFileList(job["basedir"], workdir, "job.input")

    # run a subprocess to build flash.par
    process = subprocess.run(
        f'rm -f {job["inputfile"]} && cat {" ".join(inputfile_list)} > {job["inputfile"]}',
        shell=True,
        check=True,
    )

    return process.returncode


def _createJobFile(job, jobscript, workdir):
    """
    create `jobrunner.sh` for a given simulation recursively using
    `inputfile` between `basedir` and `workdir`

    `job`       :  Job dictionary
    `jobscript` : Job script file
    `workdir`   :  Current job directory
    """
    # get config_list and submit_list from internal method
    config_list = _getFileList(job["basedir"], workdir, "job.config")
    submit_list = _getFileList(job["basedir"], workdir, "job.submit")

    # set header for the submit script
    with open(workdir + "/" + jobscript, "w") as jobfile:
        jobfile.write("#!/bin/bash\n\n")

    # run the subprocess
    process = subprocess.run(
        f'cat {" ".join(submit_list)} {" ".join(config_list)} >> {jobscript}',
        shell=True,
        check=True,
    )

    return process.returncode


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
