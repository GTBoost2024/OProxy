import platform  # Importing platform module to check system information
import subprocess  # Importing subprocess module to execute shell commands
import requests  # Importing requests module to make HTTP requests
import json  # Importing json module for JSON handling
import os  # Importing os module for operating system functionalities
import sys  # Importing sys module for system-specific parameters and functions

_name = "OProxy"  # Defining constant _name as "OProxy"
_version = "1.0.0"  # Defining constant _version as "1.0.0"
_by = "GreshAnt"  # Defining constant _by as "GreshAnt"

class NetworkControl:
    """Class to handle network-related operations like downloading files."""
    
    def download_file(self, url: str, file_name: str):
        """Download a file from a URL and save it locally."""
        print(f"Starting download from {url}...")
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            with open(file_name, 'wb') as file:
                file.write(response.content)
            print(f"{file_name} downloaded successfully")
            return f"{file_name} downloaded successfully"
        except requests.RequestException as e:
            print(f"Failed to download {file_name}: {e}")
            return f"Failed to download {file_name}: {e}"

class SystemControl:
    """Class to handle system-related operations like running commands and managing packages."""
    
    def __init__(self) -> None:
        """Initialize SystemControl object."""
        # Running check
        if os.geteuid() != 0:
            print("This script must be run as root!")
            sys.exit(1)
        else:
            print("Running as root.")
        # Checking if the system is Ubuntu Linux
        if not (('linux' in platform.system().lower()) and ('ubuntu' in platform.version().lower())):
            print("This script is only for Ubuntu Linux")
            exit()
        print("System is Ubuntu Linux")

    def run_command(self, command: str):
        """Run a shell command and capture its output."""
        print(f"Running command: {command}")
        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(f"Command '{command}' executed successfully")
            return result.stdout, result.returncode
        except subprocess.CalledProcessError as e:
            print(f"Command '{command}' failed with return code {e.returncode}: {e.stderr}")
            return e.stderr, e.returncode

    def install_package(self, package_name: str):
        """Install a package using apt."""
        print(f"Installing package: {package_name}")
        stdout, returncode = self.run_command(f"sudo apt install --yes {package_name}")
        return stdout

    def uninstall_package(self, package_name: str):
        """Uninstall a package using apt."""
        print(f"Uninstalling package: {package_name}")
        stdout, returncode = self.run_command(f"sudo apt remove --yes {package_name}")
        return stdout

    def update_package(self):
        """Update packages using apt."""
        print("Updating packages...")
        stdout, returncode = self.run_command("sudo apt update --yes")
        return stdout

    def upgrade_package(self):
        """Upgrade packages using apt."""
        print("Upgrading packages...")
        stdout, returncode = self.run_command("sudo apt upgrade --yes")
        return stdout

class ExecuteFile:
    """Class to handle file execution permissions."""
    
    def __init__(self, file_path) -> None:
        """Initialize ExecuteFile object."""
        self.file_path = file_path
        self.system_control = SystemControl()

    def execute_permission(self):
        """Give execute permissions to a file."""
        print(f'Giving {self.file_path} running permission')
        self.system_control.run_command(f"chmod +x {self.file_path}")
        return 'done'

class HandleFile:
    """Class to handle file operations like reading, writing, and creating files."""
    
    def __init__(self, file_path):
        """Initialize HandleFile object."""
        self.file_path = file_path

    def file_exists(self):
        """Check if a file exists."""
        return os.path.exists(self.file_path)

    def read_file(self):
        """Read content from a file."""
        if not self.file_exists():
            print(f"File {self.file_path} does not exist.")
            return None
        print(f"Reading file: {self.file_path}")
        with open(self.file_path, 'r') as file:
            content = file.read()
        print(f"Read content from {self.file_path}")
        return content

    def write_file(self, content):
        """Write content to a file."""
        print(f"Writing to file: {self.file_path}")
        with open(self.file_path, 'w') as file:
            file.write(content)
        print(f"Wrote content to {self.file_path}")

    def create_file(self, content=""):
        """Create a new file."""
        if self.file_exists():
            print(f"File {self.file_path} already exists.")
            return False
        print(f"Creating file: {self.file_path}")
        with open(self.file_path, 'x') as file:
            file.write(content)
        print(f"Created file {self.file_path}")
        return True

