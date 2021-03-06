#!/Users/dtg/Dropbox/UC_2014/S2/264/env/bin/python

'''
Authors:    Dillon George and Carl Kenny
Program:    Simulates a BSC, modelled using a binomial distribution.
'''

import hamming
import distribution
from sys import argv
import numpy as np


def efficiency(data_size, num_transmissions, message_len):
    return data_size / (num_transmissions * message_len)


def average_efficiency(efficiencies):
    return sum(efficiencies) / len(efficiencies)


def simulate(num_simulations, error_rate, user_data, redundant_bits):
    efficiencies = []
    k = 100 + user_data
    message_len = k + redundant_bits
    total_submissions = 0
    num_transmissions = 0
    bound = hamming.hamming_bound(message_len, k)

    for _ in range(num_simulations):

        # Send one package
        num_errors = distribution.num_errors(message_len, error_rate)

        # While not successful
        num_transmissions = 1
        while num_errors > bound:
            num_errors = distribution.num_errors(message_len, error_rate)
            num_transmissions += 1
        eff = efficiency(user_data, num_transmissions, message_len)
        efficiencies.append(eff)

        total_submissions += num_transmissions

    return average_efficiency(efficiencies)


def prob_sim(prob_min, prob_max, prob_step, num_sims, user_data):
    ''' Perform multiple simulations '''
    avg_efficiencies = []
    error_rates = np.arange(prob_min, prob_max, prob_step)

    # Calculate redundant bits
    redundant_bits = int(np.ceil((user_data + 100) * 0.1))

    for error in error_rates:
        avg_efficiencies.append(simulate(num_sims, error,
                                         user_data, redundant_bits))


    return error_rates, avg_efficiencies



if __name__ == "__main__":
    '''
    Command line parameters:
        -u data size u
        -p bit error probability
        -r number of redundant bits n-k
    '''
    overhead = 100
    num_simulations = 10 ** 6

    # Get simulation Parameters
    if len(argv) > 1:
        user_data = int(argv[argv.index("-u") + 1])
        error_rate = float(argv[argv.index("-p") + 1])
        redundant_bits = int(argv[argv.index("-r") + 1])

    else:   # Interactive Mode
        user_data = int(input("Data size (int): "))
        error_rate = float(input("Independent bit probability error (float): "))
        redundant_bits = int(input("Redundant bit size (int):"))

    message_len = user_data + overhead + redundant_bits

    average_efficiency = simulate(num_simulations, error_rate,
                                  user_data, message_len)

    print(average_efficiency)
