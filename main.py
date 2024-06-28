import platform  # Importing platform module to check system information
import subprocess  # Importing subprocess module to execute shell commands
import requests  # Importing requests module to make HTTP requests
import json  # Importing json module for JSON handling
import os  # Importing os module for operating system functionalities
import sys  # Importing sys module for system-specific parameters and functions

_name = "OProxy"
_version = "1.1.4"
_by = "GreshAnt" 

        
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
    
    def __init__(self, gh_token) -> None:
        """Initialize ProxyServer object."""
        self.network_control = NetworkControl()
        self.system_control = SystemControl()
        self.program_control = ProgramControl(gh_token)
        self.zbproxy_config = HandleJsonFile('ZBProxy.json')
        self.zbproxy_config.create_file()
        self.system_control.install_package('ufw')
        

    def download_zbproxy(self, token):
        """Download ZBProxy software."""
        print("Downloading ZBProxy...")
        return self.network_control.download_file(self.program_control.get_latest_artifact_download_url(token), "zbproxy")

    def init_zbproxy(self, target_ip: str, target_port: str, listen_on: str):
        """Initialize ZBProxy configuration."""
        print("Initializing ZBProxy...")
        self.system_control.run_command("chmod +x zbproxy")
        self.zbproxy_config.write_json({
            "Services": [
                {
                    "Name": "MinecraftProxy",
                    "TargetAddress": target_ip,
                    "TargetPort": int(target_port),
                    "Listen": int(listen_on),
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
                            "ListTags" : ["TransitServerIP"]
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
                "TransitServerIP" : []
            }
        })
        print("ZBProxy initialized successfully")
        return 'ZBProxy initialized successfully'

    def run_zbproxy(self):
        """Run ZBProxy as a service."""
        print("Running ZBProxy...")
        zbproxy_service = SystemService('ZBProxy', 'ZBProxy service', f'{os.getcwd()}/zbproxy', os.getcwd(), 'zbproxy')
        zbproxy_service.fill_service_content()
        zbproxy_service.enable_service()
        self.system_control.run_command('sudo chmod +x {os.getcwd()}/zbproxy')
        print(zbproxy_service.start_service())
        self.system_control.run_command('sudo ufw allow 25565/tcp')  # Allow traffic on port 25565
        print("ZBProxy running")

    def add_transit_server_ip(self, ip: str):
        config = self.zbproxy_config.read_json()
        if ip not in config['Lists']['TransitServerIP']:
            config['Lists']['TransitServerIP'].append(ip)
            self.zbproxy_config.write_json(config)
            print(f"Added {ip} to TransitServerIP list")
            return 'done'
        else:
            print('IP already exists in TransitServerIP list')
            return 'IP already exists'
    
    def remove_transit_server_ip(self, ip: str):
        config = self.zbproxy_config.read_json()
        if ip in config['Lists']['TransitServerIP']:
            config['Lists']['TransitServerIP'].remove(ip)
            self.zbproxy_config.write_json(config)
            print(f"Removed {ip} from TransitServerIP list")
            return 'done'
        else:
            print(f"{ip} not found in TransitServerIP list")
            return 'Not found'
        
    def turn_on_hostname_access(self):
        print("Turning on hostname access...")
        config = self.zbproxy_config.read_json()
        config['Services'][0]['Minecraft']['HostnameAccess']['Mode'] = 'allow'
        self.zbproxy_config.write_json(config)
    
    def turn_off_hostname_access(self):
        print("Turning off hostname access...")
        config = self.zbproxy_config.read_json()
        config['Services'][0]['Minecraft']['HostnameAccess']['Mode'] = ''
        self.zbproxy_config.write_json(config)



class TransitServer(ProxyServer):
    """Class to manage operations specific to a transit server, inheriting from ProxyServer."""
    
    def __init__(self, gh_token):
        """Initialize TransitServer object."""
        super().__init__(gh_token)
        self.network_control = NetworkControl()
        self.system_control = SystemControl()
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
    
    def remove_service(self, service_name: str):
        """Remove a service configuration from ZBProxy."""
        print(f"Removing service {service_name}...")
        org_config = self.zbproxy_config.read_json()
        for service in org_config["Services"]:
            if service["Name"] == service_name:
                org_config["Services"].remove(service)
                self.zbproxy_config.write_json(org_config)
                print(f"Service {service_name} removed")
                return f"Service {service_name} removed"
        

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


    def turn_on_whitelist(self, service_name):
        config = self.zbproxy_config.read_json()
        for service in config["Services"]:
            if service["Name"] == service_name:
                service["Minecraft"]["HostnameAccess"]["Mode"] = "allow"
                self.zbproxy_config.write_json(config)
                print(f"Whitelist turned on for {service_name}")
                return f"Whitelist turned on for {service_name}"

    def turn_off_whitelist(self, service_name):
        config = self.zbproxy_config.read_json()
        for service in config["Services"]:
            if service["Name"] == service_name:
                service["Minecraft"]["HostnameAccess"]["Mode"] = ""
                self.zbproxy_config.write_json(config)
                print(f"Whitelist turned off for {service_name}")
                return f"Whitelist turned off for {service_name}"



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
                "EnableHostnameRewrite": False,
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
                "MotdDescription": "§d{NAME}§e service is working on §a§o{INFO}§r\n§c§lProxy for §6§nmc.hypixel.net:25565§r"
            },
            "TLSSniffing": {
                "RejectNonTLS": False
            },
            "Outbound": {
                "Type": ""
            }
        }


