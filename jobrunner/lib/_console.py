# Standard libraries
import os
import sys
import subprocess

# Feature libraries
from alive_progress import alive_bar

# Local imports
from jobrunner import lib


def ConsoleSeparator():
    try:
        print(os.get_terminal_size().columns * "—")
    except:
        print(100 * "—")


def DisplayTree(basedir, workdir):
    """
    Display tree information on console
    """
    print(f"{lib.Color.purple}ROOT:{lib.Color.end} {basedir}")
    print(f'{lib.Color.purple}NODE:{lib.Color.end} {workdir.replace(basedir,"<ROOT>")}')


def SchedularProcess(basedir, workdir, command, script):
    """
    Submit job using a schedular
    """
    print(
        f'\n{lib.Color.purple}SUBMIT:{lib.Color.end} {workdir.replace(basedir,"<ROOT>")}/{script}'
    )

    process = subprocess.run(
        f"{command} {script}",
        shell=True,
        check=True,
    )


def BashProcess(basedir, workdir, script, verbose=False):
    """
    Run a bash process based on input configuration
    """
    print(
        f'\n{lib.Color.purple}EXECUTE:{lib.Color.end} {workdir.replace(basedir,"<ROOT>")}/{script}'
    )

    if verbose:
        process = subprocess.Popen(
            f"bash {script}".split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        with open("job.output", "w") as output:
            while process.poll() == None:
                line = process.stdout.readline()
                print(line.strip("\n"))
                output.write(line)

    else:
        with open("job.output", "w") as output:
            process = subprocess.Popen(
                f"bash {script}".split(),
                stdout=output,
                stderr=subprocess.STDOUT,
                text=True,
            )

        with alive_bar(spinner="waves", bar=None, stats=False, monitor=False) as bar:
            while process.poll() == None:
                bar()

    if process.returncode != 0:
        if not verbose:
            with open("job.output", "r") as output:
                print("".join(output.readlines()[-8:]))

        print(f"{lib.Color.red}FAILURE {lib.Color.end}")
    else:
        print(f"{lib.Color.green}SUCCESS {lib.Color.end}")

    print(
        f'\n{lib.Color.purple}OUTPUT:{lib.Color.end} {workdir.replace(basedir,"<ROOT>")}/job.output'
    )
