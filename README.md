# SolarWinds Snap Agent Ansible Role


Installs and configures SolarWinds Snap Agent on RHEL/CentOS, Debian/Ubuntu or Windows servers.

## Role Variables

Ansible role variables with default values are listed below:

```yaml
appoptics_token: ""
```
AppOptics API [token](https://docs.appoptics.com/kb/user_org/tokens/#api-tokens-and-token-roles).

```yaml
log_level: 3
log_path: /var/log/SolarWinds/Snap
```
Logging level and path to file.

```yaml
listen_addr: 127.0.0.1
listen_port: 21414
```
Address and port of running instance of SolarWinds Snap Agent.

```yaml
temp_dir_path: /tmp/SolarWinds/Snap
temp_dir_enable: false
```

```yaml
plugin_path: /opt/SolarWinds/Snap/bin
```
Path where SolarWinds Snap Agent's plugins binaries are stored.

```yaml
task_path: /opt/SolarWinds/Snap/etc/tasks.d
```
Path to SolarWinds Snap Agent's tasks files.

```yaml
http_proxy: false
http_proxy_url: ""
authenticate_http_proxy: false
http_proxy_user: ""
http_proxy_password: ""

socks_proxy: false
socks_proxy_url: ""
authenticate_socks_proxy: false
socks_proxy_user: ""
socks_proxy_password: ""
```
Optional http and socks proxies settings.

```yaml
publisher_grpc_timeout: 10
aosystem_grpc_timeout: 10
```
AppOptics Publisher and aosystem plugins GRPC settings.

OS-specific variables are stored in `vars/`. They're included in main task and, other than `installer_download_path`, shouldn't be overriden.

## Example Playbook

To use SolarWinds Snap Agent Ansible Role clone this repository to directory with your playbook's roles. Usage together with `ansible-swisnap-modules`: [example](https://github.com/librato/ansible-swisnap-modules/blob/master/tests/main.yml)

### Linux

```yaml
  hosts: localhost
  connection: local
  vars_files:
    - vars/my_vars.yaml
  roles:
    - ansible-swisnap
```

Inside `vars/my_vars.yaml`:

```yaml
appoptics_token: 123456789dbba089e9ff613bb9528320188853b1a08d91d23d2fc9bc1c41ec3e
log_level: 2
listen_port: 55555
```

### Windows:

```yaml
---
- hosts: windows
  vars_files:
    - vars/main.yml
  roles:
    - ansible-swisnap
```

Inside `vars/my_vars.yaml`:

```yaml
appoptics_token: 123456789dbba089e9ff613bb9528320188853b1a08d91d23d2fc9bc1c41ec3e
installer_download_path: "C:\\Users\\Administrator\\Downloads\\solarwinds-snap-agent-installer.msi"
```

Inside `inventory`:

```c
[windows]
1.2.3.4
```

Inside `group_vars/windows`:

```yaml
ansible_user: Administrator
ansible_password: password
ansible_port: 5986
ansible_connection: winrm
ansible_winrm_server_cert_validation: ignore
```
