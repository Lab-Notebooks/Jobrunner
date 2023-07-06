---
title: 'Jobrunner: A command line tool to manage execution environment for software based scientific studies'
tags:
  - Python
  - Lab notebooks
  - Scientfic computing
  - Reproducibility
  - Command line tools
authors:
  - name: Akash Dhruv
    orcid: 0000-0003-4997-321X
    affiliation: 1
affiliations:
  - name: Argonne National Laboratory, USA
    index: 1
date: 15 June 2023
bibliography: paper.bib
---

# Summary

Jobrunner is a command line tool to manage and deploy computational
experiments, organize workflows, and enforce a directory-based
hierarchy to enable reuse of files and bash scripts along a directory
tree. Organization details of the tree are encoded in Jobfiles,
which provide an index of files and scripts on each node and indicate
their relationship with Jobrunner commands. It is a flexible tool that
allows users to design their own directory structure and maintain
consistency with the increase in complexity of their workflows and
experiments.

# Statement of need

Use of software for data acquisition, analysis, and discovery in
scientific studies has allowed integration of sustainable software
development practices into the research process, enabling physics-based
simulation instruments like Flash-X [@DUBEY2022] to model problems
ranging from pool boiling to stellar explosions. However, the design
and management of software-based scientific studies is often left to
individual researchers who design their computational experiments
based on personal preferences and the nature of the study.

Although applications are available to create reproducible capsules
for data generation [@code-ocean], they do not provide tools to
manage research in a structured way which can enhance knowledge
related to decisions made by researchers to configure their software
instruments. A well-organized lab notebook and execution environment
enables systematic curation of the research process and provides
implicit documentation for software configuration and options used
to perform specific studies. This in turn enhances reproducibility by
providing a roadmap towards data generation and contributing towards
knowledge and understanding of an experiment.

Jobrunner addresses this need by enabling the management of software
environments for computational experiments that rely on a Unix-style
interface for development and execution. The design and operation of the
tool allow researchers to efficiently organize their workflows
without compromising their design preferences and requirements. We
have applied this tool to manage performance and computational fluid
dynamics studies using Flash-X [@DHRUV2023; @multiphase-simulations].

# Example

Application of Jobrunner can be understood better with an example
design of a computational experiment. Consider an experiment named
`Project` representative of a publicly available dataset 
[@outflow-forcing] for the work presented in [@DHRUV2023]. The 
directory tree as the following structure,

```console
$ tree Project

├── Jobfile
├── environment.sh
├── sites/
├── software/
├── simulation/
```

Each node in the tree is organized to capture information related to 
different aspects of the experiments. The node `sites/` for example 
stores platform specific information related to compilers and modules
required to build the software stack described in the  node `software/`.
Information provided in these nodes capture the execution environment
of the computational experiment.

Following is the design of the `sites/` node for the example above,

```console
$ tree Project/sites
├── sites/
    ├── sedona/
        ├── modules.sh
```

The site-specific subnode `sites/sedona/` consists of commands to
load platform specific compilers and libraries required to build
Flash-X [@DUBEY2022] which is the instrument used to perform the
experiments.

```bash
# file: Project/sites/sedona/modules.sh
#
# Load Message Passing Interface (MPI) and 
# Hierarchical Data Format (HDF5) libraries
module load openmpi hdf5
```

There are situations where requirements for Flash-X are not
available as modules and may have to be built from their
respective source. This is usually the case when a specific version
of the library or compiler is desired. The `software/` node provides
configuration details for these,

```console
$ tree Project/software

├── software/
    ├── Jobfile
    ├── setupFlashX.sh
    ├── setupAMReX.sh
```

Here the script `setupAMReX.sh` provides commands to get the source
code for AMReX[@AMReX_JOSS] and build it for desired version and
configuration. The script `setupFlashX.sh` sets the version for
Flash-X to perform the experiments. The `Jobfile` assigns the use of
these files by assigning them to specific Jobrunner commands,

```YAML
# file: Project/software/Jobfile
#
# Run these scripts during jobrunner setup command
job:
  setup:
    - setupAMReX.sh
    - setupFlashX.sh
```

The `environment.sh` file at the root of the `Project` directory
sources the site-specific `modules.sh` and sets environment
variables for compilation and execution.

```bash
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
```

The `Jobfile` at this node assigns the use of `environment.sh`,

```YAML
# file: Project/Jobfile

# Scripts to include during jobrunner setup and submit commands
job:
  setup:
    - environment.sh
  submit:
    - environment.sh
```

During the invocation of `jobrunner setup software/` command,
`environment.sh`, `setupAMReX.sh` and `setupFlashX.sh` are combined
using the information in Jobfiles and executed in sequence to build
the software stack.

The computational experiments are described in the node `simulation/`
and organized under different studies, `FlowBoiling`,
`EvaporatingBubble` and `PoolBoiling` as shown below,

```console
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
```

The `Jobfile` under subnode `simulation/PoolBoiling` provides details
for the files and scripts at this level

```YAML
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
```

During the invocation of `jobrunner setup simulation/PoolBoiling` command,
`environment.sh` and `flashSetup.sh` are combined using the information
in Jobfiles and executed in sequence to build the target executable
`flashx`. The software stack built in the previous step is available
through the environment variables in `environment.sh`.

The subnode `simulation/PoolBoiling` contains two different
configurations `earth_gravity` and `low_gravity` to represent a parametric
study of the boiling phenomenon under different gravity conditions. Each
configuration contains its respective `Jobfile`,

```YAML
# file: Project/simulation/PoolBoiling/earth_gravity/Jobfile
#
job:
  # input for the target
  input:
    - earth_gravity.par
```

Scientific instruments like Flash-X require input during execution which
is supplied in the form of parfiles with a `.par` extension. The parfiles
along a directory tree are  combined to create a single input file when
submitting the job. For example, invocation of
`jobrunner submit simulation/PoolBoiling/earth_gravity` combines
`pool_boiling.par` and `earth_gravity.par` that is used
to run the target executable `flashx` using the combination of
`environment.sh` and `flashRun.sh`.

Computational jobs are typically submitted using schedulars like `slurm`
to efficiently manage and allocate computational resources on large
supercomputing systems. The details of the schedular with desired
options is supplied by extending the `Jobfile` at root of the `Project`
directory,

```YAML
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
```

Jobrunner also provides features to keep the directory structure clean.
Results and artifacts from computational runs can be designated for
archiving or cleaning by extending the `Jobfile` for each study,

```YAML
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
```

# Acknowledgements

This material is based upon work supported by Laboratory Directed Research
and Development (LDRD) funding from Argonne National Laboratory, provided by
the Director, Office of Science, of the U.S. Department of Energy under Contract
No. DE-AC02-06CH11357.

# References