class ProgramControl:
    
    def __init__(self, token) -> None:
        self.system_control = SystemControl()
        self.network_control = NetworkControl()
        
        self.token = token
        self.cpu_model = platform.processor()
    

    def get_latest_artifact_download_url(self, token):
        GITHUB_TOKEN = token
        REPO_OWNER = 'layou233'
        REPO_NAME = 'ZBProxy'
        
        # 设置请求头
        headers = {
            'Authorization': f'token {GITHUB_TOKEN}',
            'Accept': 'application/vnd.github+json'
        }

        # 获取最新的workflow run
        workflow_runs_url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs'
        response = requests.get(workflow_runs_url, headers=headers)
        response.raise_for_status()  # 确保请求成功
        workflow_runs = response.json()

        if 'workflow_runs' in workflow_runs and workflow_runs['workflow_runs']:
            latest_run = workflow_runs['workflow_runs'][0]
            run_id = latest_run['id']

            # 获取该workflow run的artifacts
            artifacts_url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs/{run_id}/artifacts'
            response = requests.get(artifacts_url, headers=headers)
            response.raise_for_status()  # 确保请求成功
            artifacts = response.json()

            if 'artifacts' in artifacts and artifacts['artifacts']:
                for artifact in artifacts['artifacts']:
                    if artifact['name'] == ('ZBProxy-linux-amd64-v3' if ('v3' in self.cpu_model) else 'ZBProxy-linux-amd64-v1'):
                        artifact_id = artifact['id']
                        break
                else:
                    print('没有找到指定名称的artifact，则返回None')
                    return None  # 如果没有找到指定名称的artifact，则返回None

                # 获取artifact下载URL
                download_url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/artifacts/{artifact_id}/zip'
                response = requests.get(download_url, headers=headers, allow_redirects=False)
                response.raise_for_status()  # 确保请求成功

                if response.status_code == 302:  # 重定向
                    download_redirect_url = response.headers['Location']
                    return download_redirect_url
                else:
                    print('下载链接获取失败，则返回None')
                    return None  # 如果下载链接获取失败，则返回None
            else:
                print('没有找到artifacts，则返回None')
                return None  # 如果没有找到artifacts，则返回None
        else:
            print('没有找到workflow runs，则返回None')
            return None  # 如果没有找到workflow runs，则返回None

    def unzip_zbproxy(self):
        self.system_control.install_package('unzip')
        self.system_control.run_command('unzip zbproxy.zip')
        self.system_control.run_command('rm -rf zbproxy.zip')

    def update_zbproxy(self):
        print("Updating ZBProxy...")
        try:
            download_url = self.get_latest_artifact_download_url(self.token)
            if download_url:
                self.system_control.run_command('rm -rf zbproxy')
                self.network_control.download_file(download_url, 'zbproxy.zip')
                self.unzip_zbproxy()
                self.system_control.run_command(f"mv {('ZBProxy-linux-amd64-v3' if ('v3' in self.cpu_model) else 'ZBProxy-linux-amd64-v1')} zbproxy")
                self.system_control.run_command('sudo chmod +x zbproxy')
                self.system_control.run_command('sudo systemctl restart ZBProxy')
                print("ZBProxy updated successfully.")
                return "ZBProxy updated successfully."
            else:
                print("Failed to get the download URL.")
                return "Failed to get the download URL."
        except Exception as e:
            print(f"Failed to update ZBProxy: {str(e)}")
            return f"Failed to update ZBProxy: {str(e)}"

    @staticmethod
    def get_latest_release_download_url(repo_owner, repo_name, asset_name):
        # 获取最新的release
        releases_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest'
        response = requests.get(releases_url)
        response.raise_for_status()  # 确保请求成功
        release = response.json()

        # 检查release中的assets
        if 'assets' in release and release['assets']:
            for asset in release['assets']:
                if asset['name'] == asset_name:
                    download_url = asset['browser_download_url']
                    return download_url
            return "No matching asset found in the latest release."
        else:
            return "No assets found in the latest release."
    
    def upgrade_program(self):
        print("Updating program...")
        try:
            # 备份旧版本
            self.system_control.run_command('sudo mv OProxy OProxy.old')
            
            # 下载新版本
            download_url = self.get_latest_release_download_url('GTBoost2024', 'OProxy', 'OProxy')
            if download_url:
                self.network_control.download_file(download_url, 'OProxy')
                self.system_control.run_command('sudo rm -rf OProxy.old')
                self.system_control.run_command('sudo chmod +x OProxy')
                print("Program updated successfully.")
                return "Program updated successfully."
            else:
                print("Failed to get the download URL.")
                return "Failed to get the download URL."
        except Exception as e:
            print(f"Failed to upgrade program: {str(e)}")
            return f"Failed to upgrade program: {str(e)}"




