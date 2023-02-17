import pytest
import os
from dxm.lib.DxRuleset import rule_worker
from dxm.lib.DxEngine.DxConfig import DxConfig
from dxm.lib.DxLogging import logging_est

CONFIGPATH='./test/testdb.db'
TABLEFILE='./test/table_list.txt'
FILEFILE='./test/file_list.txt'
RULESETNAME="rs_test_1"
RULESETNAME_FILE="rs_test_file_1"
METANAME1="COUNTRIES"
METANAME2="DEPARTMENTS"
METANAME3="EMPLOYEES"
METANAME_FILE1="maskme.txt"
FILEFORMAT_FILE='test_file_format.txt'

#logging_est('dxm.log', True)

def delete_meta(metalist):
    for metaname in metalist:
        rc = rule_worker.ruleset_listmeta(
            p_engine="test_eng",
            p_username=None,
            format="csv",
            rulesetname=RULESETNAME,
            envname=None,
            metaname=metaname
        )

        if rc == 0:
            rc_delete = rule_worker.ruleset_deletemeta(
                p_engine="test_eng",
                p_username=None,
                rulesetname=RULESETNAME,
                envname=None,
                metaname=metaname
            )
            if rc_delete != 0:
                return rc_delete

    return 0

@pytest.fixture(autouse=True)
def open_config_file():
    DxConfig(CONFIGPATH)

@pytest.mark.dependency()
def test_ruleset_meta_list_ignore(capsys):
    rc = rule_worker.ruleset_listmeta(
        p_engine="test_eng",
        p_username=None,
        format="csv",
        rulesetname=RULESETNAME,
        envname=None,
        metaname=METANAME1
    )

    if rc == 1:
        pytest.skip("Table non-exist")
    else:
        assert True

    
@pytest.mark.dependency(depends=['test_ruleset_meta_list_ignore'])
def test_ruleset_meta_delete_old_meta():
    rc = rule_worker.ruleset_deletemeta(
        p_engine="test_eng",
        p_username=None,
        rulesetname=RULESETNAME,
        envname=None,
        metaname=METANAME1
    )

    assert rc == 0


# adding single table
def test_ruleset_meta_add(capsys):

    params = {
        "rulesetname" : RULESETNAME,
        "envname": None,
        "metaname": METANAME1,
        "custom_sql": None,
        "where_clause": None,
        "having_clause": None,
        "key_column": None
    }

    rc = rule_worker.ruleset_addmeta(
        p_engine="test_eng",
        p_username=None,
        params=params,
        inputfile=None, 
        fromconnector=False, 
        bulk=False
    )

    output = "Table {} added\n".format(METANAME1)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)

def test_ruleset_meta_delete_singletable():
    rc = rule_worker.ruleset_deletemeta(
        p_engine="test_eng",
        p_username=None,
        rulesetname=RULESETNAME,
        envname=None,
        metaname=METANAME1
    )

    assert rc == 0

def test_ruleset_meta_add_fromfetch(capsys):

    params = {
        "rulesetname" : RULESETNAME,
        "envname": None,
        "metaname": None,
        "fetchfilter": None
    }

    rc = rule_worker.ruleset_addmeta(
        p_engine="test_eng",
        p_username=None,
        params=params,
        inputfile=None, 
        fromconnector=True, 
        bulk=True
    )

    output = "Task finished sucesfully" 

    captured = list(capsys.readouterr().out.splitlines())
    filtered = "\n".join([ x for x in captured if 'finished' in x])
    assert (rc, filtered) == (0, output)


def test_ruleset_meta_delete_after_fetchload(capsys):
    rc = delete_meta(['JOBS','EMPLOYEES','DEPARTMENTS','COUNTRIES','LOCATIONS','JOB_HISTORY','REGIONS'])
    assert rc == 0


