[**English Version**](README.md)
# Chrome网络流量捕获工具

这是一个使用Selenium和tshark自动捕获Chrome浏览器网络流量的工具。它能够自动打开Chrome浏览器，执行预定义的用户行为（如搜索），同时捕获网络流量并保存为pcap文件，以及保存SSL/TLS密钥日志。

## 功能特点

- 自动启动Chrome浏览器并访问指定网页
- 执行预定义的用户交互行为（如点击搜索框并输入随机字符串进行搜索）
- 同时使用tshark捕获网络流量
- 保存SSL/TLS解密所需的密钥日志
- 自动重复执行多次实验并保存结果
- 自动计数和错误记录

## 文件说明

- `main.py`: 主程序文件，控制整个捕获流程
- `config.py`: 配置文件，包含Chrome路径、网络接口、目标URL等配置信息
- `counter.txt`: 计数器文件，记录当前采集数据的编号（自动生成）
- `error.txt`: 错误日志文件，记录执行过程中出现的错误的数据编号

## 配置说明

在`config.py`中需要配置以下参数：

- `chrome_path`: Chrome浏览器可执行文件路径
- `ssl_key_log_file`: SSL密钥日志文件路径
- `interface`: 网络接口名称（用于tshark捕获）
- `tshark_path`: tshark可执行文件路径
- `url`: 目标网站URL
- `file_name`: 应用名，文件名的一部分
- `behavior_name`: 行为名称，文件名的一部分
- `behavior_num`: 行为重复次数

## 使用方法

1. 确保已安装支持浏览器驱动的Chrome浏览器和Wireshark（包含tshark）
2. 设置环境变量SSLKEYLOGFILE为SSL密钥日志文件路径 
3. 安装Python依赖： 
4. 运行main.py文件（需要自己编写浏览器操作脚本，）