# Minecraft Acceleration with OProxy

**Version:** 1.0.4               
**Author:** GreshAnt

## Overview
OProxy is a Python utility tailored for accelerating Minecraft gameplay by managing proxy and transit server configurations on Ubuntu Linux. It simplifies downloading, executing system commands, managing packages, handling JSON configurations, and setting up systemd services.

## Features
- **Network Operations:** Download files from URLs using `NetworkControl`.
- **System Control:** Execute shell commands, manage packages, and handle system-specific tasks with `SystemControl`.
- **File Management:** Read, write, and create files with `HandleFile` and manage JSON files with `HandleJsonFile`.
- **System Services:** Manage systemd services, including enabling and starting services with `SystemService`.
- **Proxy Server:** Configure and run a proxy server optimized for Minecraft with `ProxyServer`.
- **Transit Server:** Extend proxy functionality to manage transit services, whitelist management, and specific Minecraft transit service configurations with `TransitServer`.

## Requirements
- Python 3.6+
- Ubuntu Linux (tested on Ubuntu)

## Installation
1. Ensure Python 3.6 or higher is installed.
2. Clone the repository:
   ```
   git clone https://github.com/GreshAnt/OProxy.git
   ```
3. Navigate to the repository directory:
   ```
   cd repository
   ```
4. Run the setup for the proxy and transit servers:
   ```
   python3 main.py proxy setup
   ```
   ```
   python3 main.py transit setup
   ```

## Usage
### Setting Up Proxy Server
- **Setup:** Initialize and configure the proxy server.
   ```
   python3 main.py proxy setup
   ```

- **Running:** Start running the proxy server.
   ```
   python3 main.py proxy run <transit_server_ip>
   ```

### Setting Up Transit Server
- **Setup:** Initialize and configure the transit server.
   ```
   python3 main.py transit setup
   ```

- **Running:** Start running the transit server.
   ```
   python3 main.py transit run
   ```

- **Adding a Transit Service:** Add a transit service to accelerate Minecraft gameplay.
   ```
   python3 main.py transit target <target_ip> <target_port> <listen_port> <service_name>
   ```

- **Managing Whitelist:** Manage whitelist entries for enhanced gameplay.
   ```
   python3 main.py transit whitelist add <name> <group>
   ```
   ```
   python3 main.py transit whitelist remove <name> <group>
   ```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
