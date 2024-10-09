import os
from config import config
from models.group import GroupHostsStatus

def ensure_directory_for_database():
    dir = config.get_db_path_dir()
    if not dir.exists():
        dir.mkdir(parents=True)

def get_icon_by_group_status(status: GroupHostsStatus) -> str:
    icon = "🟢"
    if status == "not_applied":
        icon = "🟡"
    elif status == "inactive":
        icon = "🔴"
    return icon

def format_group_name(name: str, status: GroupHostsStatus) -> str:
    icon = get_icon_by_group_status(status)
    return f"{icon} #{name.upper()}"

def check_permissions_hosts():
    file_path = config.get_hosts_path()
    if not os.path.exists(file_path):
        return MESSAGE_HOSTS_NOT_FOUND, False
    
    can_read = os.access(file_path, os.R_OK)
    can_write = os.access(file_path, os.W_OK)

    if can_read and can_write:
        return "", True
    
    return MESSAGE_HOSTS_NOT_ACCESS, False

MY_USER = config.get_user()

MESSAGE_HOSTS_NOT_FOUND = f"""\
# 🚫 File Not Found
The file `{config.get_hosts_path()}` could not be located.
Please verify that the file exists and the path is correct.
"""

MESSAGE_HOSTS_NOT_ACCESS = f"""\
# Permission Issue: `{config.get_hosts_path()}`

The software doesn't have permission to access the file `{config.get_hosts_path()}`. To fix this, try one of the following:

- **Run as root:** This gives the program the necessary permissions to modify the file.
- **Change file permissions:** Adjust the permissions of `{config.get_hosts_path()}` to allow your user account to read and write.
- **Other methods:** You can also use solutions like user groups, `sudoers`, or **Polkit** for more secure permission handling.

# Quick fix for Linux or Mac:
```sh
sudo chown {MY_USER}:{MY_USER} /etc/hosts
```

> These are simple suggestions that may solve the problem. However, feel free to apply a more secure solution tailored to your environment, ensuring system integrity and protection.
"""