# Standard libraries
import os
import shutil

# local imports
from . import GetTreeList


def CreateArchive(main_dict, archive_tag):
    """
    Create an archive of artifacts along the
    in workdir defined in main dictionary

    Arguments
    ---------
    main_dict : Dictionary containing details of the
                job configuration in directory tree

    archive_tag :  Tag for the archive
    """
    # get a list of directories along the
    # tree between basedir and workdir
    tree_list = GetTreeList(main_dict["basedir"], main_dict["workdir"])

    # get targetfile, setupfiles, and
    # submitfiles from main_dict
    targetfile = main_dict["config"]["target"]
    setupfile_list = [setupfile for setupfile in main_dict["config"]["setup"]]
    submitfile_list = [submitfile for submitfile in main_dict["config"]["submit"]]

    # get a list of files that are designated
    # to be ignored and should not be archived
    ignore_list = (
        [main_dict["config"]["input"]]
        + [targetfile.replace(os.path.dirname(targetfile) + os.sep, "")]
        + [
            setupfile.replace(os.path.dirname(setupfile) + os.sep, "")
            for setupfile in setupfile_list
        ]
        + [
            submitfile.replace(os.path.dirname(submitfile) + os.sep, "")
            for submitfile in submitfile_list
        ]
        + ["Jobfile", "README.md", "README.rst", "LICENSE", ".gitignore"]
    )

    # get reference to working
    # directory
    workdir = main_dict["workdir"]

    # check if archive directory already
    # exists and handle exceptions
    if os.path.exists(workdir + os.sep + archive_tag):
        print(f"Archive directory already exists in {workdir} skipping")

    # create the archive directory
    # and store results
    else:

        # create archive directory
        os.mkdir(f"{workdir + os.sep + archive_tag}")

        # get the list of
        # files in treedir
        file_list = next(os.walk(workdir), (None, None, []))[2]

        for filename in file_list:
            if filename not in ignore_list:
                shutil.move(filename, workdir + os.sep + archive_tag)
