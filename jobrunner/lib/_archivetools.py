# Standard libraries
import os
import shutil

# local imports
from . import GetNodeList


def CreateArchive(main_dict, archive_tag):
    """
    Create an archive of artifacts
    along a directory node

    Arguments
    ---------
    main_dict : Dictionary containing details of the
                job configuration in directory node

    archive_tag :  Tag for the archive
    """
    # rename archive_tag with proper extension
    archive_tag = "jobnode.archive/" + archive_tag

    # get a list of directories along the
    # node between basedir and workdir
    node_list = GetNodeList(main_dict["job"]["basedir"], main_dict["job"]["workdir"])

    for nodedir in node_list:

        os.chdir(nodedir)

        # check if archive directory already
        # exists and handle exceptions
        if os.path.exists(nodedir + os.sep + archive_tag):
            print(f"[jobrunner] {archive_tag} already exists in {nodedir} SKIPPING")

        # create the archive directory
        # and store results
        else:

            # create an empty
            # list of archive file
            archive_list = []

            # get the list of
            # files in nodedir
            nodefile_list = [
                os.path.abspath(nodefile)
                for nodefile in next(os.walk("."), (None, None, []))[2]
            ]

            # create a reference file list
            # to test which nodefile should
            # be archived
            ref_list = main_dict["job"]["archive"] + [
                nodedir + os.sep + "job.input",
                nodedir + os.sep + "job.setup",
                nodedir + os.sep + "job.submit",
            ]

            # loop over list of files in nodedir
            # and append to archive_list if file
            # is present in job.archive
            for filename in nodefile_list:
                if filename in ref_list:
                    archive_list.append(filename)

            if archive_list:
                # create archive directory
                os.makedirs(f"{nodedir + os.sep + archive_tag}")

                # loop over archive_list
                # and archive contents
                for filename in archive_list:
                    shutil.move(filename, nodedir + os.sep + archive_tag)

    # return back to working directory
    os.chdir(main_dict["job"]["workdir"])
