# This script generates 3D coarse density fields of the ICs for the ML 
# project with Chi-Ting
from mpi4py import MPI
import numpy as np
import sys,os
import MAS_library as MASL

###### MPI DEFINITIONS ######                                    
comm   = MPI.COMM_WORLD
nprocs = comm.Get_size()
myrank = comm.Get_rank()


# This routine computes the density field of a snapshot and save results to file
def density_field(snapshot, ptypes, grid, MAS, do_RSD, axis, fout):
    df = MASL.density_field_gadget(snapshot, ptypes, grid, MAS=MAS,
                                   do_RSD=do_RSD, axis=axis, verbose=True)
    #df = df/np.mean(df, dtype=np.float64)-1.0
    np.save(fout, df)



####################################### INPUT ##########################################
root         = '/simons/scratch/fvillaescusa/pdf_information'
root_out     = '/simons/scratch/fvillaescusa/high_resolution_ML/results'
ptypes       = [1]
MAS          = 'CIC'
do_RSD       = False
axis         = 0
realizations = 1000
########################################################################################

# create output folders
for cosmo_out in ['LR', 'HR']:
    folder_out = '%s/%s/'%(root_out, cosmo_out)
    if myrank==0 and not(os.path.exists(folder_out)):  
        os.system('mkdir %s'%folder_out)
    comm.Barrier()

# find the numbers that each cpu will work with                  
numbers = np.where(np.arange(realizations)%nprocs==myrank)[0]

# do a loop over all realizations
for i in numbers:

    ################# LR (z=0) ##################
    # find the name of the output file
    fout = '%s/%s/df_%d_z=0.npy'%(root_out,'LR',i)
    if os.path.exists(fout):  continue
    
    # compute the density field and save it to file
    grid = 256
    snapshot = '%s/%s/%d/snapdir_004/snap_004'%(root,'fiducial_LR',i)
    density_field(snapshot, ptypes, grid, MAS, do_RSD, axis, fout)
    #############################################

    ################# HR (z=0) ##################
    # find the name of the output file
    fout = '%s/%s/df_%d_z=0.npy'%(root_out,'HR',i)
    if os.path.exists(fout):  continue
    
    # compute the density field and save it to file
    grid = 512
    snapshot = '%s/%s/%d/snapdir_004/snap_004'%(root,'fiducial',i)
    density_field(snapshot, ptypes, grid, MAS, do_RSD, axis, fout)
    #############################################

    ################ HR (z=127) #################
    # find the name of the output file
    fout = '%s/%s/df_%d_z=127.npy'%(root_out,'HR',i)
    if os.path.exists(fout):  continue
    
    # compute the density field and save it to file
    grid = 512
    snapshot = '%s/%s/%d/ics'%(root,'fiducial',i)
    density_field(snapshot, ptypes, grid, MAS, do_RSD, axis, fout)
    #############################################
