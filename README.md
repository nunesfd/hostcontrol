![Groups](https://raw.githubusercontent.com/nunesfd/hostcontrol/refs/heads/main/assets/screenshots/list_groups.png)

# HostControl

[![English](https://img.shields.io/badge/lang-en-blue.svg)](./README.md)
[![Português](https://img.shields.io/badge/lang-pt--BR-green.svg)](./README.pt-BR.md)

HostControl is a terminal-based desktop application developed with Python and the [Textual](https://github.com/Textualize/textual) library. This tool is specifically designed to manage the `/etc/hosts` file, providing an intuitive interface that allows users to add, edit, and remove groups of hosts easily and efficiently.

![Hosts](https://raw.githubusercontent.com/nunesfd/hostcontrol/refs/heads/main/assets/screenshots/list_hosts.png)

## Features

- Manage groups of hosts (add, edit, remove)
- View the synchronization status of each group
- User-friendly terminal-based interface
- Keyboard shortcuts for quick actions

## IMPORTANT - Before install

The `/etc/hosts` file can usually only be modified by the superuser (root), so it is necessary to grant access to the app to manage this file.

- **Run as root:** This allows the app to have the necessary permissions to modify the file.
- **Change file permissions:** Modify the permissions of `/etc/hosts` so your user account can read and write to the file.
- **Other alternatives:** You can also use user groups, configure the `sudoers` file, or use **Polkit** to manage permissions more securely.

#### Quick solution for Linux or Mac:
```sh
sudo chown {YOUR_USER}:{YOUR_USER} /etc/hosts
```
> These are simple suggestions that may resolve the issue. However, you can apply a more secure and customized solution that better fits your environment, ensuring the integrity and security of the system.

## Install using Docker

To install and run the application using Docker, you can use the following command:

```bash
docker run --rm --name hostcontrol -it -v /etc/hosts:/opt/hosts -v /home/{your_user}/.host_control:/opt/host_control_db nunesfd/hostcontrol
```

Replace **your_user** with name of **your user**. 
For more details about the parameters used in this command, visit:
<https://hub.docker.com/r/nunesfd/hostcontrol>

## Install using Python (Traditional Method)

### Prerequisites

Before installing HostControl, ensure you have the following installed on your system:

- Python 3.8 or later
- Pip (Python package manager)

### 1. Clone the repository

To install HostControl, first clone the GitHub repository:

```bash
git clone https://github.com/nunesfd/hostcontrol.git
cd hostcontrol
```

### 2. Create and activate a virtual environment (optional but recommended)

Creating a virtual environment will isolate the project's dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Run the application

After installing the dependencies, you can run the app using:

```bash
python main.py
```

## To use in development mode

### Run in development mode
```bash
pip install textual-dev
make start-dev
```

### Run the console for debugging
```bash
make start-console
```

## Contributions

If you want to contribute to the project, feel free to fork the repository and create a pull request. All contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for more details.