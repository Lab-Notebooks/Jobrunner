Jobrunner
=========

Jobrunner is a command line tool to manage and deploy computing jobs, organize complex workloads, and enforce a directory based hierarchy to enable reuse of files and bash scripts within a project. Organization details of nodes in a directory tree are encoded in Jobfiles which serve as an index of files and their purpose when deploying or setting up a job.

Examples:

`Boiling Simulations <https://github.com/akashdhruv/boiling-simulations>`_

`Paramesh Performance <https://github.com/akashdhruv/paramesh-bittree-tests>`_

Install in development mode
---------------------------

::

   pip3 install click && cd jobrunner && ./setup develop
