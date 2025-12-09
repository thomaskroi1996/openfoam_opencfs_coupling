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

The most up-do-date branches are thk_precice_opencfs or Candussi_kroppert_precice_opencfs (for test cases)

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
- acouRhsLoad on internal exists twice in resultContexts, but one time the result functor is 0, eventually leading to a "cannot access element 0 of Vector with size 0" error when the output starts, and simulation fails. Why does it exist twice?

- Artefacts in the source region, likely some issue with reading in nodal values

## Notes
- oldTime() method in Adapter.C and writeCheckpoint for pressure derivative? maybe it is more efficient that way?
- in FF.C we add CouplingDataWriters.

## Changes made in openCFS and openfoam_adapter

### openCFS:

These commits are all on the thk_precice_opencfs branch of openCFS.

- add a lot of std::cout for debugging
- 13f0d569: move if statement to check result type because dimDof was not set yet in CoefFunctionGridNodalDefaultPrecice.cc
- 7e1e4b77: call GetNodeResult instead of GetElemResult in CoefFunctionGridNodalDefaultPrecice.cc
- 36a303ae: check if we have a result functor in ResultHandler.cc
    - this is just a workaround, we shouldn't have to change ResultHandler.cc to make this work. this issue is connected to the problem of having acouRhsLoad twice in our results, one time with a result functor that is 0, so the error is thrown, and therefore we had to move it out. ideally, acouRhsLoad would only be once in the results, with a non 0 result functor
- 1912b112: map the precice variable Pressure (or PressureTemporalDerivative) to acouRhsLoad solutiontype in PreciceAdapter.cc

### openfoam_adapter:
These commits are all on the dp_dt branch of my personal fork of the openfoam_adapter (the one you installed with the link above).

- first write a simple skeleton of how the derivative could look like, by implementing a new class PressureTemporalDerivative (.C & .H) that inherits from CouplingDataWriter.
- improve upon this sketch, initialise pOld_ (which is p(t-1), definitely should be renamed if we implement higher order schemes) to a buffer instead of openFoam object
- make the necessary changes in Adapter, FF, PressureTemporalDerivative, Interface .C and .H files, so that the new class gets correctly called when we have PressureTemporalDerivative in openFoam_dpdt/system/preciceDict.

## Further steps:
Number 1 priority should be fixing reading nodal values, so that we don't have artefacts
    - write temporal derivative to file

Right hand side values is not written out

Only source region -> whole pipeline, check interpolation, grids, and use 3D only

write hashmap functionality to write pressure out