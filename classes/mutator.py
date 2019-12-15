import random
import math
import copy
from classes.NN import Network


class Mutator(object):
    # Choose top x networks, choose y bad networks
    # Randomly mutate some weights of some of the neural networks
    # Breed z new networks with combo from some of the parents

    def __init__(self, mutate_chance, retain_top_ratio, retain_rest_ratio):
        self.mutate_chance = mutate_chance
        self.retain_top_ratio = retain_top_ratio
        self.retain_rest_ratio = retain_rest_ratio

    def generate_new_networks(self, networks):
        total_len = len(networks)

        networks = self.choose_parent_networks(networks)
        self.breed_children_networks(networks, total_len)

        return networks

    def choose_parent_networks(self, networks):
        split_index = math.ceil(len(networks)*self.retain_top_ratio)
        new_networks = networks[:split_index]

        for network in networks[split_index + 1:]:
            if self.retain_rest_ratio > random.random():
                new_networks.append(network)

        return new_networks

    def breed_children_networks(self, networks, total_len):
        parents = networks[:]

        while len(networks) < total_len:
            parent1 = parent2 = random.choice(parents)
            while parent2 == parent1:
                parent2 = random.choice(parents)

            networks.append(self.breed_network(parent1, parent2))

    def breed_network(self, parent1, parent2):
        new_network = Network()

        p1_weights = parent1.get_weights()
        p2_weights = parent2.get_weights()
        new_weights = new_network.get_weights()

        for index in range(len(new_weights)):
            if not index % 2:
                for index2 in range(len(new_weights[index])):
                    for index3 in range(len(new_weights[index][index2])):
                        new_weights[index][index2][index3] = random.choice(
                            [p1_weights[index][index2][index3],
                             p2_weights[index][index2][index3]])
            else:
                for index2 in range(len(new_weights[index])):
                    new_weights[index][index2] = random.choice([p1_weights[index][index2], p2_weights[index][index2]])

        new_network.set_weights(new_weights)

        self.mutate(new_network)

        return new_network

    def mutate(self, network):
        weights = network.get_weights()

        for index in range(len(weights)):
            if not index % 2:
                for index2 in range(len(weights[index])):
                    for index3 in range(len(weights[index][index2])):
                        if self.mutate_chance > random.random():
                            weights[index][index2][index3] = random.uniform(-1.0, 1.0)
            else:
                for index2 in range(len(weights[index])):
                    if self.mutate_chance > random.random():
                        weights[index][index2] = random.uniform(-1.0, 1.0)

        network.set_weights(weights)

        return
