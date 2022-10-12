Jobrunner
=========

Jobrunner is a command line tool to manage and deploy computing jobs, organize complex workloads, and enforce a directory based hierarchy to enable reuse of files and bash scripts within a project. Organization details of a directory tree is encoded in hierachial Jobfiles which serve as an index of files/scripts on a given node and their purpose when deploying or setting up a job.

Functionality of Jobrunner is best understood through example projects which can be found in following repositories:

`akashdhruv/boiling-simulations <https://github.com/akashdhruv/boiling-simulations>`_

`akashdhruv/paramesh-bittree-tests <https://github.com/akashdhruv/paramesh-bittree-tests>`_

Install in development mode
---------------------------

::

   pip3 install click && cd jobrunner && ./setup develop
