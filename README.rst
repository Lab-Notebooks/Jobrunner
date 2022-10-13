Jobrunner
=========

|Code style: black|

Jobrunner is a command line tool to manage and deploy computing jobs, organize complex workloads, and enforce a directory based hierarchy to enable reuse of files and bash scripts within a project. Organization details of a directory tree is encoded in Jobfiles which serve as an index of files/scripts, and indicate their purpose when deploying or setting up a job.

Functionality of Jobrunner is best understood through example projects which can be found in following repositories:

- `akashdhruv/boiling-simulations <https://github.com/akashdhruv/boiling-simulations>`_: A collection of high-fidelity flow/pool boiling simulations

- `akashdhruv/paramesh-bittree-tests <https://github.com/akashdhruv/paramesh-bittree-tests>`_: A lab notebook for performance tests of multiphysics scientific software instrument, Flash-X

- `akashdhruv/channel-flow <https://github.com/akashdhruv/channel-flow>`_: Example simulations of the channel flow problem to showcase applicability of containerization tools for scientific computing problems

Writing a Jobfile
-----------------

A Jobfile provides details on functionality of each file in a directory tree along with schedular configuration

::

   [schedular]
      command = "bash"
      options = []
      
   [job]
      setup = []
      input = []
      target = "target"
      submit = []
      archive = []

Jobrunner commands
------------------

- **Setup**: Executes

- **Submit**: Executes

- **Archive**: Executes

- **Clean**: Executes

Installation
------------

Using Python Package Index (PyPI)
::

   pip3 install PyJobrunner

Development mode
::

   pip3 install click && ./setup develop
   
.. |Code style: black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