class Main:
    """Main class to orchestrate setup and execution of proxy and transit servers."""
    
    def __init__(self) -> None:
        """Initialize Main object."""
        self.config = HandleJsonFile("config.json")
        if self.config.create_file():
            self.config.write_json({"token": "your_token"})
            print('config.json created, please edit it and restart the program.')
            sys.exit()
        else:
            print("config.json exists, continue...")
            self.token = self.config.read_json()["token"]
            self.program_control = ProgramControl(self.token)
            self.proxy_server = ProxyServer(self.token)
            self.transit_server = TransitServer(self.token)

    def update_zbproxy(self):
        """Update ZBProxy."""
        print("Updating ZBProxy...")
        print(self.program_control.update_zbproxy())
        print("ZBProxy updated successfully.")
        return "ZBProxy updated successfully."

    def upgrade_program(self):
        """Upgrade the program."""
        print("Upgrading program...")
        print(self.program_control.upgrade_program())
        print("Program upgraded successfully.")

    def setup_proxy_server(self, target_ip, target_port, listen_port):
        """Set up the proxy server."""
        print("Setting up Proxy Server...")
        print(self.proxy_server.download_zbproxy(self.token))
        print(self.proxy_server.init_zbproxy(target_ip, target_port, listen_port))

    def setup_transit_server(self):
        """Set up the transit server."""
        print("Setting up Transit Server...")
        print(self.transit_server.download_zbproxy(self.token))
        print(self.transit_server.init_zbproxy())


    def turn_on_hostname_access(self):
        print("Turning on hostname access...")
        print(self.transit_server.turn_on_hostname_access())
    
    def turn_off_hostname_access(self):
        print("Turning off hostname access...")
        print(self.transit_server.turn_off_hostname_access())

    def add_a_transit_server_for_proxy(self, transit_server_hostname: str):
        """Add a transit server for the proxy server."""
        print("Adding a transit server...")
        print(self.proxy_server.add_transit_server_ip(transit_server_hostname))
    
    def remove_a_transit_server_for_proxy(self, transit_server_hostname: str):
        """Remove a transit server for the proxy server."""
        print("Removing a transit server...")
        print(self.proxy_server.remove_transit_server_ip(transit_server_hostname))


    def add_a_transit_service(self, target_ip, target_port, listen_port, service_name):
        """Add a transit service to the transit server."""
        print("Adding a transit service...")
        self.transit_server.add_service(MinecraftTransitService(target_ip, target_port, listen_port, service_name).service_dict)

    def remove_a_transit_service(self, service_name):
        """Remove a transit service from the transit server."""
        print("Removing a transit service...")
        self.transit_server.remove_service(service_name)


    
    # whitelist managing functions

    def add_to_whitelist(self, name: str, group: str):
        """Add an item to a whitelist in the transit server."""
        print(f"Adding {name} to the {group}...")
        print(self.transit_server.add_whitelist(name, group))

    def remove_from_whitelist(self, name: str, group: str):
        """Remove an item from a whitelist in the transit server."""
        print(f"Removing {name} from the {group}...")
        print(self.transit_server.remove_whitelist(name, group))

    def turn_on_whitelist(self, group: str):
        """Turn on the whitelist in the transit server."""
        print(f'Turning on whitelist for {group}...')
        print(self.transit_server.turn_on_whitelist(group))

    def turn_off_whitelist(self, group: str):
        """Turn off the whitelist in the transit server."""
        print(f'Turning off whitelist for {group}...')
        print(self.transit_server.turn_off_whitelist(group))

    # Running functions

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
                        match args[3]:
                            case "add":
                                self.add_a_transit_service(args[4], args[5], args[6], args[7])
                            case "remove":
                                self.remove_a_transit_service(args[4])
                    case "whitelist":
                        match args[3]:
                            case "add":
                                self.add_to_whitelist(args[4], args[5])
                            case "remove":
                                self.remove_from_whitelist(args[4], args[5])
                            case "on":
                                self.turn_on_whitelist(args[4])
                            case "off":
                                self.turn_off_whitelist(args[4])
                            case other:
                                print(f'error input : {other}')
                    case other:
                        print(f'error input {other}')

            case "proxy":
                match args[2]:
                    case "setup":
                        self.setup_proxy_server(args[3], args[4], args[5])
                    case "run":
                        self.run_proxy_server()
                    case "transit":
                        match args[3]:
                            case "add":
                                self.add_a_transit_server_for_proxy(args[4])
                            case "remove":
                                self.remove_a_transit_server_for_proxy(args[4])
                            case other:
                                print(f'error input {other}')
                    case "hostname":
                        match args[3]:
                            case "on":
                                self.turn_on_hostname_access()
                            case "off":
                                self.turn_off_hostname_access()
                            case other:
                                print(f'error input {other}')
                    case other:
                        print(f'error input {other}')

            case "update":
                match args[2]:
                    case "zbproxy":
                        self.update_zbproxy()
                    case "program":
                        self.upgrade_program()
                    case other:
                        print(f'error input {other}')
            case other:
                print(f'error input {other}')    


if __name__ == "__main__":
    main = Main()
    main.run(sys.argv)
