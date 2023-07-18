import pytest
import os
from dxm.lib.DxEngine import eng_worker
from dxm.lib.DxEngine.DxConfig import DxConfig

CONFIGPATH='./test/testdb.db'

if os.path.isfile(CONFIGPATH):
    os.remove(CONFIGPATH)


@pytest.fixture(autouse=True)
def open_config_file():
    DxConfig(CONFIGPATH)



def test_engine_add():
    rc = eng_worker.engine_add(
        p_engine="test_eng",
        p_ip="wrong.dlpxdc.co",
        p_username="admin",
        p_password="Admin-12",
        p_port=80,
        p_protocol="http",
        p_default='Y',
        p_proxyurl=None,
        p_proxypassword=None,
        p_proxyuser=None
    )

    assert rc == 0


def test_engine_list_initial(capsys):

    rc = eng_worker.engine_list(
        p_engine="test_eng",
        p_username=None,
        p_format='csv'
    )

    captured = capsys.readouterr()

    output = "\n" + \
    "#Engine name,IP,username,protocol,port,default,proxy URL,proxy user\n" + \
    "test_eng,wrong.dlpxdc.co,admin,http,80,Y,N/A,N/A\n\n\n"

    assert (rc, captured.out.replace('\r','')) == (0, output)


def test_engine_delete(capsys):

    rc = eng_worker.engine_delete(
        p_engine="test_eng",
        p_engineuser=None
    )

    captured = capsys.readouterr()

    output = "Engine test_eng deleted\nEngine deleted from configuration\n" 

    assert (rc, captured.out.replace('\r','')) == (0, output)


def test_engine_add_2nd():
    rc = eng_worker.engine_add(
        p_engine="test_eng",
        p_ip="wrong.dlpxdc.co",
        p_username="admin",
        p_password="Admin-12",
        p_port=80,
        p_protocol="http",
        p_default='Y',
        p_proxyurl=None,
        p_proxypassword=None,
        p_proxyuser=None
    )

    assert rc == 0

def test_engine_update(capsys, engine):

    rc = eng_worker.engine_update(
        p_engine="test_eng",
        p_engineuser="admin",
        p_ip=engine,
        p_username="admin",
        p_password=None,
        p_port=None,
        p_protocol=None,
        p_default=None,
        p_proxyurl=None,
        p_proxypassword=None,
        p_proxyuser=None
    )

    captured = capsys.readouterr()

    output = "Configuration for engine test_eng updated in database\n"

    assert (rc, captured.out.replace('\r','')) == (0, output)


def test_engine_list(capsys, engine):

    rc = eng_worker.engine_list(
        p_engine="test_eng",
        p_username=None,
        p_format='csv'
    )

    output = "\n" + \
    "#Engine name,IP,username,protocol,port,default,proxy URL,proxy user\n" + \
    "test_eng,{},admin,http,80,Y,N/A,N/A\n\n\n".format(engine)

    captured = capsys.readouterr()

    assert (rc, captured.out.replace('\r','')) == (0, output)