class SystemService:
    """Class to manage system services using systemd."""
    
    def __init__(self, name, description, exec_start, working_directory, syslog_identifier) -> None:
        """Initialize SystemService object."""
        self.system_control = SystemControl()
        self.name = name
        self.service = HandleFile(f"/etc/systemd/system/{name}.service")
        self.service.create_file()  # Create a systemd service file
        self.description = description
        self.exec_start = exec_start
        self.working_directory = working_directory
        self.syslog_identifier = syslog_identifier

    def fill_service_content(self):
        """Fill systemd service file with required content."""
        self.service.write_file(f"""
[Unit]
Description={self.description}
After=network.target

[Service]
ExecStart={self.exec_start}
WorkingDirectory={self.working_directory}
Restart=always
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier={self.syslog_identifier}

[Install]
WantedBy=multi-user.target
""")
        self.system_control.run_command('sudo systemctl daemon-reload')  # Reload systemd daemon
        self.system_control.run_command(f'chmod +x {self.exec_start}')  # Ensure executable permission on the service file

    def enable_service(self):
        """Enable a systemd service."""
        print(f"Enabling {self.service.file_path}")
        self.system_control.run_command(f"sudo systemctl enable {self.service.file_path}")
        return 'done'

    def start_service(self):
        """Start a systemd service."""
        print(f"Starting {self.service.file_path}")
        self.system_control.run_command(f"sudo systemctl start {self.name}")
        return 'done'

class HandleJsonFile(HandleFile):
    """Class to handle JSON file operations, extending HandleFile."""
    
    def read_json(self):
        """Read JSON data from a file."""
        try:
            print(f"Reading JSON file: {self.file_path}")
            return json.loads(self.read_file())
        except json.JSONDecodeError as e:
            print(f"Error reading JSON from {self.file_path}: {e}")
            return None

    def write_json(self, data):
        """Write JSON data to a file."""
        try:
            print(f"Writing JSON to file: {self.file_path}")
            self.write_file(json.dumps(data, indent=4))
            print(f"JSON data written to {self.file_path}")
        except TypeError as e:
            print(f"Error writing JSON to {self.file_path}: {e}")

class ProxyServer:
    """Class to manage operations specific to a proxy server."""
    
    def __init__(self) -> None:
        """Initialize ProxyServer object."""
        self.network_control = NetworkControl()
        self.system_control = SystemControl()

    def download_zbproxy(self):
        """Download ZBProxy software."""
        print("Downloading ZBProxy...")
        return self.network_control.download_file('https://file.uhsea.com/2406/5d3185d966a77f885750bc733c0d533aJ0.', 'zbproxy')

    def init_zbproxy(self):
        """Initialize ZBProxy configuration."""
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
                            "Mode": ""
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
            "Lists": {}
        })
        print("ZBProxy initialized successfully")
        return 'ZBProxy initialized successfully'

    def run_zbproxy(self):
        """Run ZBProxy as a service."""
        print("Running ZBProxy...")
        zbproxy_service = SystemService('ZBProxy', 'ZBProxy service', f'{os.getcwd()}/zbproxy', os.getcwd(), 'zbproxy')
        zbproxy_service.fill_service_content()
        zbproxy_service.enable_service()
        print(zbproxy_service.start_service())
        self.system_control.run_command('sudo ufw allow 25565/tcp')  # Allow traffic on port 25565
        print("ZBProxy running")

