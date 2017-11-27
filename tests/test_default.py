import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')


def test_verify_curator_bin(File):
    f = File('/usr/bin/curator')
    assert f.exists


@pytest.mark.parametrize("configfile", [
    ("actions.yml"),
    ("curator.yml")
])
def test_verify_curator_conf_files(File, configfile):
    f = File('/etc/elasticsearch-curator/' + configfile)
    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


@pytest.mark.parametrize("configfile,teststring", [
    ("actions.yml",
     "timestring: '%Y.%m.%d'"),
    ("actions.yml",
     "action: delete_indices"),
    ("actions.yml",
     "3:"),
    ("actions.yml",
     "direction: younger"),
    ("actions.yml",
     "unit_count: 14"),
    ("actions.yml",
     "continue_if_exception: False"),
    ("actions.yml",
     "disable_action: True"),
    ("actions.yml",
     "value: logstash-"),
    ("curator.yml",
     "logfile: /var/log/elasticsearch-curator.log"),
    ("curator.yml",
     "loglevel: INFO"),
    ("curator.yml",
     "port: 9200"),
    ("curator.yml",
     "hosts: localhost"),
    ("curator.yml",
     "ssl_no_validate: False"),
    ("curator.yml",
     "master_only: False")
])
def test_curator_config(File, configfile, teststring):
    f = File('/etc/elasticsearch-curator/' + configfile)
    assert f.contains(teststring)


@pytest.mark.parametrize("teststring", [
    ("Ansible: Curate Elasticsearch Indices once per week"),
    ("0 0 \* \* 6 root /usr/bin/curator --config"),
    ("/etc/elasticsearch-curator/curator.yml"),
    ("/etc/elasticsearch-curator/actions.yml")
])
def test_curator_cron_job(File, teststring):
    f = File('/etc/cron.d/elasticsearch-curator')
    assert f.contains(teststring)


def test_curator_version(Command):
    version = Command("curator --version")
    assert '5.4.0' in version.stdout
