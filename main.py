import time
import psutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import config
import tqdm
import os
import shutil
import subprocess
from selenium.webdriver.common.by import By
import random
import string
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common import keys
def generate_random_string():
    # 随机生成字符串的长度，例如从1到20
    length_of_string = random.randint(1, 6)
    # 定义字符集合，包括大写字母、小写字母和数字
    characters = string.ascii_letters + string.digits
    # 使用random.choices()方法从字符集合中随机选择字符
    random_string = ''.join(random.choices(characters, k=length_of_string))
    return random_string, length_of_string

def load_counter(file_path='counter.txt'):
    """从文件中加载计数器的值"""
    try:
        with open(file_path, 'r') as file:
            return int(file.read().strip())  # 读取文件并转换为整数
    except FileNotFoundError:
        return 0  # 如果文件不存在，则从0开始

def save_counter(counter, file_path='counter.txt'):
    """将计数器的值保存到文件中"""
    with open(file_path, 'w') as file:
        file.write(str(counter))

def clear_ssl_key_log_file(ssl_key_log_file):
    """
    Clear the contents of the SSL key log file.

    :param ssl_key_log_file: Path to the SSL key log file.
    """
    try:
        with open(ssl_key_log_file, 'w') as file:
            file.truncate(0)
        print(f"SSL key log file cleared: {ssl_key_log_file}")
    except Exception as e:
        print(f"Error clearing SSL key log file: {e}")

def terminate_chrome_processes():
    """
    Terminate all running Chrome processes.
    """
    try:
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == 'chrome.exe':
                proc.terminate()
                proc.wait()
        print("Terminated all Chrome processes.")
    except Exception as e:
        print(f"Error terminating Chrome processes: {e}")


def copy_and_rename_ssl_key_log_file(original_path, new_file_name):
    """
    将原始文件复制到当前文件夹并重命名为自定义文件名。

    :param original_path: 原始文件的路径
    :param new_file_name: 新文件的自定义文件名
    """
    try:
        # 获取当前文件夹路径
        current_folder = os.getcwd()

        # 新文件路径
        new_file_path = os.path.join(current_folder, new_file_name)

        # 复制并重命名文件
        shutil.copy(original_path, new_file_path)

        print(f"文件已复制并重命名为: {new_file_path}")
    except Exception as e:
        print(f"Error copying and renaming SSL key log file: {e}")


def click_page(driver, j):
    if j > 0:
        actions2 = ActionChains(driver)
        actions2.move_by_offset(1288, 25)
        actions2.click()
        actions2.perform()
        actions2.reset_actions()
    random_string, length = generate_random_string()
    actions = ActionChains(driver)
    actions.move_by_offset(305, 32)
    actions.click()
    actions.perform()
    time.sleep(1)
    actions.send_keys(random_string)
    actions.perform()
    time.sleep(1)
    actions.send_keys(keys.Keys.RETURN)
    # actions.move_by_offset(530, 0)
    # actions.click()
    # actions.move_by_offset(530, 0)
    actions.perform()
    actions.reset_actions()


if __name__ == "__main__":
    ssl_key_log_file = config.ssl_key_log_file
    # Full path to the Chrome executable
    chrome_path = config.chrome_path  # Update this path if needed
    # Network interface to capture packets
    interface = config.interface  # Replace with your network interface name on Windows
    # Full path to the tshark executable
    tshark_path = config.tshark_path  # Update this path if needed
    # Duration to capture packets (in seconds)
    capture_duration = config.capture_duration
    opt = Options()
    opt.binary_location = chrome_path
    opt.add_argument(r'--user-data-dir=C:\Users\hua\AppData\Local\Google\Chrome for Testing\User Data')
    opt.add_experimental_option('excludeSwitches', ['enable-automation'])
    repeat_num = 1500
    with open('error.txt', 'a') as file:
        file.write(config.file_name + '_'+config.behavior_name+':\n')
    for i in range(repeat_num):
        try:
            counter = load_counter()  # 加载计数器的值
            pre_name = os.path.join('capture_pcap', config.file_name+'_'+config.behavior_name, config.file_name + '_'+config.behavior_name+'_' + f'{counter}')
            counter += 1  # 增加计数器的值
            save_counter(counter)  # 保存更新后的计数器值
            # Ensure the directory exists
            os.makedirs(os.path.dirname(pre_name), exist_ok=True)
            # Output file to save captured packets and sslkeylog
            pcap_name = f'{pre_name}.pcap'
            sslkeylog_name = f'{pre_name}.txt'
            # Clear the SSL key log file
            clear_ssl_key_log_file(ssl_key_log_file)
            tshark_command = [
                tshark_path,
                '-i', interface,
                '-w', pcap_name
            ]
            # Start the tshark process
            tshark_process = subprocess.Popen(tshark_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # random_string, length = generate_random_string()

            # 由于selenium是通过driver去操作浏览器的，所以我们需要对应浏览器的driver对象
            driver = webdriver.Chrome(options=opt)
            driver.get(config.url)
            time.sleep(10)
            print("网页加载完毕")
            # time.sleep(1)
            # for j in range(config.behavior_num):
            #     try:
            #         click_page(driver, j)
            #         time.sleep(10)
            #     except Exception as e:
            #         print('没有找到按钮')
            #         with open('error.txt', 'a') as file:
            #             file.write(str(counter-1) + '\n')

            tshark_process.terminate()
            tshark_process.wait()
            tshark_process.kill()
            time.sleep(5)
            # Rename the SSL key log file
            copy_and_rename_ssl_key_log_file(ssl_key_log_file, sslkeylog_name)
            # 关闭浏览器进程
            driver.close()
        finally:
            subprocess.run(['taskkill', '/F', '/IM', 'dumpcap.exe'], check=False)
        print("抓包结束")

