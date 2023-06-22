.. |icon| image:: ./media/icon.svg
   :width: 50

##################
 |icon| Jobrunner
##################

|Code style: black|

Jobrunner is a command line tool to manage and deploy computing jobs,
organize complex workloads, and enforce a directory based hierarchy to
enable reuse of files and bash scripts within a project. Organization
details of a directory tree are encoded in Jobfiles which serve as an
index of files/scripts, and indicate their purpose when deploying or
setting up a job. It is a flexible tool that allows users to design
their own directory structure, perserve their design, and maintain
consistency with increase in complexity of the project.

**************
 Installation
**************

Stable releases of Jobrunner are hosted on Python Package Index website
(https://pypi.org/project/PyJobRunner/) and can be installed by
executing,

.. code::

   pip install PyJobrunner

Note that ``pip`` should point to ``python3+`` installation package
``pip3``.

Upgrading and uninstallation is easily managed through this interface
using,

.. code::

   pip install --upgrade PyJobrunner
   pip uninstall PyJobRunner

There maybe situations where users may want to install Jobrunner in
development mode $\\textemdash$ to design new features, debug, or
customize options/commands to their needs. This can be easily
accomplished using the ``setup`` script located in the project root
directory and executing,

.. code::

   ./setup develop

Development mode enables testing of features/updates directly from the
source code and is an effective method for debugging. Note that the
``setup`` script relies on ``click``, which can be installed using,

.. code::

   pip install click

The ``jobrunner`` script is installed in ``$HOME/.local/bin`` directory
and therfore the environment variable, ``PATH``, should be updated to
include this location for command line use.

**************
 Dependencies
**************

``python3.8+`` ``click`` ``toml`` ``pyyaml``

*******************
 Writing a Jobfile
*******************

A Jobfile provides details on functionality of each file in a directory
tree along with schedular configuration. Consider the following
directory tree for a project,

.. code::

   $ tree Project

   ├── Jobfile
   ├── environment.sh
   ├── JobObject1
   ├── JobObject2
       ├── Jobfile
       ├── application.input
       ├── application.exe
       ├── setupScript.sh
       ├── submitScript.sh
       ├── preProcess.sh
       ├── Config1
       ├── Config2
           ├── Jobfile
           ├── application.input

The base directory ``Project`` contains two different job object
subdirectories ``/Project/JobObject1`` and ``/Project/JobObject2`` which
share a common environment defined in ``environment.sh``,

.. code:: bash

   # module for OpenMPI
   module load openmpi

   # environment variables common to different job objects
   export COMMON_ENV_VARIABLE_1=/path/to/a/library
   export COMMON_ENV_VARIABLE_2="value"

It makes sense to places this file at the level of project home
directory and define it in ``Jobfile`` as given below, indicating that
``environment.sh`` should be included when executing both ``jobrunner
setup`` and ``jobrunner submit`` commands. Details regarding the job
schedular are also defined at this level. The schedular command
$\\textemdash$ ``slurm`` in this case $\\textemdash$ is used to dispatch
the jobs with desired options.

.. code:: YAML

   # scripts to include during jobrunner setup and submit commands
   job:
     setup:
       - environment.sh
     submit:
       - environment.sh

   # schedular command and options to dispatch jobs
   schedular:
     command: slurm
     options:
       - "#SBATCH -t 0-30:00"
       - "#SBATCH --job-name=myjob"
       - "#SBATCH --ntasks=5"

At the level of subdirectory ``/Project/JobObject2`` more files are
added and lead to a Jobfile that looks like,

.. code:: yaml

   job:

     # list of scripts and input files that need to execute during setup command
     setup:
       - setupScript.sh

     # input for the job
     input:
       - application.input

     # target file/executable for the job
     target: application.exe

     # list of scripts that need to execute when running submit command
     submit:
       - preProcess.sh
       - submitScript.sh

The field, ``job:input``, refers to the inputs required to run
``job:target`` executable common for configurations
``/Project/JobObject2/Config1`` and ``/Project/JobObject2/Config2``.
Each configuration contains additional input files with values that are
appended to the ones provided at the current level. The Jobfile at
``/Project/JobObject2/Config2`` becomes,

.. code:: YAML

   job:

     # append to input file
     input:
       - application.input

     # list of file/patterns to archive
     archive:
       - "*_hdf5_*"
       - "*.log"

The field, ``job.archive``, provides a list of file/patterns that are
moved over to the
``/Project/JobObject2/Config2/jobnode.archive/<tagID>`` directory when
running ``jobrunner archive --tag=<tagID>``. This feature is provided to
store results before cleaning up working directory for fresh runs

********************
 Jobrunner commands
********************

Setup
=====

``jobrunner setup <JobWorkDir>`` creates a ``job.setup`` file in
``<workdir>`` using ``job.setup`` scripts defined in Jobfiles along the
directory tree. Jobrunner executes each script serially by changing the
working directory to the location of the script. A special environment
variable ``JobWorkDir`` provides the value of ``<JobWorkDir>`` supplied
during invocation of the command.

The ``--show`` option can be used to check which bash scripts will be
included during invocation. Following is the result of ``jobrunner setup
--show JobObject2`` for the example above,

.. code::

   Working directory: /Project/JobObject2
   Parsing Jobfiles in directory tree

   job.setup: [
           /Project/environment.sh
           /Project/JobObject2/setupScript.sh
           ]

Submit
======

``jobrunner submit <JobWorkDir>`` creates a ``job.submit`` file in
``<JobWorkDir>`` using ``job.submit`` scripts and ``schedular.options``
values defined in Jobfiles along the directory tree.
``schedular.command`` is used to dispatch the result script.

The ``--show`` option can be used to check schedular configuration and
list of bash scripts that will be included during invocation. Following
is the result of ``jobrunner submit --show JobObject2/Config2`` for the
example above,

.. code::

   Working directory: /Project/JobObject2/Config2
   Parsing Jobfiles in directory tree

   schedular.command:
           slurm
   schedular.options: [
           #SBATCH -t 0-30:00
           #SBATCH --job-name=myjob
           #SBATCH --ntasks=5
           ]
   job.input: [
           /Project/JobObject2/flash.par
           /Project/JobObject2/Config2/flash.par
           ]
   job.target:
           /Project/JobObject2/flashx
   job.submit: [
           /Project/environment.sh
           /Project/JobObject2/preProcess.sh
           /Project/JobObject2/submitScript.sh
           ]

Along with the ``job.submit`` script, ``job.input`` and ``job.target``
files are also created in ``<JobWorkDir>`` and created using values
defined in Jobfiles.

Archive
=======

``jobrunner archive --tag=<tagID> <JobWorkDir>`` creates archives along
the directory tree using the list of values defined ``job.archive``. The
archives are created under the sub-directory ``jobnode.archive/<tagID>``
and represent the state of the directory tree during the invocation.

Export
======

``jobrunner export --tag=<pathToArchive> <JobWorkDir>`` exports
directory tree and archives objects to an external directory
``<pathToArchive>`` to preserve state and curate execution environment.

Clean
=====

``jobrunner clean <JobWorkDir>`` removes Jobrunner artifacts from the
working directory

**********
 Examples
**********

Functionality of Jobrunner is best understood through example projects
which can be found in following repositories:

-  `akashdhruv/Multiphase-Simulations
   <https://github.com/akashdhruv/Multiphase-Simulations>`_: A
   collection of high-fidelity flow/pool boiling simulations

**********
 Citation
**********

.. code::

   @software{akash_dhruv_2022_7255620,
      author       = {Akash Dhruv},
      title        = {akashdhruv/Jobrunner: October 2022},
      month        = oct,
      year         = 2022,
      publisher    = {Zenodo},
      version      = {22.10},
      doi          = {10.5281/zenodo.7255620},
      url          = {https://doi.org/10.5281/zenodo.7255620}
   }

.. |Code style: black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
