# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 20:58:12 2025

@author: m.lotfi
"""

def bytes_to_human_readable(num_bytes: int) -> str:
    """
    Convert a byte count to a human-readable file size format.

    This function takes an integer representing the number of bytes and converts it
    into a string with an appropriate size unit (B, KB, MB, GB, TB, etc.), rounded
    to two decimal places.

    Args:
        num_bytes (int): The number of bytes to convert. Must be a non-negative integer.

    Returns:
        str: A string representing the human-readable file size.

    Raises:
        ValueError: If num_bytes is negative.
    """
    # Validate input
    if num_bytes < 0:
        raise ValueError("num_bytes must be non-negative")
    
    # List of size units in ascending order
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']
    index = 0  # Index to track the current unit

    # Convert num_bytes to the appropriate unit
    while num_bytes >= 1024 and index < len(units) - 1:
        num_bytes /= 1024.0  # Scale num_bytes down by 1024
        index += 1           # Move to the next unit

    # Format the number with two decimal places and append the unit
    human_readable = f"{num_bytes:.2f} {units[index]}"
    return human_readable