# SnakeAi

Classic Snake game in pygame, using machine learning to optimize AI. Tensorflow Neural Network is optimized through the Genetic Algoritihm. 

## Quick Start
1. Fork the repo

```
$ pipenv install
$ pipenv shell
```
To play the game:

```
$ python human.py
```
To run the genetic algo:

```
$ python genetics.py
```

## Neural Network

Found in classes/NN.py, the Neural network is preset to 24 inputs, 3 outputs, and 1 hidden layer with 14 units.

#### Inputs (In 8 directions around the snake)
1. Food present in that direction
2. Distance to the wall in that direction
3. Snake body present in that direction

#### Outputs (Soft-Max)
1. Turn to the left
2. Turn to the right
3. Don't change direction(stay going foward)

## Genetic Algorithm

Found in classes/mutator.py, the Genetic Algo optimizes the weights of the neural network through breeding and mutating of top performers of the previous generation. 

### Genetic Algo Steps
1. Initialize the population with random weights
2. For each network in the population, play the game and record the score
3. Sort all networks in the population in ascending order by score
4. Choose top performers and keep them in population
5. Randomly choose some less top performers to remain in the population
6. Kill off the rest of the networks
7. For the remaining spaces, breed networks from the networks choosen in step 4-5 ( Breeding consists of choosing a weight between the two parent networks for each weight in the new network)
8. Randomly mutate some attributes of some of the breeded networks(Each weight of each breeded network has a small chance of becoming a random value)
9. Repeact steprs 2 -> 8 for the number of generations


