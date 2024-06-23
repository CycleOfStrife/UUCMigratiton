import subprocess
import datetime
import csv
import os
from typing import Dict, Any

def get_container_usage(container_id: str) -> Dict[str, Any]:
    """
    Retrieves current Podman container resource usage including CPU and memory.

    Args:
        container_id (str): The ID of the container to monitor.

    Returns:
        Dict[str, Any]: A dictionary containing 'cpu' and 'memory' usage for the specified container.
    """
    command = f"podman stats --no-stream --format '{{{{.CPUPerc}}}},{{{{.MemPerc}}}}' {container_id}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    # Check for errors or empty output which indicates the container might not be running
    if result.stderr or not result.stdout.strip():
        print(f"Container {container_id} might not be running. Setting values to 0.")
        # Setting all values to 0 if container is not running or if there's an error
        return {
            'time': datetime.datetime.now(),
            'container_id': container_id,
            'cpu': '0%',
            'memory': '0%',
        }

    cpu_usage, memory_usage = result.stdout.strip().split(',')

    return {
        'time': datetime.datetime.now(),
        'container_id': container_id,
        'cpu': cpu_usage,
        'memory': memory_usage,
    }

def log_usage(data, file_path='logs/container_usage_logs.csv'):
    """
    Logs the container usage data to a CSV file.

    Args:
        data: The data to log, expected to be a dictionary with keys
              'time', 'container_id', 'cpu', and 'memory'.
        file_path: The path to the log file.
    """
    # The fields for CSV file
    fieldnames = ['time', 'container_id', 'cpu', 'memory']
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
