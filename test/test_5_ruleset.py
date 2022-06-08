import pytest
import os
from dxm.lib.DxRuleset import rule_worker
from dxm.lib.DxEngine.DxConfig import DxConfig
from dxm.lib.DxLogging import logging_est

CONFIGPATH='./test/testdb.db'
CONNNAME="oraconn"
ENVNAME="env1"
RULESETNAME="rs_test_1"

#logging_est('dxm.log', True)

@pytest.fixture(autouse=True)
def open_config_file():
    DxConfig(CONFIGPATH)


@pytest.mark.dependency()
def test_ruleset_list_ignore(capsys):
    rc = rule_worker.ruleset_list(
        p_engine="test_eng",
        p_username=None,
        format="csv",
        rulesetName=RULESETNAME,
        envname=None
    )

    if rc == 1:
        pytest.skip("Ruleset non-exist")
    else:
        assert True

    


@pytest.mark.dependency(depends=['test_ruleset_list_ignore'])
def test_ruleset_delete_old_env():
    rc = rule_worker.ruleset_delete(
        p_engine="test_eng",
        p_username=None,
        rulesetname=RULESETNAME,
        envname=None
    )

    assert rc == 0


def test_ruleset_add(capsys):
    rc = rule_worker.ruleset_add(
        p_engine="test_eng",
        p_username=None,
        rulesetname=RULESETNAME,
        connectorname=CONNNAME,
        envname=ENVNAME
    )

    output = "Ruleset {} added\n".format(RULESETNAME)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)

def test_ruleset_list(capsys):
    rc = rule_worker.ruleset_list(
        p_engine="test_eng",
        p_username=None,
        format="csv",
        rulesetName=RULESETNAME,
        envname=None
    )

    output = "\n" + \
    "#Engine name,Ruleset name,Connector name,Metadata type,Connector type,Environent name\n" + \
    "test_eng,{},{},Database,ORACLE,{}\n\n\n".format(RULESETNAME, CONNNAME, ENVNAME)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)