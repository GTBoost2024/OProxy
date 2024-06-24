import platform
import subprocess
import requests
import json
import os
import sys


class NetworkControl:
    def download_file(self, url: str, file_name: str):
        print(f"Starting download from {url}...")
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(file_name, 'wb') as file:
                file.write(response.content)
            print(f"{file_name} downloaded successfully")
            return f"{file_name} downloaded successfully"
        except requests.RequestException as e:
            print(f"Failed to download {file_name}: {e}")
            return f"Failed to download {file_name}: {e}"


class SystemControl:
    def __init__(self) -> None:
        # Running check
        
        if os.geteuid() != 0:
            print("This script must be run as root!")
            sys.exit(1)
        else:
            print("Running as root.")
        if not (('linux' in platform.system().lower()) and ('ubuntu' in platform.version().lower())):
            print("This script is only for Ubuntu Linux")
            exit()
        print("System is Ubuntu Linux")

    def run_command(self, command: str):
        print(f"Running command: {command}")
        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(f"Command '{command}' executed successfully")
            return result.stdout, result.returncode
        except subprocess.CalledProcessError as e:
            print(f"Command '{command}' failed with return code {e.returncode}: {e.stderr}")
            return e.stderr, e.returncode

    def install_package(self, package_name: str):
        print(f"Installing package: {package_name}")
        stdout, returncode = self.run_command(f"sudo apt install --yes {package_name}")
        return stdout

    def uninstall_package(self, package_name: str):
        print(f"Uninstalling package: {package_name}")
        stdout, returncode = self.run_command(f"sudo apt remove --yes {package_name}")
        return stdout

    def update_package(self):
        print("Updating packages...")
        stdout, returncode = self.run_command("sudo apt update --yes")
        return stdout

    def upgrade_package(self):
        print("Upgrading packages...")
        stdout, returncode = self.run_command("sudo apt upgrade --yes")
        return stdout


class HandleFile:
    def __init__(self, file_path):
        self.file_path = file_path

    def file_exists(self):
        return os.path.exists(self.file_path)

    def read_file(self):
        if not self.file_exists():
            print(f"File {self.file_path} does not exist.")
            return None
        print(f"Reading file: {self.file_path}")
        with open(self.file_path, 'r') as file:
            content = file.read()
        print(f"Read content from {self.file_path}")
        return content

    def write_file(self, content):
        print(f"Writing to file: {self.file_path}")
        with open(self.file_path, 'w') as file:
            file.write(content)
        print(f"Wrote content to {self.file_path}")

    def create_file(self, content=""):
        if self.file_exists():
            print(f"File {self.file_path} already exists.")
            return False
        print(f"Creating file: {self.file_path}")
        with open(self.file_path, 'x') as file:
            file.write(content)
        print(f"Created file {self.file_path}")
        return True


class HandleJsonFile(HandleFile):
    def read_json(self):
        try:
            print(f"Reading JSON file: {self.file_path}")
            return json.loads(self.read_file())
        except json.JSONDecodeError as e:
            print(f"Error reading JSON from {self.file_path}: {e}")
            return None

    def write_json(self, data):
        try:
            print(f"Writing JSON to file: {self.file_path}")
            self.write_file(json.dumps(data, indent=4))
            print(f"JSON data written to {self.file_path}")
        except TypeError as e:
            print(f"Error writing JSON to {self.file_path}: {e}")


class TransitServer:
    def __init__(self) -> None:
        self.system_control = SystemControl()
        os.makedirs('/etc/nginx/stream.d', exist_ok=True)
        self.stream_config = HandleFile('/etc/nginx/stream.d/stream.conf')

    def install_all_packages(self):
        print("Installing all necessary packages...")
        packages = [
            'wget', 'build-essential', 'libpcre3', 'libpcre3-dev', 'libssl-dev',
            'zlib1g', 'zlib1g-dev', 'tar', 'make'
        ]
        for package in packages:
            self.system_control.install_package(package)

        self.system_control.run_command('wget https://launchpad.net/ubuntu/+archive/primary/+sourcefiles/nginx/1.18.0-6ubuntu14/nginx_1.18.0.orig.tar.gz')
        self.system_control.run_command('sudo tar -zxvf nginx_1.18.0.orig.tar.gz')
        os.chdir('nginx-1.18.0')
        self.system_control.run_command('./configure --prefix="/usr/local/nginx" --with-stream')
        self.system_control.run_command('make')
        self.system_control.run_command('sudo make install')

        self.nginx_config = HandleFile('/lib/systemd/system/nginx.service')
        if not self.nginx_config.file_exists():
            print("Creating NGINX service file...")
            self.nginx_config.create_file()
        self.nginx_config.write_file(
            """
[Unit]
Description=The NGINX HTTP and reverse proxy server
After=network.target

[Service]
Type=forking
ExecStart=/usr/local/nginx/sbin/nginx
ExecReload=/usr/local/nginx/sbin/nginx -s reload
ExecStop=/usr/local/nginx/sbin/nginx -s quit
PIDFile=/usr/local/nginx/logs/nginx.pid
PrivateTmp=true

[Install]
WantedBy=multi-user.target
"""
        )
        self.system_control.run_command('sudo systemctl enable nginx')
        self.system_control.run_command('sudo systemctl start nginx')
        self.system_control.update_package()
        return 'done'

    def configure_nginx(self, server_ip: str, server_port: str):
        if not self.stream_config.file_exists():
            print("Creating stream configuration file...")
            self.stream_config.create_file()
        self.stream_config.write_file(
            f"""
stream {{
    server {{
        listen 25565;
        proxy_pass {server_ip}:{server_port};
        proxy_connect_timeout 1s;
    }}
}}
"""
        )
        print("NGINX configuration updated")
        return 'done'

    def reload_nginx(self):
        print("Restarting NGINX...")
        stdout, returncode = self.system_control.run_command('sudo systemctl reload nginx')
        if returncode == 0:
            print('Reload nginx successfully')
            return 'Reload nginx successfully'
        else:
            print(f'Failed to reload nginx: {stdout}')
            return f'Failed to reload nginx: {stdout}'


