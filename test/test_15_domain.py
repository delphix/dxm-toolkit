import pytest
import os
from dxm.lib.DxDomain import domain_worker
from dxm.lib.DxEngine.DxConfig import DxConfig

CONFIGPATH='./test/testdb.db'
DOMAIN_NAME1="TEST_DOMAIN"
ALG_NAME="dlpx-core:FirstName"
ALG_NAME2="dlpx-core:LastName"
DOMAIN_NAME2="ACCOUNT_NO"


@pytest.fixture(autouse=True)
def open_config_file():
    DxConfig(CONFIGPATH)


@pytest.mark.dependency()
def test_domain_list_ignore(capsys):
    rc = domain_worker.domain_list(
        p_engine="test_eng",
        p_username=None,
        format="csv",
        domainname=DOMAIN_NAME1
    )

    if rc == 1:
        pytest.skip("Domain non-exist")
    else:
        assert True

    


@pytest.mark.dependency(depends=['test_domain_list_ignore'])
def test_domain_delete_ifexist(capsys):
    rc = domain_worker.domain_delete(
        p_engine="test_eng",
        p_username=None,
        domain_name=DOMAIN_NAME1
    )

def test_domain_add(capsys):
    rc = domain_worker.domain_add(
        p_engine="test_eng",
        p_username=None,
        domain_name=DOMAIN_NAME1,
        classification=None,
        default_algname=ALG_NAME
    )

    output = "Domain {} added\n".format(DOMAIN_NAME1)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)


def test_domain_list(capsys):
    rc = domain_worker.domain_list(
        p_engine="test_eng",
        p_username=None,
        format="csv",
        domainname=DOMAIN_NAME1
    )

    output = "\n" + \
    "#Engine name,Domain name\n" + \
    "test_eng,{}\n\n\n".format(DOMAIN_NAME1)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)


def test_domain_update(capsys):
    rc = domain_worker.domain_update(
        p_engine="test_eng",
        p_username=None,
        domain_name=DOMAIN_NAME1,
        classification=None,
        default_algname=ALG_NAME2
    )

    output = "Domain {} updated\n".format(DOMAIN_NAME1)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)

def test_domain_delete(capsys):
    rc = domain_worker.domain_delete(
        p_engine="test_eng",
        p_username=None,
        domain_name=DOMAIN_NAME1
    )

    output = "Domain {} deleted\n".format(DOMAIN_NAME1)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)
