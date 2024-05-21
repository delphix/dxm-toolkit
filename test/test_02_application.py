import pytest
import os
from dxm.lib.DxApplication import app_worker
from dxm.lib.DxEngine.DxConfig import DxConfig

CONFIGPATH='./test/testdb.db'
APPNAME="app1"
APPCRUDNAME="appcrud"

@pytest.fixture(autouse=True)
def open_config_file():
    DxConfig(CONFIGPATH)


@pytest.mark.dependency()
def test_application_list_ignore(capsys):
    rc = app_worker.application_list(
        p_engine="test_eng",
        p_username=None,
        format="csv",
        appname=APPNAME
    )

    if rc == 0:
        pytest.skip("App exist")
    else:
        assert True

    
@pytest.mark.dependency(depends=['test_application_list_ignore'])
def test_application_add(capsys):
    rc = app_worker.application_add(
        p_engine="test_eng",
        p_username=None,
        appname=APPNAME
    )

    output = "Application {} added\n".format(APPNAME)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)


def test_application_list(capsys):
    rc = app_worker.application_list(
        p_engine="test_eng",
        p_username=None,
        format="csv",
        appname=APPNAME
    )

    output = "\n" + \
    "#Engine name,Application name\n" + \
    "test_eng,{}\n\n\n".format(APPNAME)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)


@pytest.mark.dependency()
def test_appcrud_list_ignore(capsys):
    rc = app_worker.application_list(
        p_engine="test_eng",
        p_username=None,
        format="csv",
        appname=APPCRUDNAME
    )

    if rc == 1:
        pytest.skip("App non-exist")
    else:
        assert True

    
@pytest.mark.dependency(depends=['test_appcrud_list_ignore'])
def test_appcrud_delete_ignore(capsys):
    rc = app_worker.application_delete(
        p_engine="test_eng",
        p_username=None,
        appname=APPCRUDNAME
    )

    output = "Application {} deleted\n".format(APPCRUDNAME)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)


def test_appcrud_add(capsys):
    rc = app_worker.application_add(
        p_engine="test_eng",
        p_username=None,
        appname=APPCRUDNAME
    )

    output = "Application {} added\n".format(APPCRUDNAME)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)


def test_appcrud_list(capsys):
    rc = app_worker.application_list(
        p_engine="test_eng",
        p_username=None,
        format="csv",
        appname=APPCRUDNAME
    )

    output = "\n" + \
    "#Engine name,Application name\n" + \
    "test_eng,{}\n\n\n".format(APPCRUDNAME)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)

def test_appcrud_delete(capsys):
    rc = app_worker.application_delete(
        p_engine="test_eng",
        p_username=None,
        appname=APPCRUDNAME
    )

    output = "Application {} deleted\n".format(APPCRUDNAME)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)
