# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 09:54:49 2025

@author: m.lotfi
"""
import random
import time

def generate_random_delay_gauss(mu = 5.0, sigma = 2.0, t_min = 1.0, t_max = 10.0):
    """
    Generate a random delay time based on a normal distribution, within specified bounds.
    
    :param mu: Mean of the normal distribution (seconds).
    :param sigma: Standard deviation of the distribution (seconds).
    :param t_min: Minimum delay time in seconds.
    :param t_max: Maximum delay time in seconds.
    :return: A float representing a random delay time in seconds.
    
    # Example usage:
    t_min = 1.0  # Minimum delay time in seconds
    t_max = 10.0  # Maximum delay time in seconds
    mu = 5.0      # Mean of the distribution
    sigma = 2.0   # Standard deviation
    
    """
    while True:
        # Generate a random delay based on normal distribution
        delay = random.gauss(mu, sigma)
        # Ensure the delay is within the specified bounds
        if t_min <= delay <= t_max:
            return delay