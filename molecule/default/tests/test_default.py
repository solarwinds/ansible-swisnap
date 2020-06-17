import os
import testinfra.utils.ansible_runner

SOLARWINDS = "solarwinds"
SWISNAPD = "swisnapd"


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_solarwinds_snap_agent_package(host):
    swisnap = host.package("solarwinds-snap-agent")
    assert swisnap.is_installed
    assert swisnap.version.startswith("3.")


def test_swinsapd_service(host):
    swisnapd = host.service(SWISNAPD)
    assert swisnapd.is_running
    assert swisnapd.is_enabled


def test_process_swisnapd(host):
    assert host.process.get(user=SOLARWINDS, comm=SWISNAPD)
    assert len(host.process.filter(user=SOLARWINDS, comm="snap-plugin-col")) == 2
    assert len(host.process.filter(user=SOLARWINDS, comm="snap-plugin-pub")) == 2


def test_sockets(host):
    assert host.socket("tcp://127.0.0.1:21413").is_listening


def test_config_files(host):
    main_config = host.file("/opt/SolarWinds/Snap/etc/config.yaml")
    publisher_ao = host.file(
        "/opt/SolarWinds/Snap/etc/plugins.d/publisher-appoptics.yaml"
    )
    publisher_processes = host.file(
        "/opt/SolarWinds/Snap/etc/plugins.d/publisher-processes.yaml"
    )

    for config in [main_config, publisher_processes, publisher_processes]:
        assert config.exists
        assert config.user == SOLARWINDS
        assert config.group == SOLARWINDS

    assert main_config.contains("auto_discover_path: /opt/SolarWinds/Snap/autoload")
    assert main_config.contains(
        "tasks_autoload_path: /opt/SolarWinds/Snap/etc/tasks-autoload.d"
    )
    assert main_config.contains("plugin_path: /opt/SolarWinds/Snap/bin")
    assert main_config.contains("task_path: /opt/SolarWinds/Snap/etc/tasks.d")

    for publisher in (publisher_ao, publisher_ao):
        assert publisher.contains(
            "token: 123456789dbba089e9ff613bb9528320188853b1a08d91d23d2fc9bc1c41ec3e"
        )
