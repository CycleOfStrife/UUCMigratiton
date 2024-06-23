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
    monitor_cmd = ["python3.10", "main.py", container_name, "origin1"]
    monitor_process = subprocess.Popen(monitor_cmd)
    print("监控程序运行中...")
    return monitor_process
def run_load_operations():
    time.sleep(5)
    print(f"启动容器 {container_name}...")
    start_cmd = f"podman start {container_name}"
    subprocess.run(start_cmd+ " > /dev/null 2>&1 & ", shell=True)
    time.sleep(150)
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
