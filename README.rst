.. |icon| image:: ./media/icon.svg
   :width: 50

##################
 |icon| Jobrunner
##################

|Code style: black|

Jobrunner is a command line tool to manage and deploy computational
experiments, organize workflows, and enforce a directory-based hierarchy
to enable reuse of files and bash scripts along a directory tree.
Organization details of the tree are encoded in Jobfiles, which provide
an index of files and scripts on each node and indicate their
relationship with Jobrunner commands. It is a flexible tool that allows
users to design their own directory structure and maintain consistency
with the increase in complexity of their workflows and experiments.

Read our paper here: https://arxiv.org/pdf/2308.15637.pdf

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

The following installation option can be used to allow for using
customization specific to instruments.

.. code::

   pip install PyJobruner --user --install-option="--with-instruments"

This allow for the use of the ``instrument`` field in the Jobfile

There maybe situations where users may want to install Jobrunner in
development mode $\\textemdash$ to design new features, debug, or
customize options/commands to their needs. This can be easily
accomplished using the ``setup`` script located in the project root
directory and executing,

.. code::

   ./setup develop --with-instruments

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

``python3.8+`` ``click`` ``toml`` ``pyyaml`` ``alive-progress``

*******************
 Statement of Need
*******************

Use of software for data acquisition, analysis, and discovery in
scientific studies has allowed integration of sustainable software
development practices into the research process, enabling physics-based
simulation instruments like Flash-X (https://flash-x.org) to model
problems ranging from pool boiling to stellar explosions. However, the
design and management of software-based scientific studies is often left
to individual researchers who design their computational experiments
based on personal preferences and the nature of the study.

Although applications are available to create reproducible capsules for
data generation (https://codeocean.com), they do not provide tools to
manage research in a structured way which can enhance knowledge related
to decisions made by researchers to configure their software
instruments. A well-organized lab notebook and execution environment
enables systematic curation of the research process and provides
implicit documentation for software configuration and options used to
perform specific studies. This in turn enhances reproducibility by
providing a roadmap towards data generation and contributing towards
knowledge and understanding of an experiment.

Jobrunner addresses this need by enabling the management of software
environments for computational experiments that rely on a Unix-style
interface for development and execution. The design and operation of the
tool allow researchers to efficiently organize their workflows without
compromising their design preferences and requirements. We have applied
this tool to manage performance and computational fluid dynamics studies
using Flash-X.

*********
 Example
*********

Application of Jobrunner can be understood better with an example design
of a computational experiment. Consider an experiment named `Project`
representative of a publicly available dataset
(https://github.com/Lab-Notebooks/Outflow-Forcing-BubbleML) for the work
presented in (https://arxiv.org/pdf/2306.10174.pdf). The directory tree
has the following structure,

.. code:: console

   $ tree Project

   ├── Jobfile
   ├── environment.sh
   ├── sites/
   ├── software/
   ├── simulation/

Each node in the tree is organized to capture information related to
different aspects of the experiments. The node ``sites/`` for example
stores platform specific information related to compilers and modules
required to build the software stack described in the node
``software/``. Information provided in these nodes capture the execution
environment of the computational experiment.

Following is the design of the ``sites/`` node for the example above,

.. code:: console

   $ tree Project/sites
   ├── sites/
       ├── sedona/
           ├── modules.sh

The site-specific subnode ``sites/sedona/`` consists of commands to load
platform specific compilers and libraries required to build Flash-X
which is the instrument used to perform the experiments.

.. code:: bash

   # file: Project/sites/sedona/modules.sh
   #
   # Load Message Passing Interface (MPI) and
   # Hierarchical Data Format (HDF5) libraries
   module load openmpi
   module load hdf5

There are situations where requirements for Flash-X are not available as
modules and may have to be built from their respective source. This is
usually the case when a specific version of the library or compiler is
desired. The ``software/`` node provides configuration details for
these,

.. code:: console

   $ tree Project/software

   ├── software/
       ├── Jobfile
       ├── setupFlashX.sh
       ├── setupAMReX.sh

Here the script ``setupAMReX.sh`` provides commands to get the source
code for AMReX(https://github.com/AMReX-Codes/amrex) and build it for
desired version and configuration. The script ``setupFlashX.sh`` sets
the version for Flash-X to perform the experiments. The ``Jobfile``
indicates the use of these files by assigning them to specific Jobrunner
commands,

.. code:: yaml

   # file: Project/software/Jobfile
   #
   # Run these scripts during jobrunner setup command
   job:
     setup:
       - setupAMReX.sh
       - setupFlashX.sh

The ``environment.sh`` file at the root of the ``Project`` directory
sources the site-specific ``modules.sh`` and sets environment variables
for compilation and execution.

.. code:: bash

   # file: Project/environment.sh
   #
   # Set project home using realpath of current directory
   export PROJECT_HOME=$(realpath .)

   # Enter site information and source the modules
   SiteName="sedona"
   SiteHome="$PROJECT_HOME/sites/$SiteName"
   source $SiteHome/modules.sh

   # Set environment variables required for Makefile.h
   export MPI_HOME=$(which mpicc | sed s/'\/bin\/mpicc'//)
   export HDF5_HOME=$(which h5pfc | sed s/'\/bin\/h5pfc'//)

   # Assign path for local AMReX installation
   export AMREX2D_HOME="$PROJECT_HOME/software/AMReX/install-$SiteName/2D"
   export AMREX3D_HOME="$PROJECT_HOME/software/AMReX/install-$SiteName/3D"

   # Path to Flash-X
   export FLASHX_HOME="$PROJECT_HOME/software/Flash-X"

The ``Jobfile`` at this node assigns the use of ``environment.sh``,

.. code:: yaml

   # file: Project/Jobfile

   instrument: Flash-X

   # Scripts to include during jobrunner setup and submit commands
   job:
     setup:
       - environment.sh
     submit:
       - environment.sh

During the invocation of ``jobrunner setup software/`` command,
``environment.sh``, ``setupAMReX.sh`` and ``setupFlashX.sh`` are
combined using the information in Jobfiles and executed in sequence to
build the software stack.

The computational experiments are described in the node ``simulation/``
and organized under different studies, ``FlowBoiling``,
``EvaporatingBubble`` and ``PoolBoiling`` as shown below,

.. code:: console

   $ tree Project/simulation

   ├── simulation/
       ├── FlowBoiling/
       ├── EvaporatingBubble/
       ├── PoolBoiling/
           ├── Jobfile
           ├── flashSetup.sh
           ├── flashRun.sh
           ├── pool_boiling.par
           ├── earth-gravity/
               ├── Jobfile
               ├── earth_gravity.par
           ├── low-gravity/
               ├── Jobfile
               ├── low_gravity.par

The ``Jobfile`` under subnode ``simulation/PoolBoiling`` provides
details for the files and scripts at this level

.. code:: yaml

   # file: Project/simulation/PoolBoiling/Jobfile
   #
   job:
     # list of scripts that need to execute during setup
     setup:
       - flashSetup.sh

     # target executable created during setup
     target: flashx

     # input for the target
     input:
       - pool_boiling.par

     # list of scripts that need to execute during submit
     submit:
       - flashRun.sh

During the invocation of ``jobrunner setup simulation/PoolBoiling``
command, ``environment.sh`` and ``flashSetup.sh`` are combined using the
information in Jobfiles and executed in sequence to build the target
executable ``flashx``. The software stack built in the previous step is
available through the environment variables in ``environment.sh``.

The subnode ``simulation/PoolBoiling`` contains two different
configurations ``earth_gravity`` and ``low_gravity`` to represent a
parametric study of the boiling phenomenon under different gravity
conditions. Each configuration contains its respective ``Jobfile``,

.. code:: yaml

   # file: Project/simulation/PoolBoiling/earth_gravity/Jobfile
   #
   job:
     # input for the target
     input:
       - earth_gravity.par

Scientific instruments like Flash-X require input during execution which
is supplied in the form of parfiles with a ``.par`` extension. The
parfiles along a directory tree are combined to create a single input
file when submitting the job. For example, invocation of ``jobrunner
submit simulation/PoolBoiling/earth_gravity`` combines
``pool_boiling.par`` and ``earth_gravity.par`` that is used to run the
target executable ``flashx`` using the combination of ``environment.sh``
and ``flashRun.sh``.

Computational jobs are typically submitted using schedulars like
``slurm`` to efficiently manage and allocate computational resources on
large supercomputing systems. The details of the schedular with desired
options is supplied by extending the ``Jobfile`` at root of the
``Project`` directory,

.. code:: yaml

   # file: Project/Jobfile
   #
   # Scripts to include during jobrunner setup and submit commands
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

Jobrunner also provides features to keep the directory structure clean.
Results and artifacts from computational runs can be designated for
archiving or cleaning by extending the ``Jobfile`` for each study,

.. code:: yaml

   # file: Project/simulation/PoolBoiling/earth_gravity/Jobfile
   #
   job:
     # input for the target
     input:
       - earth_gravity.par

     # clean slurm output and error files
     clean:
       - "*.out"
       - "*.err"

     # archive flashx log and output files
     archive:
       - "*_hdf5_*"
       - "*.log"

********************
 Jobrunner commands
********************

Setup
=====

``jobrunner setup <JobWorkDir>`` creates a ``job.setup`` file using
``job.setup`` scripts defined in Jobfiles along the directory tree.
Jobrunner executes each script serially by changing the working
directory to the location of the script. A special environment variable
``JobWorkDir`` provides the value of ``<JobWorkDir>`` supplied during
invocation of the command.

.. code:: console

   Working directory: /Project/simulation/PoolBoiling
   Parsing Jobfiles in directory tree

   job.setup: [
           /Project/environment.sh
           /Project/simulation/PoolBoiling/flashSetup.sh
           ]

Submit
======

``jobrunner submit <JobWorkDir>`` creates a ``job.submit`` file using
``job.submit`` scripts and ``schedular.options`` values defined in
Jobfiles along the directory tree. ``schedular.command`` is used to
dispatch the resulting script.

.. code:: console

   Working directory: /Project/simulation/PoolBoiling/earth_gravity
   Parsing Jobfiles in directory tree

   schedular.command:
           slurm
   schedular.options: [
           #SBATCH -t 0-30:00
           #SBATCH --job-name=myjob
           #SBATCH --ntasks=5
           ]
   job.input: [
           /Project/simulation/PoolBoiling/pool_boiling.par
           /Project/simulation/PoolBoiling/earth_gravity/earth_gravity.par
           ]
   job.target:
           /Project/simulation/PoolBoiling/flashx
   job.submit: [
           /Project/environment.sh
           /Project/simulation/PoolBoiling/flashRun.sh
           ]

Along with the ``job.submit`` script, ``job.input`` and ``job.target``
files are also created in ``<JobWorkDir>`` using values defined in
Jobfiles.

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
   <https://github.com/akashdhruv/Multiphase-Simulations>`_: A lab
   notebook to manage development of Flash-X

-  `Lab-Notebooks/Outflow-Forcing-BubbleML
   <https://github.com/Lab-Notebooks/Outflow-Forcing-BubbleML>`_:
   Reproducibility capsule for research papers
   (https://arxiv.org/pdf/2306.10174.pdf)
   (https://arxiv.org/pdf/2307.14623.pdf)

-  `Lab-Notebooks/Flow-Boiling-3DL
   <https://github.com/Lab-Notebooks/Flow-Boiling-3D>`_: Execution
   environment for running three-dimensional flow boiling simulations on
   high performance computing systems.

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

******************
 Acknowledgements
******************

This material is based upon work supported by Laboratory Directed
Research and Development (LDRD) funding from Argonne National
Laboratory, provided by the Director, Office of Science, of the U.S.
Department of Energy under Contract No. DE-AC02-06CH11357.

.. |Code style: black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
