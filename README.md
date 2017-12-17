![OpenWorm](http://www.openworm.org/img/OpenWormLogo.png)

[![Stories in Ready](https://badge.waffle.io/openworm/openworm.png?label=ready&title=Ready)](https://waffle.io/openworm/openworm)

About **OpenWorm**
------------------

[OpenWorm](http://openworm.org) aims to build the first comprehensive computational model of *Caenorhabditis elegans* (*C. elegans*), a microscopic roundworm. With only a thousand cells, it solves basic problems such as feeding, mate-finding and predator avoidance. Despite being extremely well-studied in biology, a deep, principled understanding of the biology of this organism remains elusive.

We are using a bottom-up approach, aimed at observing the worm behaviour emerge from a simulation of data derived from scientific experiments carried out over the past decade. To do so we are incorporating the data available from the scientific community into software models. We are also forging new collaborations with universities and research institutes to collect data that fill in the gaps.

Quickstart
----------
We have put together a [docker container](http://docker.com) that pulls together the major components of our simulation and runs it on your machine.  When you get it all running it do the following:

1. Run our nervous system model, known as c302, on your computer.  
2. Run our body model, known as sibernetic, on your computer, using the output of the nervous system model.
3. Produce graphs from the output of the nervous system model that demonstrate its output on your computer for you to inspect.
4. Produce a movie showing the output of the body model for you to inspect.

**Example Output**

![Worm Crawling](img/worm-crawling.gif)

<img src="img/muscle-activity.png" width="300">
<img src="img/neuron-activity.png" width="400">

**Installation**

Pre-requisites:

1. Currently Windows is not supported; you will need Mac OS or Linux (or a virtual environment on Windows that runs either of those).
2. You should have at least 60 GB of free space on your machine and at least 2GB of RAM

To Install:

1. Install [Docker](http://docker.com) on your system.  

To Run: 

1. Open a terminal and run 'run.sh'
2. About 5-10 minutes of output will display on the screen as the steps run
3. The simulation will end.  Run 'stop.sh' on your system to clean up the running container.
4. Inspect the output in the `output` directory.

Documentation
-------------
Find out more about OpenWorm.  Documentation is available at [http://docs.openworm.org](http://docs.openworm.org)

This repository stores:
* A project-wide [Kanban board of all issues](https://waffle.io/openworm/openworm)
* Project-wide tracking via high-level [issues](https://github.com/openworm/OpenWorm/issues?labels=&milestone=&page=1&state=open) and [milestones](https://github.com/openworm/OpenWorm/milestones)


