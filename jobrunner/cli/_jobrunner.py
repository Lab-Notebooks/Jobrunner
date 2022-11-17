# Standard libraries
import os
import subprocess
import pkg_resources

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
            f'export PATH=~/.local/bin:/usr/local/bin:$PATH && jobrunner --help',
            shell=True,
            check=True,
        )

    if version:
        click.echo(pkg_resources.require("PyJobrunner")[0].version)
