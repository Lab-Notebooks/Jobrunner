Jobrunner
=========

Jobrunner is a command line tool to manage and deploy computing jobs, organize complex workloads, and enforce a directory based hierarchy to enable reuse of files and bash scripts within a project. Organization details of a directory tree is encoded in hierachial Jobfiles which serve as an index of files/scripts on a given node and their purpose when deploying or setting up a job.

Functionality of Jobrunner is best understood through example projects which can be found in following repositories:

- `akashdhruv/boiling-simulations <https://github.com/akashdhruv/boiling-simulations>`_: A collection of high-fidelity flow/pool boiling simulations

- `akashdhruv/paramesh-bittree-tests <https://github.com/akashdhruv/paramesh-bittree-tests>`_: A lab notebook for performance tests of multiphysics scientific software instrument, Flash-X

- `akashdhruv/channel-flow <https://github.com/akashdhruv/channel-flow>`_: Example simulations of the channel flow problem to showcase applicability of containerization tools for scientific computing problems

Jobrunner commands
------------------

Writing a Jobfile
-----------------

Installation
------------

Using Python Package Index (PyPI)
::
   pip3 install PyJobrunner==1.5

Development mode
::
   pip3 install click && cd jobrunner && ./setup develop
