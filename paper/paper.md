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
affiliations:
 - name: Argonne National Laboratory, USA
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
research, enabling physics-based simulation instruments like Flash-X to 
model problems ranging from pool boiling to stellar explosions. However, 
design and management of software-based scientific studies is often left to 
individual researchers who design their computational experiments based on 
personal preferences and nature of the study. Although applications are available 
to create reproducible capsules for data generation, they do not provide tools to 
manage research in a structured way which can enhance knowledge related to decisions 
made by researchers to configure their software instruments. A well organized lab 
notebook and execution environment enables systematic curation of the research 
process and provides implicit documentation for software configuration and options 
used to perform specific studies. This in turn enhances reproducibility by providing 
a roadmap towards data generation and contributing towards knowledge and understanding 
of an experiment. In this article we will provide an overview of tools and practices 
that we have developed to manage computational fluid dynamics studies using Flash-X, 
and demonstrate how research process can be efficiently organized without having 
to compromise researcher preferences and requirements. The lightweight tools 
that we provide can be applied to computational experiments that rely on unix style 
interface for development and execution.

# Acknowledgements

We acknowledge contributions from Laboratory Directed Research and Development
(LDRD) program supported by Argonne National Laboratory [@argonne].

# References