class ProxyServer:
    def __init__(self) -> None:
        self.network_control = NetworkControl()
        self.system_control = SystemControl()

    def download_zbproxy(self):
        print("Downloading ZBProxy...")
        return self.network_control.download_file('https://file.uhsea.com/2406/5d3185d966a77f885750bc733c0d533aJ0.', 'zbproxy')

    def init_zbproxy(self):
        print("Initializing ZBProxy...")
        self.system_control.run_command("chmod +x zbproxy")
        self.zbproxy_config = HandleJsonFile('ZBProxy.json')
        self.zbproxy_config.write_json({
            "Services": [
                {
                    "Name": "HypixelSpeedProxy",
                    "TargetAddress": "mc.hypixel.net",
                    "TargetPort": 25565,
                    "Listen": 25565,
                    "Flow": "auto",
                    "IPAccess": {
                        "Mode": ""
                    },
                    "Minecraft": {
                        "EnableHostnameRewrite": True,
                        "OnlineCount": {
                            "Max": 114514,
                            "Online": -1,
                            "EnableMaxLimit": False
                        },
                        "HostnameAccess": {
                            "Mode": "allow",
                            "ListTags": ["whitelist"]
                        },
                        "NameAccess": {
                            "Mode": ""
                        },
                        "PingMode": "",
                        "MotdFavicon": "{DEFAULT_MOTD}",
                        "MotdDescription": "§d{NAME}§e service is working on §a§o{INFO}§r\n§c§lProxy for §6§n{HOST}:{PORT}§r"
                    },
                    "TLSSniffing": {
                        "RejectNonTLS": False
                    },
                    "Outbound": {
                        "Type": ""
                    }
                }
            ],
            "Lists": {
                "whitelist": ["Noliun"]
            }
        })
        print("ZBProxy initialized successfully")
        return 'ZBProxy initialized successfully'

    def add_whitelist(self, name: str):
        print(f"Adding {name} to whitelist...")
        config = self.zbproxy_config.read_json()
        if config and name not in config["Lists"]["whitelist"]:
            config["Lists"]["whitelist"].append(name)
            self.zbproxy_config.write_json(config)
            print(f"{name} added to whitelist")
        else:
            print(f"{name} is already in the whitelist or failed to read the config")
        return f"Added {name} to whitelist"


class Main:
    def __init__(self):
        self.transit_server = TransitServer()
        self.proxy_server = ProxyServer()

    def setup_transit_server(self, server_ip: str, server_port: str):
        print("Setting up Transit Server...")
        print(self.transit_server.install_all_packages())
        print(self.transit_server.configure_nginx(server_ip, server_port))
        print(self.transit_server.reload_nginx())

    def setup_proxy_server(self):
        print("Setting up Proxy Server...")
        print(self.proxy_server.download_zbproxy())
        print(self.proxy_server.init_zbproxy())

    def add_to_whitelist(self, name: str):
        print(f"Adding {name} to the whitelist...")
        print(self.proxy_server.add_whitelist(name))

    def run(self, args):
        if len(args) < 2:
            print("Insufficient arguments provided.")
            return

        command = args[1]
        if command == "transit" and len(args) == 4:
            server_ip = args[2]
            server_port = args[3]
            self.setup_transit_server(server_ip, server_port)
        elif command == "proxy":
            self.setup_proxy_server()
        else:
            name = command
            self.add_to_whitelist(name)


if __name__ == "__main__":
    main = Main()
    main.run(sys.argv)
