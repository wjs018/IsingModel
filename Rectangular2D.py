#=========================================================================
# This simulates a 2D Ising Model ferromagnet with a rectangular lattice.
#=========================================================================

import numpy as np
import random
import math
import matplotlib.pyplot as plt


def initialize(rows=50, cols=50, prob=0.5):
    """Initialize a rectangular 2D lattice of a given size with a given
    probability of each site getting a positive 1 value.

    Inputs:
    rows    number of rows in the lattice
    cols    number of columns in the lattice
    prob    probability of each site getting a positive value

    Output:
    lattice    the resulting initialized lattice
    """

    lattice = np.random.choice([1, -1], size=(rows, cols), p=[prob, 1 - prob])

    return lattice


def magnetization(lattice):
    """Sums the array to find the magnetization of the lattice."""

    mag = np.sum(lattice)

    return mag


def checkFlip(row, col, lattice, temp, J=1):
    """Goes through the Metropolis algorithm to determine whether or not to
    flip the spin at the specified site in the lattice.

    Inputs:
    row        row number of the chosen site
    col        column number of the chosen site
    lattice    the current lattice
    temp       the value for kT in our simulation
    J          coupling constant between neighboring sites


    Output:
    newLattice    the lattice after the site has either been flipped or not
    """

    # First, calculate energy difference between flipping and not flipping

    diffEnergy = checkEnergyDiff(row, col, lattice, temp)

    # Compare energies

    if diffEnergy <= 0:

        # Flip was energy neutral or beneficial, it is kept

        lattice[row][col] = -1 * lattice[row][col]

        return lattice

    else:

        # Flip was energy costly, flip is only kept with Boltzmann probability

        BoltzFactor = math.exp(-diffEnergy / temp)

        if random.random() < BoltzFactor:

            # Flip is kept

            lattice[row][col] = -1 * lattice[row][col]

            return lattice

        else:

            # Flip is not kept

            return lattice


def checkEnergyDiff(row, col, lattice, temp, J=1):
    """Calculates the energy of a specified site in a lattice assuming
    periodic boundary conditions.

    Inputs:
    row        row number of the chosen site
    col        column number of the chosen site
    lattice    the current lattice
    temp       the value for kT in our simulation
    J          coupling constant between neighboring sites

    Output:
    energy    the energy at the given site
    """

    # Get number of rows and columns from lattice

    rows, cols = (lattice.shape[0], lattice.shape[1])

    # Calculate the energy

    energy = 2 * J * lattice[row][col] * (lattice[(row + rows - 1) % rows][col]
                                          + lattice[row][(col + 1) % cols]
                                          + lattice[(row + 1) % rows][col]
                                          + lattice[row][(col + cols - 1) % cols])

    return energy


if __name__ == '__main__':

    # Initialize lattice of a given size with random 1,-1

    rows = 50
    cols = 50
    prob = 0.5

    lattice = initialize(rows=rows, cols=cols, prob=prob)

    # Set our kT value

    kT = 0.003
    
    # Set our coupling constant
    
    J = 1

    # Find magnetization of the lattice, <|M|>

    mag = [abs(magnetization(lattice)) / float(rows * cols)]
    
    # Plot our starting configuration
    
    plt.ion()
    
    plt.pcolormesh(lattice, cmap='winter')
    plt.axis('equal')
    plt.show()

    # Define maximum number of time steps where one time step is rows*cols
    # attempted flip events as well as the plot interval

    tmax = 1000
    plotInt = 50

    # Now we are ready to start our time loop

    for t in range(0, tmax):
        
        # Occasionally plot our lattice
        
        if t % plotInt == 0:
            
            plt.pcolormesh(lattice, cmap='winter')
            plt.axis('equal')
            plt.draw()

        # Now do a loop that iterates rows*cols times

        for i in range(0, rows * cols):

            # First, pick a random site on our lattice

            row = random.randint(0, rows - 1)
            col = random.randint(0, cols - 1)

            # Decide whether or not this site should be flipped

            lattice = checkFlip(row, col, lattice, kT, J=J)

        # Calculate magnetization for the time step

        mag.append(abs(magnetization(lattice)) / float(rows * cols))
      
    plt.ioff()
    plt.clf()
    plt.plot(mag)
    plt.show()