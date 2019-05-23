from mpi4py import MPI
import numpy as np
import readgadget
import sys,os

###### MPI DEFINITIONS ######                                    
comm   = MPI.COMM_WORLD
nprocs = comm.Get_size()
myrank = comm.Get_rank()


#################################### INPUT ##############################################
root         = '/simons/scratch/fvillaescusa/pdf_information'
root_out     = '/simons/scratch/fvillaescusa/HR_ML/results'
cosmo        = 'fiducial_LR'
BoxSize      = 1000.0 #Mpc/h
ptype        = [1]
snapnum      = 4
realizations = 1000
#########################################################################################

middle = BoxSize/2.0

# find the numbers that each cpu will work with                  
numbers = np.where(np.arange(realizations)%nprocs==myrank)[0]

# do a loop over the different realizations
for i in numbers:

    print i

    # find the name of the output file
    fout = '%s/LR/displacement_%d_z=0.npy'%(root_out,i)
    if os.path.exists(fout):  continue
    
    # find the name of the snapshots
    snap1 = '%s/%s/%d/ICs/ics'%(root,cosmo,i)
    snap2 = '%s/%s/%d/snapdir_%03d/snap_%03d'%(root,cosmo,i,snapnum,snapnum)

    # read the positions and IDs of the ICs. Sort positions by particle IDs
    pos1 = readgadget.read_block(snap1, "POS ", ptype)/1e3 #positions in Mpc/h
    IDs1 = readgadget.read_block(snap1, "ID  ", ptype)-1   #normalized
    indexes = np.argsort(IDs1)
    pos1 = pos1[indexes]

    # read the positions and IDs of the z=0 snap. Sort positions by particle IDs
    pos2 = readgadget.read_block(snap2, "POS ", ptype)/1e3 #positions in Mpc/h
    IDs2 = readgadget.read_block(snap2, "ID  ", ptype)-1   #normalized
    indexes = np.argsort(IDs2)
    pos2 = pos2[indexes]

    # compute displacement field and care about boundary conditions
    disp = pos2-pos1
    indexes = np.where(disp>middle)
    disp[indexes] -= BoxSize
    indexes = np.where(disp<-middle)
    disp[indexes] += BoxSize

    # save results to file
    np.save(fout, disp)
