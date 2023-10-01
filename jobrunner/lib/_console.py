# Standard libraries
import subprocess

# Feature libraries
from alive_progress import alive_bar

# Local imports
from jobrunner import lib


def DisplayTree(workdir, basedir=None):
    """
    Display tree information on console
    """
    print(
        "#######################################################################################################"
    )

    print(f"➜ {lib.Color.purple}node: {lib.Color.blue}{workdir} {lib.Color.end}")

    if basedir:
        print(f"➜ {lib.Color.purple}root: {lib.Color.blue}{basedir} {lib.Color.end}")


def SchedularProcess(workdir, command, script):
    """
    Submit job using a schedular
    """
    print(
        f"\n➜ {lib.Color.purple}scheduling: {lib.Color.blue}{workdir}/{script} {lib.Color.end}"
    )

    process = subprocess.run(
        f"{command} {script}",
        shell=True,
        check=True,
    )


def BashProcess(workdir, script, verbose=False):
    """
    Run a bash process based on input configuration
    """
    print(
        f"\n➜ {lib.Color.purple}executing: {lib.Color.blue}{workdir}/{script} {lib.Color.end}"
    )

    process = subprocess.Popen(
        f"bash {script}".split(),
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

        print(f"{lib.Color.red}FAILURE {lib.Color.end}")
    else:
        print(f"{lib.Color.green}SUCCESS {lib.Color.end}")

    print(
        f"\n➜ {lib.Color.purple}output: {lib.Color.blue}{workdir}/job.output {lib.Color.end}"
    )
