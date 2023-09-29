# Set MPI_HOME by quering path loaded by site module
export MPI_HOME=$(which mpicc | sed s/'\/bin\/mpicc'//)

# Path to parallel HDF5 installtion with fortran support
export HDF5_HOME=$(which h5pfc | sed s/'\/bin\/h5pfc'//)
