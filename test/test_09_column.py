import pytest
import os
from dxm.lib.DxColumn import column_worker
from dxm.lib.DxEngine.DxConfig import DxConfig
from dxm.lib.DxLogging import logging_est


CONFIGPATH='./test/testdb.db'
RULESETNAME="rs_test_1"
RULESETNAME_FILE="rs_test_file_1"
METANAME1="COUNTRIES"
METANAME2="DEPARTMENTS"
METANAME3="EMPLOYEES"
COLUMNNAME1="FIRST_NAME"
ALGNAME1="dlpx-core:FirstName"
DOMAINNAME="FIRST_NAME"
METANAME_FILE1="maskme.txt"

#logging_est('dxm.log', True)

@pytest.fixture(autouse=True)
def open_config_file():
    DxConfig(CONFIGPATH)


def test_column_list_single(capsys):
    rc = column_worker.column_list(
        p_engine="test_eng",
        p_username=None,
        format="csv",
        rulesetname=RULESETNAME,
        envname=None,
        metaname=METANAME3,
        columnname=COLUMNNAME1,
        sortby=None,
        algname=None,
        is_masked=None
    )

    output = "\n" + \
        "#Engine name,Environment name,Ruleset name,Metadata name,Column name,Type,Data type,Date format,Domain name,Alg name\n" + \
        "test_eng,env1,{},{},{},IX,VARCHAR2(20),-,,\n\n\n".format(RULESETNAME,METANAME3,COLUMNNAME1)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)

def test_column_list_onetable(capsys):
    rc = column_worker.column_list(
        p_engine="test_eng",
        p_username=None,
        format="csv",
        rulesetname=RULESETNAME,
        envname=None,
        metaname=METANAME3,
        columnname=None,
        sortby=None,
        algname=None,
        is_masked=None
    )

    output = "\n" + \
        "#Engine name,Environment name,Ruleset name,Metadata name,Column name,Type,Data type,Date format,Domain name,Alg name\n" + \
        "test_eng,env1,rs_test_1,EMPLOYEES,COMMISSION_PCT,,NUMBER(2),-,,\n" + \
        "test_eng,env1,rs_test_1,EMPLOYEES,DEPARTMENT_ID,FK IX,NUMBER(4),-,,\n" + \
        "test_eng,env1,rs_test_1,EMPLOYEES,EMAIL,IX,VARCHAR2(25),-,,\n" + \
        "test_eng,env1,rs_test_1,EMPLOYEES,EMPLOYEE_ID,PK IX,NUMBER(6),-,,\n" + \
        "test_eng,env1,rs_test_1,EMPLOYEES,FIRST_NAME,IX,VARCHAR2(20),-,,\n" + \
        "test_eng,env1,rs_test_1,EMPLOYEES,HIRE_DATE,,DATE(7),-,,\n" + \
        "test_eng,env1,rs_test_1,EMPLOYEES,JOB_ID,FK IX,VARCHAR2(10),-,,\n" + \
        "test_eng,env1,rs_test_1,EMPLOYEES,LAST_NAME,IX,VARCHAR2(25),-,,\n" + \
        "test_eng,env1,rs_test_1,EMPLOYEES,MANAGER_ID,FK IX,NUMBER(6),-,,\n" + \
        "test_eng,env1,rs_test_1,EMPLOYEES,PHONE_NUMBER,,VARCHAR2(20),-,,\n" + \
        "test_eng,env1,rs_test_1,EMPLOYEES,SALARY,,NUMBER(8),-,,\n\n\n"
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)

def test_column_set_masking(capsys):
    rc = column_worker.column_setmasking(
        p_engine="test_eng",
        p_username=None,
        rulesetname=RULESETNAME,
        envname=None,
        metaname=METANAME3,
        columnname=COLUMNNAME1,
        algname=ALGNAME1,
        domainname=DOMAINNAME,
        dateformat=None,
        idmethod=None
    )

    output = "Column FIRST_NAME updated\n" + \
        "Algorithm dlpx-core:FirstName domain FIRST_NAME updated for ruleset rs_test_1 meta EMPLOYEES column FIRST_NAME\n"
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)

def test_column_confirm_masking_singlecol(capsys):
    rc = column_worker.column_list(
        p_engine="test_eng",
        p_username=None,
        format="csv",
        rulesetname=RULESETNAME,
        envname=None,
        metaname=METANAME3,
        columnname=COLUMNNAME1,
        sortby=None,
        algname=None,
        is_masked=None
    )

    output = "\n" + \
        "#Engine name,Environment name,Ruleset name,Metadata name,Column name,Type,Data type,Date format,Domain name,Alg name\n" + \
        "test_eng,env1,{},{},{},IX,VARCHAR2(20),-,{},{}\n\n\n".format(RULESETNAME,METANAME3,COLUMNNAME1,DOMAINNAME,ALGNAME1)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)

def test_column_set_unmasking(capsys):
    rc = column_worker.column_unsetmasking(
        p_engine="test_eng",
        p_username=None,
        rulesetname=RULESETNAME,
        envname=None,
        metaname=METANAME3,
        columnname=COLUMNNAME1
    )

    output = "Column FIRST_NAME updated\n" + \
        "Algorithm None domain None updated for ruleset rs_test_1 meta EMPLOYEES column FIRST_NAME\n"
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)


def test_column_cofirm_unmask_singlecol(capsys):
    rc = column_worker.column_list(
        p_engine="test_eng",
        p_username=None,
        format="csv",
        rulesetname=RULESETNAME,
        envname=None,
        metaname=METANAME3,
        columnname=COLUMNNAME1,
        sortby=None,
        algname=None,
        is_masked=None
    )

    output = "\n" + \
        "#Engine name,Environment name,Ruleset name,Metadata name,Column name,Type,Data type,Date format,Domain name,Alg name\n" + \
        "test_eng,env1,{},{},{},IX,VARCHAR2(20),-,,\n\n\n".format(RULESETNAME,METANAME3,COLUMNNAME1)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)