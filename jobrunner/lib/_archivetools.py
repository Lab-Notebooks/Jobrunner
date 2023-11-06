# Standard libraries
import os
import shutil

# local imports
from jobrunner import lib


def CreateArchive(config, archive_tag):
    """
    Create an archive of artifacts
    along a directory node

    Arguments
    ---------
    config : Dictionary containing details of the
                job configuration in directory node

    archive_tag :  Tag for the archive
    """
    # rename archive_tag with proper extension
    archive_tag = "jobnode.archive/" + archive_tag

    # get a list of directories along the node between basedir and workdir
    node_list = lib.GetNodeList(config.job.basedir, config.job.workdir)

    for nodedir in node_list:

        os.chdir(nodedir)

        # check if archive directory already exists and handle exceptions
        if os.path.exists(nodedir + os.sep + archive_tag):
            print(
                f'{" "*4}[jobrunner] {archive_tag} already exists in {nodedir} SKIPPING'
            )

        # create the archive directory and store results
        else:

            # create an empty list of archive file
            archive_list = []

            # get the list of files in nodedir
            nodefile_list = [
                os.path.abspath(nodefile)
                for nodefile in next(os.walk("."), (None, None, []))[2]
            ]

            # create a reference file list to test which nodefile should be archived
            ref_list = config.job.archive + [
                nodedir + os.sep + "job.input",
                nodedir + os.sep + "job.setup",
                nodedir + os.sep + "job.submit",
                nodedir + os.sep + "job.output",
            ]

            # loop over list of files in nodedir and append to
            # archive_list if file is present in job.archive
            for filename in nodefile_list:
                if filename in ref_list:
                    archive_list.append(filename)

            if archive_list:
                # create archive directory
                os.makedirs(f"{nodedir + os.sep + archive_tag}")

                # loop over archive_list and archive contents
                for filename in archive_list:
                    shutil.move(filename, nodedir + os.sep + archive_tag)

    # return back to working directory
    os.chdir(config.job.workdir)


def ExportTree(config, archive_tag):
    """
    Export directory tree to archive

    Arguments
    ---------
    config : Dictionary containing details of the
                job configuration in directory node

    archive_tag :  Tag for the archive
    """

    # check if workdir already exists in the archive folder
    workdir = config.job.workdir.replace(config.job.basedir, "")

    if os.path.exists(archive_tag + os.sep + workdir):
        print(f'{" "*4}[jobrunner] {workdir} already exists in {archive_tag} SKIPPING')
        return

    # get a list of directories along the node between basedir and workdir
    node_list = lib.GetNodeList(config.job.basedir, config.job.workdir)

    for nodedir in node_list:

        os.chdir(nodedir)

        # create the archive directory and store results
        # create an empty list of archive and copy file
        archive_list = []
        copy_list = []

        # get the list of files in nodedir
        nodefile_list = [
            os.path.abspath(nodefile)
            for nodefile in next(os.walk("."), (None, None, []))[2]
        ]

        # create a reference file list to test which nodefile should be archived
        ref_list = config.job.archive + [
            nodedir + os.sep + "job.input",
            nodedir + os.sep + "job.setup",
            nodedir + os.sep + "job.submit",
            nodedir + os.sep + "job.output",
            nodedir + os.sep + "jobnode.archive",
        ]

        # loop over list of files in nodedir and append to archive_list and copy_list
        for filename in nodefile_list:
            if filename in ref_list:
                archive_list.append(filename)
            else:
                copy_list.append(filename)

        # create archive directory
        os.makedirs(
            f"{archive_tag + os.sep + nodedir.replace(config.job.basedir,'')}",
            exist_ok=True,
        )

        if archive_list:
            # loop over archive_list and archive contents
            for filename in archive_list:
                shutil.move(
                    filename,
                    archive_tag + os.sep + nodedir.replace(config.job.basedir, ""),
                )

        if copy_list:
            # loop over copy_list and archive contents
            for filename in copy_list:
                if os.path.exists(
                    archive_tag
                    + os.sep
                    + nodedir.replace(config.job.basedir, "")
                    + os.sep
                    + filename.replace(nodedir, "")
                ):
                    ftrimmed = filename.replace(nodedir, "")
                    print(
                        f"[jobrunner] {nodedir.replace(config.job.basedir,'')+ ftrimmed} not copied"
                    )

                else:
                    shutil.copy(
                        filename,
                        archive_tag + os.sep + nodedir.replace(config.job.basedir, ""),
                    )

        if os.path.exists(nodedir + os.sep + "jobnode.archive"):
            shutil.move(
                nodedir + os.sep + "jobnode.archive",
                archive_tag + os.sep + nodedir.replace(config.job.basedir, ""),
            )

    # return back to working directory
    os.chdir(config.job.workdir)
