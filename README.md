# Minecraft Acceleration with OProxy

**Version:** 1.1.1                    
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
- Ubuntu Linux (tested on Ubuntu)
- Root access

## Installation
1. Ensure your system is Ubuntu Linux

2. Download the file in releases.

3. Give the file execution permission: 
   
   ```
   chmod +x OProxy
   ```


## Usage
### Setting Up Proxy Server
- **Setup:** Initialize and configure the proxy server.
   ```
   sudo ./OProxy proxy setup <transit_server_ip> <target_server_ip> <target_server_port> <listen_port> <service_name>
   ```

- **Running:** Start running the proxy server.
   ```
   sudo ./OProxy proxy run
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
   sudo ./OProxy transit target <target_ip> <target_port> <listen_port> <service_name>
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
