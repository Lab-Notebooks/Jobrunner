# Standard libraries
import os
import subprocess

# Feature libraries
import toml
import click

from . import jobrunner
from .. import lib


@jobrunner.command(name="submit")
@click.argument("workdir", default=None, type=str)
def submit(workdir):
    """
    Command to submit a job from a working directory
    """
    # Get base directory
    basedir = os.getcwd()

    # chdir to working directory
    os.chdir(workdir)
    workdir = os.getcwd()

    # Build `job` dictionary
    print(f"Parsing job.toml")
    main_dict = lib.parseJobToml(basedir, workdir)

    # Build inputfile
    print(f"Running config scripts")
    lib.runConfigScripts(main_dict)

    # Build inputfile
    print(f'Creating input file: {workdir + "/" + main_dict["job"]["input"]}')
    lib.createInputFile(main_dict)

    # Build jobfile
    print(f'Creating job file: {workdir + "/" + "job.sh"}')
    lib.createJobFile(main_dict)

    # Submit job
    print("Submitting job")

    subprocess.run(f'{main_dict["job"]["schedular"]} job.sh', shell=True, check=True)


@jobrunner.command(name="clean")
@click.argument("workdir_list", default=None, type=str, nargs=-1)
def clean(workdir_list):
    """
    Command to clean artifacts from working directory
    """
    # Get base directory
    basedir = os.getcwd()

    # run cleanup
    for workdir in workdir_list:

        main_dict = lib.parseJobToml(basedir, workdir)

        process = subprocess.run(
            f'rm -vf {workdir + "/" + main_dict["job"]["input"]} {workdir + "/" + "job.sh"}',
            shell=True,
            check=True,
        )
