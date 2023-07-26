import pytest
import os
from dxm.lib.DxEnvironment import env_worker
from dxm.lib.DxEngine.DxConfig import DxConfig
from dxm.lib.DxLogging import logging_est

CONFIGPATH='./test/testdb.db'
ENVNAME="env1"

@pytest.fixture(autouse=True)
def open_config_file():
    DxConfig(CONFIGPATH)


#logging_est('dxm.log', True)

@pytest.mark.dependency()
def test_environment_list_ignore(capsys):
    rc = env_worker.environment_list(
        p_engine="test_eng",
        p_username=None,
        format="csv",
        envname=ENVNAME
    )

    if rc == 1:
        pytest.skip("Environment non-exist")
    else:
        assert True

    


@pytest.mark.dependency(depends=['test_environment_list_ignore'])
def test_environment_delete_old_env():
    rc = env_worker.environment_delete(
        p_engine="test_eng",
        p_username=None,
        envname=ENVNAME 
    )

    assert rc == 0

def test_environment_add(capsys):
    rc = env_worker.environment_add(
        p_engine="test_eng",
        p_username=None,
        envname=ENVNAME,
        appname="app1",
        purpose="MASK"
    )

    output = "Environment {} added\n".format(ENVNAME)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)


def test_environment_list(capsys):
    rc = env_worker.environment_list(
        p_engine="test_eng",
        p_username=None,
        format="csv",
        envname=ENVNAME
    )

    output = "\n" + \
    "#Engine name,Environment name,Application name\n" + \
    "test_eng,{},app1\n\n\n".format(ENVNAME)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)


def test_environment_delete(capsys):
    rc = env_worker.environment_delete(
        p_engine="test_eng",
        p_username=None,
        envname=ENVNAME 
    )

    output = "Environment {} deleted\n".format(ENVNAME)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)

def test_environment_add_next_steps(capsys):
    rc = env_worker.environment_add(
        p_engine="test_eng",
        p_username=None,
        envname=ENVNAME,
        appname="app1",
        purpose="MASK"
    )

    output = "Environment {} added\n".format(ENVNAME)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)


def test_environment_list_next_steps(capsys):
    rc = env_worker.environment_list(
        p_engine="test_eng",
        p_username=None,
        format="csv",
        envname=ENVNAME
    )

    output = "\n" + \
    "#Engine name,Environment name,Application name\n" + \
    "test_eng,{},app1\n\n\n".format(ENVNAME)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)