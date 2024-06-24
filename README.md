# Proxy and Transit Server Setup Script

This repository contains a Python script designed to automate the setup of a transit server using NGINX with the stream module and a proxy server using ZBProxy. The script ensures all necessary packages are installed, downloads and configures the software, and sets up the servers with minimal user intervention.

## Features

- Automatic installation and configuration of NGINX with stream module
- Automatic setup of a transit server to redirect traffic
- Automatic download and configuration of ZBProxy
- Simple command-line interface for setup and configuration

## Requirements

- Ubuntu 22.04
- Python 3.x

## Getting Started

### Prerequisites

Before running the script, make sure you have the following installed:

- `python3`
- `pip3`
- Root privileges (the script must be run as root)

### Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/yourusername/proxy-transit-server.git
    cd proxy-transit-server
    ```

### Usage

The script provides three main functionalities: setting up the transit server, setting up the proxy server, and adding a user to the whitelist. Below are the commands to execute these tasks.

#### Setting up the Transit Server

To set up the transit server, run the following command with the desired server IP and port:

```bash
sudo python3 main.py transit <server_ip> <server_port>
```

#### Setting up the Proxy Server

To set up the proxy server, simply run:

```bash
sudo python3 main.py proxy
```

#### Adding a User to the Whitelist

To add a user to the ZBProxy whitelist, run:

```bash
sudo python3 main.py <username>
```

### Example

1. Setting up the transit server with IP `192.168.1.1` and port `25565`:

    ```bash
    sudo python3 main.py transit 192.168.1.1 25565
    ```

2. Setting up the proxy server:

    ```bash
    sudo python3 main.py proxy
    ```

3. Adding a user named `exampleuser` to the whitelist:

    ```bash
    sudo python3 main.py exampleuser
    ```

## File Structure

```
proxy-transit-server/
│
├── main.py               # Main script
├── README.md             # This readme file
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [NGINX](https://nginx.org/)
- [ZBProxy](https://github.com/layou233/ZBProxy)

## Contact

For any questions or suggestions, feel free to reach out at [your email](mailto:ccvvxuruoteng@gmail.com).
