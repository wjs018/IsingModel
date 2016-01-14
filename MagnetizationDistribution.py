#===============================================================================
# This runs a number of 2D Ising model simulations in order to get a 
# distribution of the resulting magnetization.
#===============================================================================

import multiprocessing as mp
import time
import sys
import matplotlib.pyplot as plt

from Rectangular2D import *


def simulateParallel(args):
    """ This function runs a 2D rectangular lattice Ising model simulation and
    returns the final magentization of the lattice as well as the end result of
    the lattice.
    
    Inputs:
    
    args       Should be a tuple that contains the following in order:
    
    rows       total number of rows in the simulated lattice
    cols       total number of columns in the simulated lattice
    prob       probability of spin 1 when initializing lattice
    kT         the dimensionless temperature of the simulation
    J          coupling constant between neighboring sites
    B          external magnetic field
    mu         magnetic moment of the lattice site
    tmax       maximum number of time steps to simulate
    
    
    Outputs:
    
    mag        ending normalized magnetization of the lattice (sign is kept)
    """
    
    # Unpack our args
    
    rows = args[0]
    cols = args[1]
    prob = args[2]
    kT = args[3]
    J = args[4]
    B = args[5]
    mu = args[6]
    tmax = args[7]
    
    # Run the simulation
    
    mag = simulate(rows=rows, cols=cols, prob=prob, kT=kT, J=J, B=B, mu=mu, tmax=tmax)[0]
    
    return mag


if __name__ == '__main__':
    
    # Make a vector of the temperatures to measure
    
    kTs = np.linspace(0,4,num=30)
    kTs[0] = 0.001
    
    # Initialize some variables
    
    rows = 30
    cols = 30
    prob = 0.5
    J = 1
    B = 0
    mu = 1
    tmax = 1200
    
    # Number of simulations to run at each kT
    
    samples = 100
    
    # Initialize the array to store results
    
    data = np.zeros((kTs.size, samples))
    
    # Counter to keep track of iterations
    
    count = 0
    
    workers = mp.Pool()
    kT = []
    
    # Now we can run our loop
    
    for kTidx in range(0, kTs.size):
         
        # Make a list of kT values that will be iterated through later
         
        kT += [kTs[kTidx]] * samples
        
    # Build arguments for simulation
     
    args = [(rows, cols, prob, temp, J, B, mu, tmax) for temp in kT]
    
    # Run the simulation in parallel
    
    result = workers.map_async(simulateParallel, args, chunksize=1)
    
    # Output the progress of the simulation
 
    while True:
        
        # Keep track of how many jobs to go
        
        remaining = result._number_left * result._chunksize
        
        # Write out to the terminal
        
        sys.stdout.write('\rRemaining: %d   ' % remaining)
        sys.stdout.flush()
         
        time.sleep(0.1)
        
        # If the simulation is done, exit the loop
         
        if result.ready():
             
            sys.stdout.write('\rDone!             \n')
            break
    
    # Close the Pool
    
    workers.close()
    workers.join()
    
    # Get the list of results
    
    endResult = result.get()
    
    # Plot the results
    
    plt.plot(kT, endResult, 'ko')
    plt.show()