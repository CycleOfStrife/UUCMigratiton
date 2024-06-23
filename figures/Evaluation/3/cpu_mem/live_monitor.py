import subprocess
import time
import signal
import os
import datetime
def is_container_running(name):
    # 执行 `docker ps` 命令来获取当前运行的容器列表
    result = subprocess.run(['podman', 'ps'], stdout=subprocess.PIPE)
    # 检查容器名称是否在命令输出中
    return name in result.stdout.decode()

container_name = "mycri_2"
def run_monitor():
    print("启动监控程序...")
    monitor_cmd = ["python3.10", "main.py", container_name, "live1"]
    monitor_process = subprocess.Popen(monitor_cmd)
    print("监控程序运行中...")
    return monitor_process
def calculate_transfer_time(file_path, bandwidth_mbps):
    """
    Calculate the time required to transfer a file over a network given the bandwidth.

    Parameters:
        file_path (str): The path to the file.
        bandwidth_mbps (float): The network bandwidth in Mbps.

    Returns:
        float: The time required to transfer the file in seconds.
    """
    # Check if the file exists
    if not os.path.exists(file_path):
        return "File does not exist"

    # Get the file size in bytes
    file_size_bytes = os.path.getsize(file_path)

    # Convert file size to bits
    file_size_bits = file_size_bytes * 8

    # Convert bandwidth from Mbps to bits per second
    bandwidth_bps = bandwidth_mbps * 1_000_000

    # Calculate the transfer time in seconds
    transfer_time_seconds = file_size_bits / bandwidth_bps

    return transfer_time_seconds
def run_load_operations():
    time.sleep(5)
    print(f"启动容器 {container_name}...")
    start_cmd = f"podman start {container_name}"
    subprocess.run(start_cmd+ " > /dev/null 2>&1 & ", shell=True)
    time.sleep(50)
    print("创建容器检查点...")
    chk_t = datetime.datetime.now()
    #checkpoint_cmd = "podman container checkpoint --log-level debug  --tcp-established --live-migration --predict-model lsh --iter 3 memswcontainer"
    checkpoint_cmd = f"podman container checkpoint  --tcp-established -P {container_name}"
    subprocess.run(checkpoint_cmd + " > /dev/null 2>&1 ", shell=True)
    checkpoint_cmd = f"podman container checkpoint  --tcp-established --with-previous {container_name}"
    subprocess.run(checkpoint_cmd + " > /dev/null 2>&1 ", shell=True)
    chk_t_end = datetime.datetime.now()
    print(f"chk_t = {chk_t},chk_t_end={chk_t_end}")
    # Example usage
    file_path = "/var/lib/containers/storage/overlay-containers/ca4d2e6797af4bca1b8499dc0c361b672c9c04bc5ca86f74fc03cd8c5c0ffb39/userdata/checkpoint"
    bandwidth_mbps = 100  # Bandwidth in Mbps

    transfer_time = calculate_transfer_time(file_path, bandwidth_mbps)
    print(f"检查点创建完成, 等待{transfer_time}秒...")
    time.sleep(transfer_time)

    print("恢复容器操作...")
    #restore_cmd = "podman container restore --log-level debug --print-stats --live-migration --tcp-established memswcontainer"
    restore_cmd = f"podman container restore --log-level debug --print-stats --tcp-established  {container_name}"
    #subprocess.run(restore_cmd + " > /dev/null 2>&1 ", shell=True)
    subprocess.run(restore_cmd, shell=True)
    print("容器恢复操作完成。")
    time.sleep(50)
    # while True:
    #     if is_container_running(container_name):
    #         print(f"Container {container_name} is still running.")
    #         time.sleep(10)  # 每10秒检查一次
    #     else:
    #         print(f"Container {container_name} has stopped.")
    #         break  # 如果容器不再运行，退出循环
def main():
    try:
        
        monitor_process = run_monitor()
        run_load_operations()
    finally:
        print("正在停止监控程序...")
        monitor_process.send_signal(signal.SIGINT)
        monitor_process.wait()
        print("监控程序已停止。")
        

if __name__ == "__main__":
    main()