def test_ruleset_meta_add_fromfile(capsys):

    params = {
        "rulesetname" : RULESETNAME,
        "envname" : None,
        "metaname": None
    }

    tablefile = open(TABLEFILE, "r")

    rc = rule_worker.ruleset_addmeta(
        p_engine="test_eng",
        p_username=None,
        params=params,
        inputfile=tablefile, 
        fromconnector=False, 
        bulk=False
    )

    output = "Table {} added\nTable {} added\nTable {} added\n".format(METANAME1, METANAME2, METANAME3)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)

def test_ruleset_meta_delete_before_add_fromfile_bulk(capsys):
    rc = delete_meta([METANAME1, METANAME2, METANAME3])
    assert rc == 0


def test_ruleset_meta_add_fromfile_bulk(capsys):

    params = {
        "rulesetname" : RULESETNAME,
        "envname": None,
        "metaname": None
    }

    tablefile = open(TABLEFILE, "r")

    rc = rule_worker.ruleset_addmeta(
        p_engine="test_eng",
        p_username=None,
        params=params,
        inputfile=tablefile, 
        fromconnector=False, 
        bulk=True
    )

    output = "Task finished sucesfully" 

    captured = list(capsys.readouterr().out.splitlines())
    filtered = "\n".join([ x for x in captured if 'finished' in x])
    assert (rc, filtered) == (0, output)


@pytest.mark.dependency()
def test_ruleset_meta_list_file_ignore(capsys):
    rc = rule_worker.ruleset_listmeta(
        p_engine="test_eng",
        p_username=None,
        format="csv",
        rulesetname=RULESETNAME_FILE,
        envname=None,
        metaname=METANAME_FILE1
    )

    if rc == 1:
        pytest.skip("Table non-exist")
    else:
        assert True

    
@pytest.mark.dependency(depends=['test_ruleset_meta_list_file_ignore'])
def test_ruleset_meta_delete_old_file():
    rc = rule_worker.ruleset_deletemeta(
        p_engine="test_eng",
        p_username=None,
        rulesetname=RULESETNAME_FILE,
        envname=None,
        metaname=METANAME_FILE1
    )

    assert rc == 0



def test_ruleset_meta_file_add(capsys):

    params = {
        "rulesetname" : RULESETNAME_FILE,
        "envname": None,
        "metaname": METANAME_FILE1,
        "file_format": FILEFORMAT_FILE,
        "file_delimiter": ',',
        "file_eor": 'linux',
        "file_enclosure": None,
        "file_name_regex": None,
        "file_eor_custom": None,
        "envname": None,
    }

    rc = rule_worker.ruleset_addmeta(
        p_engine="test_eng",
        p_username=None,
        params=params,
        inputfile=None, 
        fromconnector=False, 
        bulk=False
    )

    output = "File {} added\n".format(METANAME_FILE1)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)

def test_ruleset_meta_delete_singletable():
    rc = rule_worker.ruleset_deletemeta(
        p_engine="test_eng",
        p_username=None,
        rulesetname=RULESETNAME_FILE,
        envname=None,
        metaname=METANAME_FILE1
    )

    assert rc == 0


def test_ruleset_meta_file_add_from_file(capsys):

    params = {
        "rulesetname" : RULESETNAME_FILE,
        "envname": None,
        "metaname": None,
        "file_format": FILEFORMAT_FILE,
        "file_delimiter": ',',
        "file_eor": 'linux',
        "file_enclosure": None,
        "file_name_regex": None,
        "file_eor_custom": None,
        "envname": None,
        "fetchfilter": None
    }

    filefile = open(FILEFILE, "r")

    rc = rule_worker.ruleset_addmeta(
        p_engine="test_eng",
        p_username=None,
        params=params,
        inputfile=filefile, 
        fromconnector=False, 
        bulk=False
    )

    output = "File {} added\n".format(METANAME_FILE1)
    captured = capsys.readouterr()
    assert (rc, captured.out.replace('\r','')) == (0, output)


