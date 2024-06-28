# Minecraft Acceleration with OProxy

**Version:** 1.1.3      
**Author:** GreshAnt

## Overview
OProxy is a Python utility designed to accelerate Minecraft gameplay by managing proxy and transit server configurations on Ubuntu Linux. It simplifies the process of downloading, executing system commands, managing packages, handling JSON configurations, and setting up systemd services.

## Features
- **Network Operations:** Download files from URLs.
- **System Control:** Execute shell commands, manage packages, and handle system-specific tasks.
- **File Management:** Read, write, and create files, including JSON configuration files.
- **System Services:** Manage systemd services, including enabling and starting services.
- **Proxy Server:** Configure and run a proxy server optimized for Minecraft.
- **Transit Server:** Manage transit services, including whitelist management and Minecraft-specific configurations.

## Requirements
- Ubuntu Linux
- Root access
- Python 3.x

## Installation
1. Ensure your system is Ubuntu Linux.
2. Download the latest release of OProxy.
3. Give the file execution permission:
   
   ```
   chmod +x OProxy
   ```


## Usage
### Setting Up Proxy Server
- **Setup:** Initialize and configure the proxy server.
   ```
   sudo ./OProxy proxy setup <target_server_ip> <target_server_port> <listen_port>
   ```

- **Running:** Start running the proxy server.
   ```
   sudo ./OProxy proxy run
   ```
- **Adding a transit server:** Add a transit server to accelerate Minecraft gameplay.
   In order to add a transit server, you need to run the following command:
   ```
   sudo ./OProxy proxy transit add <transit_server>
   ```
- **Removing a transit server:** Remove a transit server from the list.
   ```
   sudo ./OProxy proxy transit remove <transit_server>
   ```


### Setting Up Transit Server
- **Setup:** Initialize and configure the transit server.
   ```
   sudo ./OProxy transit setup
   ```

- **Running:** Start running the transit server.
   ```
   sudo ./OProxy transit run
   ```

- **Adding a Transit Service:** Add a transit service to accelerate Minecraft gameplay.
   ```
   sudo ./OProxy transit target add <target_ip> <target_port> <listen_port> <service_name>
   ```

- **Removing a Transit Service:** Remove a transit service from the list.
   ```
   sudo ./OProxy transit target remove <service_name>
   ```

- **Managing Whitelist:** Manage whitelist entries for enhanced gameplay.
   ```
   sudo ./OProxy transit whitelist add <name> <group>
   ```
   ```
   sudo ./OProxy transit whitelist remove <name> <group>
   ```
   ```
   sudo ./OProxy transit whitelist on
   ```
   ```
   sudo ./OProxy transit whitelist off
   ```


## Updating

### Updating OProxy
   - **Updating in the Terminal**
   ```
   sudo ./OProxy update program
   ```

### Updating Proxy Server
  - **Updating in the Terminal**
  ```
  sudo ./OProxy update zbproxy
  ```

## License
This project is licensed under the MIT License - see the [LICENCE](LICENCE) file for details.
