.. _installation:

Prerequisites
-------------

AnnoTater uses a variety of bioinformatics software packages, which will be downloaded to your machine automatically. **The AnnoTater workflow is downloaded automatically to your machine when you run it via Nextflow for the first time**. To do this, there are two dependencies you will need: Nextflow and your choice of container executor (Singularity or Docker).

Required Dependencies
*********************

At a minimum, AnnoTater requires the following:

- `Nextflow <https://www.nextflow.io/>`__ : Executes the workflow.  Nextflow also requires an installation of Java.
- `Singularity <https://sylabs.io/>`__ or `Docker <https://www.docker.com/>`__. **(Singularity Recommended)**

Container Support
*****************

All of the software tools needed to run AnnoTater have been pre-installed into a Docker container. Therefore, you do not need to install them!  Using the container can ensure that results from AnnoTater are always reproducible because the environment in which the software is executed will not change even if the host computational computer is updated.  Please ensure one of these containerization services are installed.

  - `Singularity Community Edition (CE) <https://sylabs.io/>`__  **(recommended)**.
  - `Docker <https://www.docker.com/>`__.


Choice of Computing Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Local Machine
*************

AnnoTater can be run on a local computer; in particular, it has been tested on `Ubuntu <https://www.ubuntu.com/>`__.  AnnoTater has been optimized to allow for execution of large sample sizes without consuming large amounts of storage space.  However, the time required to execute is dependent on the amount of computing power the machine has. You should consider using a High-Performance Computing (HPC) system if you have a large number of samples and would like AnnoTater to execute faster.

High-Performance Computing (HPC) Setup
**************************************

On an HPC system it is recommended to use containerized dependencies as most HPC users do not have access to install software and HPC systems can change yielding results that may be hard to reproduce after time has passed and system setups have changed.  Additionally, most HPC setups do not allow users to run Docker, but rather support Singularity instead. Using singularity is recommended on an HPC system rather than installing software dependencies manually. You will need to make sure that Nextflow and Singularity are installed on your cluster (you may need the help of your HPC administrator).
