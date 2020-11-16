import os
import pytest
import testinfra.utils.ansible_runner

PACKAGE_NAME = "solarwinds-snap-agent"
SOLARWINDS = "solarwinds"
SWISNAPD = "swisnapd"


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.fixture
def version(host):
    return host.package(PACKAGE_NAME).version


def test_solarwinds_snap_agent_package(host, version):
    swisnap = host.package(PACKAGE_NAME)
    assert swisnap.is_installed
    assert version.startswith("3.") or version.startswith("4.")


def test_swinsapd_service(host):
    swisnapd = host.service(SWISNAPD)
    assert swisnapd.is_running
    assert swisnapd.is_enabled


def test_process_swisnapd(host):
    assert host.process.get(user=SOLARWINDS, comm=SWISNAPD)
    # checking default collector plugins: aosystem, processes, logs
    assert len(host.process.filter(user=SOLARWINDS, comm="snap-plugin-col")) == 3
    # checking default publisher plugins: publisher-appoptics, publisher-processes
    assert len(host.process.filter(user=SOLARWINDS, comm="snap-plugin-pub")) == 2


def test_sockets(host, version):
    if version.startswith("4."):
        pytest.skip("Using unix socket from version 4.x.x")
    assert host.socket("tcp://127.0.0.1:21413").is_listening


def test_config_files(host):
    main_config = host.file("/opt/SolarWinds/Snap/etc/config.yaml")
    publisher_ao = host.file(
        "/opt/SolarWinds/Snap/etc/plugins.d/publisher-appoptics.yaml"
    )
    publisher_processes = host.file(
        "/opt/SolarWinds/Snap/etc/plugins.d/publisher-processes.yaml"
    )

    for config in (main_config, publisher_processes, publisher_processes):
        assert config.exists
        assert config.user == SOLARWINDS
        assert config.group == SOLARWINDS

    assert main_config.contains("auto_discover_path: /opt/SolarWinds/Snap/autoload")
    assert main_config.contains(
        "tasks_autoload_path: /opt/SolarWinds/Snap/etc/tasks-autoload.d"
    )
    assert main_config.contains("plugin_path: /opt/SolarWinds/Snap/bin")
    assert main_config.contains("task_path: /opt/SolarWinds/Snap/etc/tasks.d")
    assert main_config.contains("plugin_trust_level: 1")

    for publisher in (publisher_ao, publisher_ao):
        assert publisher.contains(
            "token: 123456789dbba089e9ff613bb9528320188853b1a08d91d23d2fc9bc1c41ec3e"
        )
        assert publisher.contains("hostname_alias: swisnap_hostname")
        assert publisher.contains("proxy_url: http://127.0.0.1:12345")
        assert publisher.contains("proxy_user: test_user")
        assert publisher.contains("proxy_password: test_pass")
        assert publisher.contains("host_check_timeout: 10s")
        assert publisher.contains("check_retries: 5")
        assert publisher.contains("floor_seconds: 50")
        assert publisher.contains("period: 30")
