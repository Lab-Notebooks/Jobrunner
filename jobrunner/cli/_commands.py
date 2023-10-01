"""Command line interface for Jobrunner"""

# Standard libraries
import os
import sys
import subprocess
from datetime import date

# Feature libraries
import click
from alive_progress import alive_bar

from jobrunner.cli import jobrunner
from jobrunner import lib


class Colors:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


@jobrunner.command(name="setup")
@click.argument("workdir_list", required=True, nargs=-1, type=str)
@click.option(
    "--verbose", "-V", is_flag=True, help="print execution output on the terminal"
)
def setup(workdir_list, verbose):
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
    # Get base directory
    basedir = os.getcwd()

    # loop over workdir_list
    for workdir in workdir_list:

        # chdir to working directory
        print(
            "#######################################################################################################"
        )
        os.chdir(workdir)
        workdir = os.getcwd()
        print("➜ " + Colors.PURPLE + "node: " + Colors.BLUE + f"{workdir}" + Colors.END)

        # Build main dictionary
        print("➜ " + Colors.PURPLE + "root: " + Colors.BLUE + f"{basedir}" + Colors.END)
        main_dict = lib.ParseJobConfig(basedir, workdir)

        # Create setup file
        lib.CreateSetupFile(main_dict)

        # Print configuration details
        print("\n" + Colors.PURPLE + "job.setup:" + Colors.END)
        for value in main_dict["job"]["setup"]:
            print("➜ " + Colors.BLUE + f"{value}" + Colors.END)

        print(
            "\n"
            + "➜ "
            + Colors.PURPLE
            + "executing:"
            + Colors.BLUE
            + f"{workdir}/job.setup"
            + Colors.END
        )

        process = subprocess.Popen(
            "bash job.setup".split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        with open("job.output", "w") as output:

            if not verbose:
                with alive_bar(
                    spinner="waves", bar=None, stats=False, monitor=False
                ) as bar:
                    while process.poll() == None:
                        bar()
                        output.write(process.stdout.readline())
            else:
                while process.poll() == None:
                    line = process.stdout.readline()
                    print(line.strip("\n"))
                    output.write(line)

        if process.returncode != 0:
            if not verbose:
                with open("job.output", "r") as output:
                    print("".join(output.readlines()[-8:]))

            print(Colors.RED + "FAILURE" + Colors.END)
        else:
            print(Colors.GREEN + "SUCCESS" + Colors.END)

        print(
            "\n"
            + "➜ "
            + Colors.PURPLE
            + "output:"
            + Colors.BLUE
            + f"{workdir}/job.output"
            + Colors.END
        )

        # Return to base directory
        os.chdir(basedir)


@jobrunner.command(name="submit")
@click.argument("workdir_list", required=True, nargs=-1, type=str)
def submit(workdir_list):
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
    # Get base directory
    basedir = os.getcwd()

    # loop over workdir_list
    for workdir in workdir_list:

        # chdir to working directory
        print(
            "#######################################################################################################"
        )
        os.chdir(workdir)
        workdir = os.getcwd()
        print("➜ " + Colors.PURPLE + "node: " + Colors.BLUE + f"{workdir}" + Colors.END)

        # Build main dictionary
        print("➜ " + Colors.PURPLE + "root: " + Colors.BLUE + f"{basedir}" + Colors.END)
        main_dict = lib.ParseJobConfig(basedir, workdir)

        # Build inputfile
        lib.CreateInputFile(main_dict)
        print("\n" + Colors.PURPLE + "job.input:" + Colors.END)
        for value in main_dict["job"]["input"]:
            print("➜ " + Colors.BLUE + f"{value}" + Colors.END)

        # Build targetfile
        lib.CreateTargetFile(main_dict)
        print("\n" + Colors.PURPLE + "job.target:" + Colors.END)
        print("➜ " + Colors.BLUE + f'{main_dict["job"]["target"]}' + Colors.END)

        # Build submitfile
        lib.CreateSubmitFile(main_dict)
        print("\n" + Colors.PURPLE + "job.submit:" + Colors.END)
        for value in main_dict["job"]["submit"]:
            print("➜ " + Colors.BLUE + f"{value}" + Colors.END)

        # Submit job
        if main_dict["schedular"]["command"] == "bash":
            subprocess.run(
                f'{main_dict["schedular"]["command"]} job.submit > job.output 2>&1',  # > /dev/null 2>&1 &',
                shell=True,
                check=True,
            )

        else:
            subprocess.run(
                f'{main_dict["schedular"]["command"]} job.submit',
                shell=True,
                check=True,
            )

        # Return to base directory
        os.chdir(basedir)


@jobrunner.command(name="clean")
@click.argument("workdir_list", required=True, nargs=-1, type=str)
def clean(workdir_list):
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
    # Get base directory
    basedir = os.getcwd()

    # run cleanup
    for workdir in workdir_list:

        # chdir to working directory
        print(
            "#######################################################################################################"
        )
        os.chdir(workdir)
        workdir = os.getcwd()
        print("➜ " + Colors.PURPLE + "node: " + Colors.BLUE + f"{workdir}" + Colors.END)

        # Build main dictionary
        print("➜ " + Colors.PURPLE + "root: " + Colors.BLUE + f"{basedir}" + Colors.END)
        main_dict = lib.ParseJobConfig(basedir, workdir)

        print("➜ " + Colors.PURPLE + "cleaning" + Colors.END)
        lib.RemoveNodeFiles(main_dict, workdir)

        os.chdir(basedir)


@jobrunner.command(name="archive")
@click.option(
    "--tag", "-t", help="name of the archive", default=str(date.today()), type=str
)
@click.argument("workdir_list", required=True, nargs=-1, type=str)
def archive(tag, workdir_list):
    """
    \b
    Create an archive along a directory tree
    \b
    """
    # Get base directory
    basedir = os.getcwd()

    # loop over workdir_list
    for workdir in workdir_list:

        # chdir to working directory
        print(
            "#######################################################################################################"
        )
        os.chdir(workdir)
        workdir = os.getcwd()
        print("➜ " + Colors.PURPLE + "node: " + Colors.BLUE + f"{workdir}" + Colors.END)

        # Build main dictionary
        print("➜ " + Colors.PURPLE + "root: " + Colors.BLUE + f"{basedir}" + Colors.END)
        main_dict = lib.ParseJobConfig(basedir, workdir)

        # Create archive
        print(
            "➜ "
            + Colors.PURPLE
            + "archiving: "
            + Colors.BLUE
            + f"jobnode.archive/{tag}"
            + Colors.END
        )
        lib.CreateArchive(main_dict, tag)

        # Return to base directory
        os.chdir(basedir)


@jobrunner.command(name="export")
@click.option(
    "--tag", "-t", help="name of the archive", default=str(date.today()), type=str
)
@click.argument("workdir_list", required=True, nargs=-1, type=str)
def export(tag, workdir_list):
    """
    \b
    Export directory tree to an external folder
    \b
    """
    # Get base directory
    basedir = os.getcwd()

    # loop over workdir_list
    for workdir in workdir_list:

        # chdir to working directory
        print(
            "#######################################################################################################"
        )
        os.chdir(workdir)
        workdir = os.getcwd()
        print("➜ " + Colors.PURPLE + "node: " + Colors.BLUE + f"{workdir}" + Colors.END)

        # Build main dictionary
        print("➜ " + Colors.PURPLE + "root: " + Colors.BLUE + f"{basedir}" + Colors.END)
        main_dict = lib.ParseJobConfig(basedir, workdir)

        # Create archive
        print(
            "➜ " + Colors.PURPLE + "exporting: " + Colors.BLUE + f"{tag}" + Colors.END
        )
        lib.ExportTree(main_dict, tag)

        # Return to base directory
        os.chdir(basedir)


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
