"""Command line interface for Jobrunner"""

# Standard libraries
import sys
import subprocess
if sys.version_info < (3, 8):
    import pkg_resources
else:
    from importlib import metadata

# Feature libraries
import click


@click.group(name="jobrunner", invoke_without_command=True)
@click.pass_context
@click.option("--version", "-v", is_flag=True)
def jobrunner(ctx, version):
    """
    \b
    Command line tool to organize and manage computing jobs.
    """
    if ctx.invoked_subcommand is None and not version:
        subprocess.run(
            "jobrunner --help",
            shell=True,
            check=True,
        )

    if version:
        if sys.version_info < (3, 8):
            jobrunner_version = pkg_resources.require("PyJobrunner")[0].version
        else:
            jobrunner_version = metadata.version("PyJobrunner")
        click.echo(jobrunner_version)
