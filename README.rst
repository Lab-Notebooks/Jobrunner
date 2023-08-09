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
representative of a publicly available dataset [@outflow-forcing] for
the work presented in [@DHRUV2023]. The directory tree as the following
structure,

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
[@DUBEY2022] which is the instrument used to perform the experiments.

.. code:: bash

   # file: Project/sites/sedona/modules.sh
   #
   # Load Message Passing Interface (MPI) and
   # Hierarchical Data Format (HDF5) libraries
   module load openmpi hdf5

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

******************
 Acknowledgements
******************

This material is based upon work supported by Laboratory Directed
Research and Development (LDRD) funding from Argonne National
Laboratory, provided by the Director, Office of Science, of the U.S.
Department of Energy under Contract No. DE-AC02-06CH11357.

.. |Code style: black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
