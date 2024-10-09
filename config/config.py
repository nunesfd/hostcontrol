import os
import platform
import getpass
from pathlib import Path

APP_NAME = "HostControl"
APP_VERSION = "0.0.1 (Alpha)"

ENV_HOSTS_PATH = "HOSTCTL_HOSTS_PATH"
ENV_DB_PATH = "HOSTCTL_DB_PATH"
DB_FOLDER = ".host_control"
DB_NAME = "host_control.db"

def get_app_env():
    return os.getenv('APP_ENV', 'production')

def get_user() -> str:
    return getpass.getuser()

def get_hosts_path():
    
    env_hosts_path = os.getenv(ENV_HOSTS_PATH)
    
    if env_hosts_path:
        return env_hosts_path
    
    system = platform.system().lower()
    
    if system == 'windows':
        return r'C:\Windows\System32\drivers\etc\hosts'
    elif system == 'darwin':  # macOS
        return '/etc/hosts'
    elif system == 'linux':
        return '/etc/hosts'
    else:
        raise RuntimeError(f"Operating system not supported: {system}")

def get_db_path_dir() -> Path:
    
    env_db_path = os.getenv(ENV_DB_PATH)
    if env_db_path:
        return Path(env_db_path)

    return Path.home() / DB_FOLDER

def get_db_path_file() -> Path:
    return get_db_path_dir() / DB_NAME
