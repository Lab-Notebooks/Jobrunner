"""Command line interface for Jobrunner"""

# Standard libraries
from datetime import date

# Feature libraries
import click

from jobrunner.cli import jobrunner
from jobrunner import api


@jobrunner.command(name="setup")
@click.argument("dirlist", required=True, nargs=-1, type=str)
@click.option(
    "--verbose", "-V", is_flag=True, help="print execution output on the terminal"
)
def setup(dirlist, verbose):
    """
    \b
    Run setup scripts in a directory
    \b

    \b
    Jobfiles in a directory tree provide a list of
    setup scripts which are composed into a job.setup
    file and run along the directory tree
    \b

    \b
    Bash Variables
    --------------
    JobWorkDir - Path to working directory of the job
    """
    api.setup(dirlist, verbose)


@jobrunner.command(name="submit")
@click.argument("dirlist", required=True, nargs=-1, type=str)
@click.option(
    "--verbose", "-V", is_flag=True, help="print execution output on the terminal"
)
def submit(dirlist, verbose):
    """
    \b
    Submit a job from a directory
    \b

    \b
    Jobfiles in a directory tree provide a list of
    submit scripts which are composed into a job.submit
    file for linux schedulars
    \b

    \b
    Bash Variables
    --------------
    JobWorkDir - Path to working directory of the job
    """
    api.submit(dirlist, verbose)


@jobrunner.command(name="clean")
@click.argument("dirlist", required=True, nargs=-1, type=str)
def clean(dirlist):
    """
    \b
    Remove artifacts from a directory
    \b

    \b
    This command removes job.input, job.target,
    job.setup, and job.submit files from a
    working directory
    \b
    """
    api.clean(dirlist)


@jobrunner.command(name="archive")
@click.option(
    "--tag", "-t", help="name of the archive", default=str(date.today()), type=str
)
@click.argument("dirlist", required=True, nargs=-1, type=str)
def archive(tag, dirlist):
    """
    \b
    Create an archive along a directory tree
    \b
    """
    api.archive(tag, dirlist)


@jobrunner.command(name="export")
@click.option(
    "--dest",
    "-d",
    help="path to destination archive",
    default=str(date.today()),
    type=str,
)
@click.argument("dirlist", required=True, nargs=-1, type=str)
def export(dest, dirlist):
    """
    \b
    Export directory tree to an external folder
    \b
    """
    api.export(dest, dirlist)


@jobrunner.command(name="diff")
@click.argument("file1", type=str, required=True)
@click.argument("file2", type=str, required=True)
def diff(file1, file2):
    """
    Run diff on two files
    """
    subprocess.run(
        f"export PATH=~/.local/bin:/usr/local/bin:$PATH && logdiff {file1} {file2}",
        shell=True,
        check=True,
    )
