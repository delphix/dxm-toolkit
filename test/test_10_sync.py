import pytest
import os
from dxm.lib.DxSync import sync_worker
from dxm.lib.DxEngine.DxConfig import DxConfig
from dxm.lib.DxLogging import logging_est


CONFIGPATH='./test/testdb.db'
ALGNAME1="dlpx-core:FirstName"


#logging_est('dxm.log', True)

@pytest.fixture(autouse=True)
def open_config_file():
    DxConfig(CONFIGPATH)


def test_algorithm_list_single(capsys):

    rc = sync_worker.sync_list(
        p_engine="test_eng",
        p_username=None,
        format="csv",
        envname=None,
        objecttype=None,
        objectname=ALGNAME1
    )

    output = "\n" + \
        "#Engine name,Object type,Env name,Object name,Revision\n" + \
        "test_eng,USER_ALGORITHM,global,{}\n\n".format(ALGNAME1)
    captured = capsys.readouterr()

    # remove revision
    print(captured.out)

    output_from_cpmmand = []

    "aa".split()

    for line in captured.out.splitlines():
        if "test_eng" in line:
            output_from_cpmmand.append(",".join(line.split(',')[0:4]))
        else:
            output_from_cpmmand.append(line.replace("\r",""))

    assert (rc, "\n".join(output_from_cpmmand)) == (0, output)


def test_algorithm_export_single(capsys):

    rc = sync_worker.sync_export(
        p_engine="test_eng",
        p_username=None,
        envname=None,
        objecttype=None,
        objectname=ALGNAME1,
        path="./test/"
    )

    output = "Exported object types: \n" + \
             'USER_ALGORITHM\n' + \
             'Object saved to ./test/user_algorithm_{}.bin\n'.format(ALGNAME1)

    captured = capsys.readouterr()


    assert (rc, captured.out.replace("\r","")) == (0, output)


def test_algorithm_import_single(capsys):


    input_file_handler = open("./test/user_algorithm_dlpx-core:FirstName.bin","rb")

    rc = sync_worker.sync_import(
        p_engine="test_eng",
        p_username=None,
        envname=None,
        inputpath=None,
        inputfile=input_file_handler,
        force=True
    )

    output = "File ./test/user_algorithm_{}.bin was loaded or engine revision is in sync with file\n".format(ALGNAME1)

    captured = capsys.readouterr()


    assert (rc, captured.out.replace("\r","")) == (0, output)