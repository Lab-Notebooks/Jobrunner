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

Jobrunner is a command line tool to manage and deploy computing jobs,
organize complex workloads and enforce a directory based hierarchy to
enable reuse of files and bash scripts within a project. Organization
details of a directory tree are encoded in `Jobfiles` which serve as
an index of files/scripts, and indicate their purpose when deploying or
setting up a job. It is a flexible tool that allows users to design their
own directory structure, perserve their design and maintain consistency
with increase in complexity of the project.

# Statement of need

Scientific processes continue to rely on software as an important tool
for data acquisition, analysis, and discovery. This has allowed
inclusion of sustainable software development practices as an integral
component of research, enabling physics-based simulation instruments like
Flash-X [@DUBEY2022] to model problems ranging from pool boiling to stellar
explosions. However, design and management of software-based scientific
studies is often left to individual researchers who design their
computational experiments based on personal preferences and nature of the
study.

Although applications are available to create reproducible capsules for data
generation [@code-ocean], they do not provide tools to manage research in a
structured way which can enhance knowledge related to decisions made by
researchers to configure their software instruments. A well organized lab notebook
and execution environment enables systematic curation of the research process and
provides implicit documentation for software configuration and options used to
perform specific studies. This in turn enhances reproducibility by providing a
roadmap towards data generation and contributing towards knowledge and
understanding  of an experiment.

Jobrunner addresses this need by enabling management of software environments for
computational experiments that rely on unix style interface for development and
execution. Design and operation of the tool allows researchers to efficiently organize
their workflows without compromising their design perferences and requirements. We have
applied this tool to manage performance and computational fluid dynamics studies using
Flash-X [@DHRUV2023; @multiphase-simulations].

# Example

Application of Jobrunner can be understood better with an example design
of a computational experiment. Consider an experiment named `Project` with
two different studies tiled `Study1` and `Study2`. Lets assume that
`Study2` consists of a parameteric investigation using different
configurations, `Config1` and `Config2`. All of this can be organized
using the following directory tree,

```
$ tree Project

├── Jobfile
├── environment.sh
├── sites
    ├── sedona
        ├── Makefile.h.FlashX
        ├── modules.sh
├── software
    ├── Jobfile
    ├── setupFlashX.sh
    ├── setupAMReX.sh
    ├── setupFlashKit.sh
    ├── setupHDF5.sh
├── simulation
    ├── PoolBoiling
        ├── Jobfile
        ├── flashOptions.sh
        ├── flashBuild.sh
        ├── flashRun.sh
        ├── flash.toml
    ├── FlowBoiling
    ├── EvaporatingBubble   
├── analysis
```

```
# Load MPI module available on local machine 
module load openmpi-4.1.1
```

Lets say that both `Study1` and `Study2` are based on some
common environment options that can be defined in `environment.sh` [@outflow-forcing],

```bash
# Set project home using realpath of current directory
export PROJECT_HOME=$(realpath .)

# Set SiteHome to realpath of SiteName
SiteHome="$PROJECT_HOME/sites/$SiteName"

# Load modules from the site directory
source $SiteHome/modules.sh

# Set MPI_HOME by quering path loaded by site module
export MPI_HOME=$(which mpicc | sed s/'\/bin\/mpicc'//)

# Path to parallel HDF5 installtion with fortran support
export HDF5_HOME="$PROJECT_HOME/software/HDF5/install-$SiteName"

# Store path to amrex as environment variable
export AMREX2D_HOME="$PROJECT_HOME/software/AMReX/install-$SiteName/2D"
export AMREX3D_HOME="$PROJECT_HOME/software/AMReX/install-$SiteName/3D"

# Path to Flash-X
export FLASHX_HOME="$PROJECT_HOME/software/Flash-X"
```

It makes sense to places this file at the level of project home
directory and define it in `Jobfile` as described below,

```YAML

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
```

A Jobfile provides details on functionality of each file in a directory
tree along with schedular configuration to execute specific studies
with desired configuration. The Jobfile above indicates that
`environment.sh` should be included when setting up and executing
experiments using Jobrunner. Details regarding the job
schedular are also defined at this level. The schedular command,
`slurm` in this case, is used to dispatch
the jobs with desired options.

At the level of subdirectory `/Project/Study2` more files are
added and lead to a Jobfile that looks like,

```YAML

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
```

The field, `input`, refers to the inputs required to run
`target` executable common for configurations
`/Project/Study2/Config1` and `/Project/Study2/Config2`.
Each configuration contains additional input files with values that are
appended to the ones provided at the current level. The Jobfile at
`/Project/Study2/Config2` becomes,

```YAML

   job:

     # append to input file
     input:
       - application.input

     # list of file/patterns to archive
     archive:
       - "*_hdf5_*"
       - "*.log"
```

The field, `archive`, provides a list of file/patterns that should
be preserved as artifacts of an experiment. Jobrunner parses information provided
in these Jobfiles and stitches together computational experiments that can be
efficiently scaled and managed using a directory-based hierarchy.

# Acknowledgements

This material is based upon work supported by Laboratory Directed Research
and Development (LDRD) funding from Argonne National Laboratory, provided by
the Director, Office of Science, of the U.S. Department of Energy under Contract
No. DE-AC02-06CH11357.

# References
