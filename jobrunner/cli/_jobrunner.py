# Standard libraries
import os
import subprocess

# Feature libraries
import toml
import click

from .. import lib

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

    return_code = lib.createInputFile(job, workdir)
    if return_code != 0:
        raise ValueError()

    # Build jobfile
    print(f'Creating job file: {workdir + "/" + jobscript}')

    return_code = lib.createJobFile(job, jobscript, workdir)
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