class TransitServer(ProxyServer):
    """Class to manage operations specific to a transit server, inheriting from ProxyServer."""
    
    def __init__(self):
        """Initialize TransitServer object."""
        super().__init__()
        self.zbproxy_config = HandleJsonFile('ZBProxy.json')

    def init_zbproxy(self):
        """Initialize ZBProxy configuration specific to transit server."""
        print("Initializing ZBProxy...")
        self.zbproxy_config.write_json({
            "Services": [],
            "Lists": {}
        })
        print("ZBProxy initialized successfully")
        return 'ZBProxy initialized successfully'

    def add_service(self, service_dict: dict):
        """Add a service configuration to ZBProxy."""
        print("Adding service...")
        self.system_control.run_command(f'ufw allow {service_dict["Listen"]}/tcp')  # Allow traffic on specified port
        org_config = self.zbproxy_config.read_json()
        org_config["Services"].append(service_dict)
        service_name = service_dict["Name"]
        if service_name not in org_config["Lists"]:
            org_config["Lists"][service_name] = []
        self.zbproxy_config.write_json(org_config)

    def add_whitelist(self, name: str, group: str):
        """Add an item to a whitelist in ZBProxy configuration."""
        print(f"Adding {name} to the {group}...")
        config = self.zbproxy_config.read_json()
        if config and group in config["Lists"] and name not in config["Lists"][group]:
            config["Lists"][group].append(name)
            self.zbproxy_config.write_json(config)
            print(f"{name} added to {group}")
        else:
            print(f'{name} is already in the {group} or failed to read the config')
        return f"Added {name} to the {group}"

    def remove_whitelist(self, name: str, group: str):
        """Remove an item from a whitelist in ZBProxy configuration."""
        print(f"Removing {name} from the {group}...")
        config = self.zbproxy_config.read_json()
        if config and group in config["Lists"] and name in config["Lists"][group]:
            config["Lists"][group].remove(name)
            self.zbproxy_config.write_json(config)
            print(f"{name} removed from {group}")
        return f"Removed {name} from the {group}"

class MinecraftTransitService:
    """Class to represent a Minecraft transit service configuration."""
    
    def __init__(self, target_ip, target_port, listen_port, service_name) -> None:
        """Initialize MinecraftTransitService object."""
        self.target_ip = target_ip
        self.target_port = target_port
        self.listen_port = listen_port
        self.service_name = service_name
        self.service_dict = {
            "Name": self.service_name,
            "TargetAddress": self.target_ip,
            "TargetPort": int(self.target_port),
            "Listen": int(self.listen_port),
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
                    "Mode": ""
                },
                "NameAccess": {
                    "Mode": "allow",
                    "ListTags": [self.service_name]
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

class Main:
    """Main class to orchestrate setup and execution of proxy and transit servers."""
    
    def __init__(self) -> None:
        """Initialize Main object."""
        self.transit_server = TransitServer()
        self.proxy_server = ProxyServer()

    def setup_proxy_server(self):
        """Set up the proxy server."""
        print("Setting up Proxy Server...")
        print(self.proxy_server.download_zbproxy())
        print(self.proxy_server.init_zbproxy())

    def setup_transit_server(self):
        """Set up the transit server."""
        print("Setting up Transit Server...")
        print(self.transit_server.download_zbproxy())
        print(self.transit_server.init_zbproxy())

    def add_a_transit_service(self, target_ip, target_port, listen_port, service_name):
        """Add a transit service to the transit server."""
        print("Adding a transit service...")
        self.transit_server.add_service(MinecraftTransitService(target_ip, target_port, listen_port, service_name).service_dict)

    def add_to_whitelist(self, name: str, group: str):
        """Add an item to a whitelist in the transit server."""
        print(f"Adding {name} to the {group}...")
        print(self.transit_server.add_whitelist(name, group))

    def remove_from_whitelist(self, name: str, group: str):
        """Remove an item from a whitelist in the transit server."""
        print(f"Removing {name} from the {group}...")
        print(self.transit_server.remove_whitelist(name, group))

    def run_proxy_server(self):
        """Run the proxy server."""
        print("Running Proxy Server...")
        self.proxy_server.run_zbproxy()

    def run_transit_server(self):
        """Run the transit server."""
        print("Running Transit Server...")
        self.transit_server.run_zbproxy()

    def run(self, args):
        """Main entry point to run the script."""
        if len(args) < 2:
            print("Insufficient arguments provided.")
            return

        command = args[1]
        match command:
            case "transit":
                match args[2]:
                    case "setup":
                        self.setup_transit_server()
                    case "run":
                        self.run_transit_server()
                    case "target":
                        self.add_a_transit_service(args[3], args[4], args[5], args[6])
                    case "whitelist":
                        match args[3]:
                            case "add":
                                self.add_to_whitelist(args[4], args[5])
                            case "remove":
                                self.remove_from_whitelist(args[4], args[5])
            case "proxy":
                match args[2]:
                    case "setup":
                        self.setup_proxy_server()
                    case "run":
                        self.run_proxy_server()

if __name__ == "__main__":
    main = Main()
    main.run(sys.argv)
