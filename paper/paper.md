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
organize complex workloads, and enforce a directory based hierarchy to 
enable reuse of files and bash scripts within a project. Organization 
details of a directory tree are encoded in Jobfiles which serve as an 
index of files/scripts, and indicate their purpose when deploying or 
setting up a job. It is a flexible tool that allows users to design their 
own directory structure, perserve their design, and maintain consistency 
with increase in complexity of the project.


# Statement of need

Scientific processes continue to rely on software as an important tool 
for data acquisition, analysis, and discovery. This has allowed inclusion 
of sustainable software development practices as an integral component of 
research, enabling physics-based simulation instruments like Flash-X 
[@DUBEY2022] to model problems ranging from pool boiling to stellar explosions. 
However, design and management of software-based scientific studies is often left to 
individual researchers who design their computational experiments based on 
personal preferences and nature of the study. 

Although applications are available to create reproducible capsules for data 
generation [@code-ocean], they do not provide tools to manage research in a 
structured way which can enhance knowledge related to decisions made by 
researchers to configure their software instruments. 
A well organized lab notebook and execution environment enables systematic curation 
of the research process and provides implicit documentation for software configuration 
and options used to perform specific studies. This in turn enhances reproducibility 
by providing a roadmap towards data generation and contributing towards knowledge and 
understanding  of an experiment.

Jobrunner is a lightweight tool that addresses this need by enabling management of
software environments for computational experiments that rely on unix style interface
for development and execution. Design and operation of the tool allows researchers
to efficiently organize their workflows without compromising their design perferences
and requirements. We have applied this tool to manage performance and 
computational fluid dynamics studies using Flash-X [@DHRUV2023; @multiphase-simulations].

# Acknowledgements

We acknowledge contributions from Laboratory Directed Research and Development
(LDRD) program supported by Argonne National Laboratory [@argonne].

# References
