import pytest
import os
from dxm.lib.DxFileFormat import fileformat_worker
from dxm.lib.DxEngine.DxConfig import DxConfig
from dxm.lib.DxLogging import logging_est

CONFIGPATH='./test/testdb.db'
FILEFORMAT="fileconn"
FILEFORMAT_FILE='./test/test_file_format.txt'

#logging_est('dxm.log', True)

@pytest.fixture(autouse=True)
def open_config_file():
    DxConfig(CONFIGPATH)


@pytest.mark.dependency()
def test_fileformat_list_ignore(capsys):
    rc = fileformat_worker.fileformat_list(
        p_engine="test_eng",
        p_username=None,
        format="csv",
        fileformat_type='DELIMITED',
        fileformat_name=os.path.basename(FILEFORMAT_FILE)
    )

    if rc != 0:
        pytest.skip("Fileformat non-exist")
    else:
        assert True

    


@pytest.mark.dependency(depends=['test_fileformat_list_ignore'])
def test_fileformat_delete_old():
    rc = fileformat_worker.fileformat_delete(
        p_engine="test_eng",
        p_username=None,
        fileformat_name=os.path.basename(FILEFORMAT_FILE)
    )

    assert rc == 0


def test_fileformat_add(capsys):
    f = open(FILEFORMAT_FILE, 'r')
    rc = fileformat_worker.fileformat_add(
        p_engine="test_eng",
        p_username=None,
        fileformat_type='delimited', 
        fileformat_file=f
    )

    output = "Filetype {} added\n".format(os.path.basename(FILEFORMAT_FILE))
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)

def test_fileformat_list(capsys):
    rc = fileformat_worker.fileformat_list(
        p_engine="test_eng",
        p_username=None,
        format="csv",
        fileformat_type='DELIMITED',
        fileformat_name=os.path.basename(FILEFORMAT_FILE)
    )

    output = "\n" + \
    "#Engine name,File format type,File format name\n" + \
    "test_eng,DELIMITED,{}\n\n\n".format(os.path.basename(FILEFORMAT_FILE))
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)