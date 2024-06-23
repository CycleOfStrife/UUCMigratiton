# monitor.py

import psutil
import datetime
import csv
import os
from typing import Dict, Any

def get_system_usage() -> Dict[str, Any]:
    """
    Retrieves current system resource usage including CPU, memory, and I/O.

    Returns:
        Dict[str, Any]: A dictionary containing 'cpu', 'memory', and 'io' usage.
    """
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    io_counters = psutil.disk_io_counters()
    io_read = io_counters.read_bytes
    io_write = io_counters.write_bytes

    return {
        'time': datetime.datetime.now(),
        'cpu': cpu_usage,
        'memory': memory_usage,
        'io_read': io_read,
        'io_write': io_write
    }

def log_usage(data, file_path='logs/usage_logs.csv'):
    """
    Logs the system usage data to a CSV file.

    Args:
        data: The data to log, expected to be a dictionary with keys
              'time', 'cpu', 'memory', 'io_read', and 'io_write'.
        file_path: The path to the log file.
    """
    # The fields for CSV file
    fieldnames = ['time', 'cpu', 'memory', 'io_read', 'io_write']
    # Check if the file exists to write headers only on the first time
    file_exists = os.path.isfile(file_path)

    try:
        with open(file_path, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()  # Write the header only if the file is new
            writer.writerow(data)
    except Exception as e:
        print(f"Error logging data: {e}")