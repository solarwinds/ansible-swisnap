# SolarWinds Snap Agent Ansible Role

[![CircleCI](https://circleci.com/gh/solarwinds/ansible-swisnap.svg?style=shield)](https://circleci.com/gh/solarwinds/ansible-swisnap)

Installs and configures SolarWinds Snap Agent on RHEL/CentOS, Debian/Ubuntu or Windows servers.

For more detailed information about SolarWinds Snap Agent please refer to [documentation](https://docs.appoptics.com/kb/host_infrastructure/host_agent/)

## Role Variables

Ansible role variables with default values are listed below:

```yaml
solarwinds_token: ""
```
AppOptics API [token](https://docs.appoptics.com/kb/user_org/tokens/#api-tokens-and-token-roles).
It has to be configured by user before running the role

```yaml
swisnap_hostname_alias: ""
```
Hostname alias for the server which will be used in AppOptics UI

```yaml
swisnap_main_config_path: /opt/SolarWinds/Snap/etc/config.yaml
```
Path to SolarWinds Snap Agent's main configuration file

```yaml
swisnap_plugins_config: /opt/SolarWinds/Snap/etc/plugins.d
```
Path to SolarWinds Snap Agent's plugin configuration files

```yaml
swinsap_publisher_appoptics_path: /opt/SolarWinds/Snap/etc/plugins.d/publisher-appoptics.yaml
```
Path to SolarWinds Snap Agent's publisher AppOptics configuration files

```yaml
swinsap_processes_appoptics_path: /opt/SolarWinds/Snap/etc/plugins.d/publisher-processes.yaml
```
Path to SolarWinds Snap Agent's publisher processes configuration files

```yaml
swisnap_auto_discover_path: /opt/SolarWinds/Snap/autoload
```
Path to SolarWinds Snap Agent's autoload directory for V1 plugins

```yaml
swisnap_tasks_autoload_path: /opt/SolarWinds/Snap/etc/tasks-autoload.d
```
Path to SolarWinds Snap Agent's V2 tasks files

```yaml
swisnap_plugin_path: /opt/SolarWinds/Snap/bin
```
Path where SolarWinds Snap Agent's plugins binaries are stored

```yaml
swisnap_task_path: /opt/SolarWinds/Snap/etc/tasks.d
```
Path to SolarWinds Snap Agent's V1 tasks files

```yaml
swisnap_service: swisnapd
swisnap_user: solarwinds
swisnap_user_group: solarwinds
```
Name of SolarWinds Snap Agent service. User and group under which service will operate

```yaml
swisnap_log_level: warning
swisnap_log_path: /var/log/SolarWinds/Snap
swisnap_log_format: text
```
Logging level, path to log file and log format.

```yaml
swisnap_plugin_trust_level: ""
swisnap_keyring_paths: ""
```
Plugin trust level for swisnapd. When enabled, only signed plugins that can be verified will be loaded into swisnapd. Signatures are verified from keyring files specified in swisnap_keyring_path. Valid values are 0 - Off, 1 - Enabled, 2 - Warning

```yaml
swisnap_tls_cert_path: ""
swisnap_tls_key_path: ""
swisnap_plugin_tls_cert_path: ""
swisnap_plugin_tls_key_path: ""
swisnap_ca_cert_paths: ""
```
Secure plugin communication optional parameters. 

```yaml
swisnap_plugin_load_timeout: ""
```
The maximal time allowed for a plugin to load. Default value is 30

```yaml
swisnap_global_tags: {}
```
Tags that will be applied to collected metrics across tasks

```yaml
swisnap_restapi_enable: true
swisnap_restapi_https: ""
swisnap_restapi_rest_auth: ""
swisnap_restapi_rest_auth_password: ""
swisnap_restapi_rest_certificate: ""
swisnap_restapi_rest_key: ""
swisnap_restapi_port: ""
swisnap_restapi_addr: ""
swisnap_restapi_plugin_load_timeout: ""
```
Optional REST API parameters. By default REST API is enabled

```yaml
publisher_appoptics_url: ""
publisher_processes_url: ""
```
These parameters can override default URL for publishers

```yaml
swisnap_proxy_url: ""
swisnap_proxy_user: ""
swisnap_proxy_password: ""
```
Optional proxy settings

```yaml
swisnap_host_check_timeout: ""
```
swisnap_host_check_timeout allows to configure timeout for querying host operating system for identification informations. Default value is set to 5s

```yaml
swisnap_ec2_check_timeout: ""
```
swisnap_ec2_check_timeout allows to configure timeout for querying EC2 instance metadata URL to determine if host agent is running on EC2 (or OpenStack) instance. By default it is set to 1s

```yaml
swisnap_ec2_check_retries: ""
```
swisnap_ec2_check_retries allows to configure number of retries for querying EC2 instance metadata URL to determine if host agent is running on EC2 (or OpenStack) instance. By default it is set to 3

```yaml
swisnap_floor_seconds: ""
```
whether to floor timestamps to a specific interval, default value is 60 seconds

```yaml
swisnap_period: ""
```
metrics interval period to report to AppOptics API, default value is 60 seconds

```yaml
swisnap_custom_v1_task_path: ""
swisnap_custom_v2_task_path: ""
swisnap_custom_plugin_configs_path: ""
```
Paths to directories with custom task and plugin configuration files. It allows users to configure additional plugins. It should be path to directory e.g. ``/path/to/directory``

```yaml
swisnap_win_installer_download_path: ""
```
Path to download Windows installer. It has to be configured by user before running the role on Windows platform

```yaml
swisnap_package_version: ""
```

Specific version of package to install e.g. `4.0.0.863` It works only for Linux platforms. For Windows always latest package is installed.

## Example Playbook

Install SolarWinds swinsap role using Ansible Galaxy:

```bash
ansible-galaxy install solarwinds.swisnap
```

or clone this repository to directory with your playbook's roles:

```bash
git clone https://github.com/solarwinds/ansible-swisnap.git solarwinds.swisnap
```

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
solarwinds_token: 123456789dbba089e9ff613bb9528320188853b1a08d91d23d2fc9bc1c41ec3e
```

### Windows:

```yaml
- hosts: windows
  vars_files:
    - vars/main.yml
  roles:
    - ansible-swisnap
```

Inside `vars/my_vars.yaml`:

```yaml
solarwinds_token: 123456789dbba089e9ff613bb9528320188853b1a08d91d23d2fc9bc1c41ec3e
swisnap_win_installer_download_path: "C:\\Users\\Administrator\\Downloads\\solarwinds-snap-agent-installer.msi"
```

Inside `inventory`:

```yaml
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
