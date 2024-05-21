import pytest
import os
from dxm.lib.DxTable import tab_worker
from dxm.lib.DxEngine.DxConfig import DxConfig
from dxm.lib.DxLogging import logging_est

CONFIGPATH='./test/testdb.db'
RULESETNAME="rs_test_1"
RULESETNAME_FILE="rs_test_file_1"
METANAME1="COUNTRIES"
METANAME2="DEPARTMENTS"
METANAME3="EMPLOYEES"
METANAME_FILE1="maskme.txt"

@pytest.fixture(autouse=True)
def open_config_file():
    DxConfig(CONFIGPATH)


def test_table_list_single(capsys):
    rc = tab_worker.tab_listtable_details(
        p_engine="test_eng",
        p_username=None,
        p_format="csv",
        rulesetname=RULESETNAME,
        envname=None,
        metaname=METANAME2
    )

    output = "\n" + \
        "#Engine name,Environent name,Ruleset name,Table name,Logical key,Where clause,Custom SQL\n" + \
        "test_eng,env1,rs_test_1,{},ROWID,,select * from {}\n\n\n".format(METANAME2,METANAME2)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)

def test_table_list_all(capsys):
    rc = tab_worker.tab_listtable_details(
        p_engine="test_eng",
        p_username=None,
        p_format="csv",
        rulesetname=RULESETNAME,
        envname=None,
        metaname=None
    )

    output = "#Engine name,Environent name,Ruleset name,Table name,Logical key,Where clause,Custom SQL\n" + \
        "test_eng,env1,rs_test_1,{},,,\n".format(METANAME1) + \
        "test_eng,env1,rs_test_1,{},ROWID,,select * from {}\n".format(METANAME2,METANAME2) + \
        "test_eng,env1,rs_test_1,{},ROWID,EMPLOYEE_ID<=200,".format(METANAME3) 

    # tables can be added in different order and there is no sort in the output 
    # so output from command needs to be sorted to match expected output
    captured = list(capsys.readouterr().out.splitlines())
    captured_sort = sorted(captured[2:])
    filtered = captured[1] + "\n" + "\n".join([x for x in captured_sort if x != ''])      
    assert (rc, filtered) == (0, output)


def test_table_update_single_remove_custom_sql(capsys):
    params = {
        "rulesetname": RULESETNAME,
        "metaname": METANAME2,
        "custom_sql": "",
        "where_clause": None,
        "having_clause": None,
        "key_column": 'DEPARTMENT_ID',
        "envname": None,
        "file_format": None,
        "file_delimiter": None,
        "file_eor": None,
        "file_enclosure": None,
        "file_name_regex": None,
        "file_eor_custom": None
    }

    rc = tab_worker.tab_update_meta(
        p_engine="test_eng",
        p_username=None,
        params=params
    )

    assert (rc == 0)

def test_table_update_single_set_where(capsys):
    params = {
        "rulesetname": RULESETNAME,
        "metaname": METANAME2,
        "custom_sql": None,
        "where_clause": 'MANAGER_ID<100',
        "having_clause": None,
        "key_column": 'DEPARTMENT_ID',
        "envname": None,
        "file_format": None,
        "file_delimiter": None,
        "file_eor": None,
        "file_enclosure": None,
        "file_name_regex": None,
        "file_eor_custom": None
    }

    rc = tab_worker.tab_update_meta(
        p_engine="test_eng",
        p_username=None,
        params=params
    )

    assert (rc == 0)


def test_table_list_single_after_update(capsys):
    rc = tab_worker.tab_listtable_details(
        p_engine="test_eng",
        p_username=None,
        p_format="csv",
        rulesetname=RULESETNAME,
        envname=None,
        metaname=METANAME2
    )

    output = "\n" + \
        "#Engine name,Environent name,Ruleset name,Table name,Logical key,Where clause,Custom SQL\n" + \
        "test_eng,env1,rs_test_1,{},DEPARTMENT_ID,MANAGER_ID<100,\n\n\n".format(METANAME2)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)

def test_table_update_single_revert(capsys):
    params = {
        "rulesetname": RULESETNAME,
        "metaname": METANAME2,
        "custom_sql": "select * from {}".format(METANAME2),
        "where_clause": "",
        "having_clause": None,
        "key_column": 'ROWID',
        "envname": None,
        "file_format": None,
        "file_delimiter": None,
        "file_eor": None,
        "file_enclosure": None,
        "file_name_regex": None,
        "file_eor_custom": None
    }

    rc = tab_worker.tab_update_meta(
        p_engine="test_eng",
        p_username=None,
        params=params
    )

    assert (rc == 0)


def test_file_list_single(capsys):
    rc = tab_worker.tab_listfile_details(
        p_engine="test_eng",
        p_username=None,
        p_format="csv",
        rulesetname=RULESETNAME_FILE,
        envname=None,
        metaname=METANAME_FILE1
    )

    output = "\n" + \
        "#Engine name,Environent name,Ruleset name,File name,File type,File format name,Delimiter,End of record\n" + \
        "test_eng,env1,{},{},DELIMITED,test_file_format.txt,,,'\\n'\n\n\n".format(RULESETNAME_FILE,METANAME_FILE1)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)


def test_file_update_single(capsys):
    params = {
        "rulesetname": RULESETNAME_FILE,
        "metaname": METANAME_FILE1,
        "envname": None,
        "custom_sql": None,
        "where_clause": None,
        "having_clause": None,
        "key_column": None,
        "file_format": None,
        "file_delimiter": "|",
        "file_eor": None,
        "file_enclosure": None,
        "file_name_regex": None,
        "file_eor_custom": None
    }

    rc = tab_worker.tab_update_meta(
        p_engine="test_eng",
        p_username=None,
        params=params
    )

    assert (rc == 0)

def test_file_list_single_after_update(capsys):
    rc = tab_worker.tab_listfile_details(
        p_engine="test_eng",
        p_username=None,
        p_format="csv",
        rulesetname=RULESETNAME_FILE,
        envname=None,
        metaname=METANAME_FILE1
    )

    output = "\n" + \
        "#Engine name,Environent name,Ruleset name,File name,File type,File format name,Delimiter,End of record\n" + \
        "test_eng,env1,{},{},DELIMITED,test_file_format.txt,|,'\\n'\n\n\n".format(RULESETNAME_FILE,METANAME_FILE1)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)


def test_file_update_single_revert(capsys):
    params = {
        "rulesetname": RULESETNAME_FILE,
        "metaname": METANAME_FILE1,
        "envname": None,
        "custom_sql": None,
        "where_clause": None,
        "having_clause": None,
        "key_column": None,
        "file_format": None,
        "file_delimiter": ",",
        "file_eor": None,
        "file_enclosure": None,
        "file_name_regex": None,
        "file_eor_custom": None
    }

    rc = tab_worker.tab_update_meta(
        p_engine="test_eng",
        p_username=None,
        params=params
    )

    assert (rc == 0)