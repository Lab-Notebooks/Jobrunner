.. |icon| image:: ./icon.svg
  :width: 50

|icon| Jobrunner
================

|Code style: black|

Jobrunner is a command line tool to manage and deploy computing jobs, organize complex workloads, and enforce a directory based hierarchy to enable reuse of files and bash scripts within a project. Organization details of a directory tree are encoded in Jobfiles which serve as an index of files/scripts, and indicate their purpose when deploying or setting up a job. It is a flexible tool that allows users to design their own directory structure, and simply perserves their design and maintains consistency with increase in complexity of the project.

Installation
------------

Stable releases of Jobrunner are hosted on Python Package Index website (`<https://pypi.org/project/PyJobRunner/>`_) and can be installed by executing,

::

   pip install PyJobrunner
   
Note that ``pip`` should point to ``python3+`` installation package ``pip3``. 

Upgrading and uninstallation is easily managed through this interface using,

::

   pip install --upgrade PyJobrunner
   pip uninstall PyJobRunner

There maybe situations where users may want to install Jobrunner in development mode $\\textemdash$ to design new features, debug, or customize options/commands to their needs. This can be easily accomplished using the ``setup`` script located in the project root directory and executing,

::

   ./setup develop

Development mode enables testing of features/updates directly from the source code and is an effective method for debugging. Note that the ``setup`` script relies on ``click``, which can be installed using,

::

  pip install click

Dependencies
------------

``python3.8+`` ``toml``

Writing a Jobfile
-----------------

A Jobfile provides details on functionality of each file in a directory tree along with schedular configuration. Consider the following directory tree for a project,

..  code-block:: none

    $ tree Project
    ├── Jobfile
    ├── environment.sh
    ├── JobObject1
    |── JobObject2
        ├── Jobfile
        ├── flash.par
        ├── flashx
        ├── setupScript.sh
        ├── submitScript.sh
        ├── preProcess.sh
        ├── config1
        ├── config2
            ├── Jobfile
            ├── flash.par

The base directory ``Project`` contains two different job object sub-directories ``JobObject1`` and ``JobObject2`` which share a common environment defined in ``environment.sh``,

.. code-block:: bash

   # module for OpenMPI
   module load openmpi-4.1.1

   # environment variables common to
   # different job objects
   export COMMON_ENV_VARIABLE_1=/path/to/a/libarary
   export COMMON_ENV_VARIABLE_2="value"

It makes sense to places this file at the level of project home directory and defined it ``Jobfile`` as,

..  code-block:: python

    # scripts to include during
    # jobrunner setup command
    job.setup = ["environment.sh"]

    # scripts to include during
    # jobrunner submit command
    job.submit = ["environment.sh"]
    
indicating that ``environment.sh`` should be included when executing both ``jobrunner setup`` and ``jobrunner submit`` commands. Descending down to the ``JobObject1`` level 

..  code-block:: python

   [schedular]
      
      # schedular command to dispatch jobs
      command = "slurm"
      
      # schedular options job name, time, nodes/tasks
      options = [
                  "#SBATCH --ntasks=5",
                  "#SBATCH -t 0-30:00",
                  "#SBATCH --job-name=myjob",
                ]
      
   [job]
   
      # list of scripts that need to execute when running setup command
      setup = ["setupScript.sh"]
      
      # input for the job
      input = ["flash.par"]
      
      # target file/executable for the job
      target = "flashx"
      
      # list of scripts that need to execute when running submit command
      submit = [
                  "preProcess.sh", 
                  "submitScript.sh",
               ]
               
      # list of file/patterns to archive
      archive = ["*_hdf5_*", "*.log"]

Jobrunner commands
------------------

- **Setup**: Executes

- **Submit**: Executes

- **Archive**: Executes

- **Clean**: Executes
   
Examples
--------

Functionality of Jobrunner is best understood through example projects which can be found in following repositories:

- `akashdhruv/boiling-simulations <https://github.com/akashdhruv/boiling-simulations>`_: A collection of high-fidelity flow/pool boiling simulations

- `akashdhruv/paramesh-bittree-tests <https://github.com/akashdhruv/paramesh-bittree-tests>`_: A lab notebook for performance tests of multiphysics scientific software instrument, Flash-X

- `akashdhruv/channel-flow <https://github.com/akashdhruv/channel-flow>`_: Example simulations of the channel flow problem to showcase applicability of containerization tools for scientific computing problems
.. |Code style: black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
