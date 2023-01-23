import pytest
import os
from dxm.lib.DxConnector import conn_worker
from dxm.lib.DxEngine.DxConfig import DxConfig
from dxm.lib.DxLogging import logging_est

CONFIGPATH='./test/testdb.db'
CONNNAME="oraconn"
ENVNAME="env1"

#logging_est('dxm.log', True)

params = {
    'envname': ENVNAME,
    'schemaName': 'HR',
    'host': 'marcindxmcdb.dlpxdc.co',
    'port': 1521,
    'password': 'hr',
    'username': 'HR',
    'connname': CONNNAME,
    'sid': 'DBOMSR3A85E9',
    'type': 'oracle',
    'jdbc': None,
    'instancename': None,
    'databasename': None,
    'jdbc_driver_name': None
}

@pytest.fixture(autouse=True)
def open_config_file():
    DxConfig(CONFIGPATH)


@pytest.mark.dependency()
def test_connector_list_ignore(capsys):
    rc = conn_worker.connector_list(
        p_engine="test_eng",
        p_username=None,
        format="csv",
        envname=None,
        connector_name=CONNNAME,
        details=False
    )

    if rc == 1:
        pytest.skip("Connector non-exist")
    else:
        assert True

    


@pytest.mark.dependency(depends=['test_connector_list_ignore'])
def test_connector_delete_old_env():
    rc = conn_worker.connector_delete(
        p_engine="test_eng",
        p_username=None,
        connectorname=CONNNAME,
        envname="env1"
    )

    assert rc == 0


def test_connector_add(capsys):
    rc = conn_worker.connector_add(
        p_engine="test_eng",
        p_username=None,
        params=params
    )

    output = "Connector {} added\n".format(CONNNAME)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)


def test_connector_list(capsys):
    rc = conn_worker.connector_list(
        p_engine="test_eng",
        p_username=None,
        format="csv",
        envname=None,
        connector_name=CONNNAME,
        details=False
    )

    output = "\n" + \
    "#Engine name,Environment name,Connector name,Connector type\n" + \
    "test_eng,{},{},ORACLE\n\n\n".format(ENVNAME, CONNNAME)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)


def test_connector_test(capsys):
    rc = conn_worker.connector_test(
        p_engine="test_eng",
        p_username=None,
        envname=None,
        connectorname=CONNNAME
    )

    output = "Connector test {} succeeded\n".format(CONNNAME)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)


def test_connector_fetch(capsys):
    rc = conn_worker.connector_fetch(
        p_engine="test_eng",
        p_username=None,
        envname=None,
        connectorname=CONNNAME,
        format="csv"
    )

    output = "\n" + \
    "#Engine name,Connector name,Table name\n" + \
    "test_eng,{},COUNTRIES\n".format(CONNNAME) + \
    "test_eng,{},DEPARTMENTS\n".format(CONNNAME) + \
    "test_eng,{},EMPLOYEES\n".format(CONNNAME) + \
    "test_eng,{},JOBS\n".format(CONNNAME) + \
    "test_eng,{},JOB_HISTORY\n".format(CONNNAME) + \
    "test_eng,{},LOCATIONS\n".format(CONNNAME) + \
    "test_eng,{},REGIONS\n\n\n".format(CONNNAME)

    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)


def test_connector_delete(capsys):
    rc = conn_worker.connector_delete(
        p_engine="test_eng",
        p_username=None,
        connectorname=CONNNAME,
        envname="env1"
    )

    output = "Connector {} deleted\n".format(CONNNAME)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)

def test_connector_add_next_steps(capsys):
    rc = conn_worker.connector_add(
        p_engine="test_eng",
        p_username=None,
        params=params
    )

    output = "Connector {} added\n".format(CONNNAME)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)


def test_connector_list_next_steps(capsys):
    rc = conn_worker.connector_list(
        p_engine="test_eng",
        p_username=None,
        format="csv",
        envname=None,
        connector_name=CONNNAME,
        details=False
    )

    output = "\n" + \
    "#Engine name,Environment name,Connector name,Connector type\n" + \
    "test_eng,{},{},ORACLE\n\n\n".format(ENVNAME, CONNNAME)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)