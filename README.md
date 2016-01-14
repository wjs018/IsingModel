# IsingModel

This is a simulation of the Ising Model of ferromagnetism. To learn more about the model and its uses, check out the wikipedia page [here](https://en.wikipedia.org/wiki/Ising_model). In this simulation, the Metropolis algorithm is applied.

At the moment, this consists of two python programs:

1. Rectangular2D.py - This does the heavy lifting of simulating a 2D lattice with up and down spins. The `simulate` function in this file can be used to perform a single simulation with user defined parameters. For descriptions of the parameters, check the function description in the file.
2. MagnetizationDistribution.py - This can be used to perform many simulations to build up a distribution of what the resulting distribution of magnetizations looks like for a given set of parameter variations. The `__main__` function utilizes the `multiprocessing` module to perform these simulations in parallel using the defined `simulateParallel` function. An example of the output can be seen [here](http://i.imgur.com/b6e4LjU.png).

## Dependencies

* Python 2.x (tested 2.7.6)

## Future Work

At some point I hope to include more options including, but not limited to:

* Hexagonal Lattice
* 1D and 3D lattices
* Longer range interactions
* Cluster detection/Percolation checking
* Metastable state detection

## Contact

* Walter Schwenger, wjs018@gmail.com
