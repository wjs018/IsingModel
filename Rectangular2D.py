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


def checkFlip(row, col, lattice, temp, J=1, B=0, mu=1):
    """Goes through the Metropolis algorithm to determine whether or not to
    flip the spin at the specified site in the lattice.

    Inputs:
    row        row number of the chosen site
    col        column number of the chosen site
    lattice    the current lattice
    temp       the value for kT in our simulation
    J          coupling constant between neighboring sites
    B          external magnetic field
    mu         magnetic moment of the lattice site


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


def checkEnergyDiff(row, col, lattice, temp, J=1, B=0, mu=1):
    """Calculates the energy difference of a specified site in a lattice
    assuming periodic boundary conditions. The difference is between being
    flipped and not being flipped.

    Inputs:
    row        row number of the chosen site
    col        column number of the chosen site
    lattice    the current lattice
    temp       the value for kT in our simulation
    J          coupling constant between neighboring sites
    B          external magnetic field
    mu         magnetic moment of the lattice site

    Output:
    energy    the energy difference at the given site
    """

    # Get number of rows and columns from lattice

    rows, cols = (lattice.shape[0], lattice.shape[1])

    # Calculate the energy

    energy = 2 * J * lattice[row][col] * (lattice[(row + rows - 1) % rows][col]
                                          + lattice[row][(col + 1) % cols]
                                          + lattice[(row + 1) % rows][col]
                                          + lattice[row][(col + cols - 1) % cols]) + (
                                          2 * B * mu * lattice[row][col])

    return energy

def simulate(rows=100, cols=100, prob=0.5, kT=0.001, J=1, B=0, mu=1, tmax=5000):
    """ This function runs a 2D rectangular lattice Ising model simulation and
    returns the final magentization of the lattice as well as the end result of
    the lattice.
     
    Inputs:
     
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
    lattice    final configuration of the lattice
    """
     
    # Initialize our lattice
     
    lattice = initialize(rows, cols, prob)
     
    # Run our loop
     
    for t in range(0, tmax):
         
        for i in range(0, rows * cols):
             
            # Pick a random site on the lattice
             
            row = random.randint(0, rows - 1)
            col = random.randint(0, cols - 1)
 
            # Decide whether or not this site should be flipped
 
            lattice = checkFlip(row, col, lattice, kT, J=J, B=B, mu=mu)
             
        # Check magnetization
         
        currentMag = abs(magnetization(lattice)) / float(rows * cols)
         
        # Check to see if all the sites are the same spin
         
        if currentMag == 1:
 
            # Absorbing state reached, end simulation
 
            break
            
    # Calculate normalized magnetization
      
    mag = magnetization(lattice) / float(rows * cols)
     
    return (mag, lattice)


if __name__ == '__main__':

    # Initialize lattice of a given size with random 1,-1

    rows=100
    cols=100
    prob=0.5

    lattice=initialize(rows=rows, cols=cols, prob=prob)

    # Set our kT value

    kT=0.003

    # Set our coupling constant

    J=1

    # Set the value of the external magnetic field

    B=0

    # Set the value of magnetic moment of our lattice sites

    mu=1

    # Find magnetization of the lattice, <|M|>

    mag=[abs(magnetization(lattice)) / float(rows * cols)]

    # Plot our starting configuration

    plt.ion()

    plt.pcolormesh(lattice, cmap='winter')
    plt.axis('equal')
    plt.show()

    # Define maximum number of time steps where one time step is rows*cols
    # attempted flip events as well as the plot interval

    tmax=1000
    plotInt=50

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

            row=random.randint(0, rows - 1)
            col=random.randint(0, cols - 1)

            # Decide whether or not this site should be flipped

            lattice=checkFlip(row, col, lattice, kT, J=J, B=B, mu=mu)

        # Calculate magnetization for the time step

        currentMag=abs(magnetization(lattice)) / float(rows * cols)
        mag.append(currentMag)

        # If we have saturated all the sites in one state or another, go ahead
        # and cease simulation

        if currentMag == 1:

            # Absorbing state reached, end simulation

            print('Homogenous state reached')

            break

    plt.ioff()
    plt.clf()
    plt.plot(mag)
    plt.show()
