[**中文版本**](README.zh-CN.md)
# Chrome Network Traffic Capture Tool

This is a tool that uses Selenium and tshark to automatically capture network traffic from the Chrome browser. It can automatically open the Chrome browser, perform predefined user behaviors (such as searching), capture network traffic and save it as a pcap file, and save SSL/TLS key logs.

## Features

- Automatically launch Chrome browser and visit specified web pages
- Perform predefined user interaction behaviors (such as clicking search box and entering random strings for searching)
- Simultaneously capture network traffic using tshark
- Save SSL/TLS decryption key logs
- Automatically repeat experiments multiple times and save results
- Automatic counting and error logging

## File Descriptions

- `main.py`: Main program file, controls the entire capture process
- `config.py`: Configuration file, contains configuration information such as Chrome path, network interface, and target URL
- `counter.txt`: Counter file, records the current data collection number (automatically generated)
- `error.txt`: Error log file, records the data numbers with errors during execution

## Configuration Instructions

The following parameters need to be configured in `config.py`:

- `chrome_path`: Chrome browser executable file path
- `ssl_key_log_file`: SSL key log file path
- `interface`: Network interface name (for tshark capture)
- `tshark_path`: tshark executable file path
- `url`: Target website URL
- `file_name`: Application name, part of the file name
- `behavior_name`: Behavior name, part of the file name
- `behavior_num`: Number of behavior repetitions

## Usage

1. Ensure Chrome browser with compatible browser driver and Wireshark (including tshark) are installed
2. Set the SSLKEYLOGFILE environment variable to the SSL key log file path
3. Install Python dependencies:
4. Run the main.py file (need to write browser operation scripts yourself)