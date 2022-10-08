# Standard libraries
import os
import shutil

# feature imports
import toml

# local imports
from . import GetTreeList


def CreateArchive(main_dict, archive_tag):
    """
    Create an archive of artifacts
    along a directory tree

    Arguments
    ---------
    main_dict : Dictionary containing details of the
                job configuration in directory tree

    archive_tag :  Tag for the archive
    """
    # rename archive_tag with proper extension
    archive_tag = "job." + archive_tag + ".archive"

    # get a list of directories along the
    # tree between basedir and workdir
    tree_list = GetTreeList(main_dict["basedir"], main_dict["workdir"])

    for treedir in tree_list:

        os.chdir(treedir)

        # check if archive directory already
        # exists and handle exceptions
        if os.path.exists(treedir + os.sep + archive_tag):
            print(f"[jobrunner] {archive_tag} already exists in {treedir} SKIPPING")

        # create the archive directory
        # and store results
        else:

            # create an empty
            # list of archive file
            archive_list = []

            # get the list of
            # files in treedir
            treefile_list = [
                os.path.abspath(treefile)
                for treefile in next(os.walk("."), (None, None, []))[2]
            ]

            # create a reference file list
            # to test which treefile should
            # be archived
            ref_list = main_dict["config"]["archive"] + [
                treedir + os.sep + "job.input",
                treedir + os.sep + "job.setup",
                treedir + os.sep + "job.submit",
            ]

            # loop over list of files in treedir
            # and append to archive_list if file
            # is present in config.archive
            for filename in treefile_list:
                if filename in ref_list:
                    archive_list.append(filename)

            if archive_list:
                # create archive directory
                os.mkdir(f"{treedir + os.sep + archive_tag}")

                # loop over archive_list
                # and archive contents
                for filename in archive_list:
                    shutil.move(filename, treedir + os.sep + archive_tag)

    # return back to working directory
    os.chdir(main_dict["workdir"])
