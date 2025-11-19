# How to use this folder, and set up everything

## Installing the openfoam adapter

This should be hopefully straightforward, when you have preCICE already installed and it is discoverable at runtime.
Clone the repository:

<pre>
git clone https://github.com/thomaskroi1996/openfoam-adapter/tree/dp_dt
cd openfoam-adapter
./Allclean                                                      #run this first in case there are some leftovers I accidentally commited
./Allwmake                                                      #this will build the adapter
</pre>

## Building openCFS with preCICE enabled

The most up-do-date branch is thk_precice_opencfs

<pre>
git clone https://gitlab.com/openCFS/cfs/-/tree/thk_precice_opencfs?ref_type=heads
mkdir build && cd build
cmake .. -DUSE_PRECICE=ON                                       # or ccmake .. and set graphically
make -j
</pre>

If precice is not discoverable, you can manually set the path with -DPRECICE_DIR=..

## Running the simulation

Now you should be able to run the simulations by having two terminals open.

openFoam Terminal:

<pre>
cd openFoam
icoFoam
</pre>

openCFS Terminal:

<pre>
cd openCFS
cfs propagation
</pre>

or with propagation_dpdt.xml and cd openFoam_dpdt for pressure derivative. 

The simulation has to be run for the result files to be present, because of github's file size limit.

## Important files and notes on folders

The most important files are:

- openCFS/propagation.xml
- precice-config.xml
- openFoam/system/controlDict
- openFoam/system/preciceDict

cylinder_standard_way is a folder containing the cylinder example simulated in the standard way.

openFoam_dpdt is a folder that is already designed to run using the PressureTemporalDerivative class in the openfoam adapter.

graph.png is a visualisation of the precice configuration file used, made with the precice-config-visualizer (https://precice.org/tooling-config-visualization.html)


cylinder_standard_way/3_ca/results_hdf5/propagation.cfs is how the simulation should look like

## Known issues
- When using the cfs build with USE_PRECICE=ON, you have to use precice in the simulation xml, otherwise:

<pre>
***********************************************************************
 SIMULATION RUN FAILED!  -  CAUGHT EXCEPTION:


element 'fileFormats' has no child 'name'

In file '/home/thk/cfs_precice/source/DataInOut/ParamHandling/ParamNode.cc' at line 701


***********************************************************************
</pre>

- acouRhsLoad on internal exists twice in resultContexts, but one time the result functor is 0, eventually leading to a "cannot access element 0 of Vector with size 0" error when the output starts, and simulation fails. Why does it exist twice?


- Artefacts in the source region, perhaps some issue with reading in nodal values? 


oldTime() method in Adapter.C and writeCheckpoint for pressure derivative? maybe it is more efficient that way?

added definitions and Object instatiations into FF.H and FF.C so tomorrow test if finally PressureTemporalDerivative gets created