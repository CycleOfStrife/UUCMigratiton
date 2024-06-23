import argparse  # 导入argparse库来解析命令行参数
import time
import monitorInside as  monitorContainer  # 容器内部
import monitor as monitorSystem # 容器外部
import os
import logger  # 确保logger模块包含setup_logger函数
import shutil
def main(container_id,logs):
    # 设置日志
    
    
    logs_dir = 'logs_'+ logs
    # 检查是否存在logs目录，如果不存在，则创建
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    else:
        for filename in os.listdir(logs_dir):
            file_path = os.path.join(logs_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
    # 定义监控间隔（以秒为单位）
    monitor_interval = 1  # 比如，每分钟监控一次

    log = logger.setup_logger('performance_monitor', os.path.join(logs_dir,'performance_monitor.log'))
    log.info("Starting the performance monitoring for container: " + container_id + ". Press Ctrl+C to stop.")
    log_csv=os.path.join(logs_dir,'usage_logs.csv')
    log_system_csv=os.path.join(logs_dir,'usage_system_logs.csv')
    try:
        while True:
            # 获取系统使用情况数据
            usage_data = monitorContainer.get_container_usage(container_id)
            log.info(f"Logged data: {usage_data}")  # 使用log.info替换print
            
            # 记录数据
            monitorContainer.log_usage(usage_data,log_csv)

            system_data = monitorSystem.get_system_usage()
            log.info(f"Logged data: {usage_data}")  # 使用log.info替换print
            
            # 记录数据
            monitorSystem.log_usage(system_data,log_system_csv)

            # 等待下一个间隔
            time.sleep(monitor_interval)
    except KeyboardInterrupt:
        log.info("Monitoring stopped by user.")
    except Exception as e:
        log.error(f"An error occurred: {e}")  # 使用log.error替换print
    finally:
        log.info("Performance monitoring script has been terminated.")

if __name__ == "__main__":
    # 使用argparse解析命令行参数以获取容器ID
    parser = argparse.ArgumentParser(description="Monitor a Podman container's performance.")
    parser.add_argument('container_id', type=str, help='The ID of the container to monitor.')
    parser.add_argument('logs', type=str, help='LogDir Name')
    args = parser.parse_args()

    main(args.container_id, args.logs)