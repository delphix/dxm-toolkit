import pytest
import os
from dxm.lib.DxUser import user_worker
from dxm.lib.DxEngine.DxConfig import DxConfig
from dxm.lib.DxLogging import logging_est


CONFIGPATH='./test/testdb.db'
USERNAME1="nonadmin"
USERNAME2="admin2"
ROLENAME="Operator" 


#logging_est('dxm.log', True)

@pytest.fixture(autouse=True)
def open_config_file():
    DxConfig(CONFIGPATH)


@pytest.mark.dependency()
def test_user_list_ignore(capsys):
    rc = user_worker.user_list(
        p_engine="test_eng",
        p_username=None,
        format="csv",
        username = USERNAME1
    )

    if rc == 1:
        pytest.skip("User non-exist")
    else:
        assert True

    

@pytest.mark.dependency(depends=['test_user_list_ignore'])
def test_user_delete_old_user():
    rc = user_worker.user_delete(
        p_engine="test_eng",
        p_username=None,
        username=USERNAME1,
        force=False
    )

    assert rc == 0

@pytest.mark.dependency()
def test_user2_list_ignore(capsys):
    rc = user_worker.user_list(
        p_engine="test_eng",
        p_username=None,
        format="csv",
        username = USERNAME2
    )

    if rc == 1:
        pytest.skip("User non-exist")
    else:
        assert True

    

@pytest.mark.dependency(depends=['test_user2_list_ignore'])
def test_user2_delete_old_user():
    rc = user_worker.user_delete(
        p_engine="test_eng",
        p_username=None,
        username=USERNAME2,
        force=True
    )

    assert rc == 0


def test_add_nonadmin_user_single(capsys):

    rc = user_worker.user_add(
        p_engine="test_eng",
        p_username=None,
        username=USERNAME1,
        firstname="non",
        lastname="user",
        email="non@admin.com",
        password="Admin-12",
        user_type="nonadmin",
        user_role=ROLENAME,
        user_environments="env1"
    )


    output = "User {} added\n".format(USERNAME1)

    captured = capsys.readouterr()


    assert (rc, captured.out.replace("\r","")) == (0, output)


def test_nonadmin_list(capsys):
    rc = user_worker.user_list(
        p_engine="test_eng",
        p_username=None,
        format="csv",
        username = USERNAME1
    )



    output = "\n#Engine name,User name,First name,Last name,E-mail,Auth type,Principal,Role name,Locked,Environment list\n" + \
             "test_eng,{},non,user,non@admin.com,NATIVE,,Operator,Open,env1\n\n\n".format(USERNAME1)

    captured = capsys.readouterr()

    assert (rc, captured.out.replace('\r','')) == (0, output)



def test_nonadmin_update(capsys):
    rc = user_worker.user_update(
        p_engine="test_eng",
        p_username=None,
        username = USERNAME1,
        user_role='DBA',
        user_environments='',
        firstname=None,
        lastname=None,
        email=None,
        password=None,
        user_type=None
    )

    output = "User {} updated\n".format(USERNAME1)

    captured = capsys.readouterr()
    assert (rc, captured.out.replace("\r","")) == (0, output)


def test_nonadmin_list_with_update(capsys):
    rc = user_worker.user_list(
        p_engine="test_eng",
        p_username=None,
        format="csv",
        username = USERNAME1
    )



    output = "\n#Engine name,User name,First name,Last name,E-mail,Auth type,Principal,Role name,Locked,Environment list\n" + \
             "test_eng,{},non,user,non@admin.com,NATIVE,,DBA,Open,\n\n\n".format(USERNAME1)

    captured = capsys.readouterr()

    assert (rc, captured.out.replace('\r','')) == (0, output)


def test_add_admin_user(capsys):

    rc = user_worker.user_add(
        p_engine="test_eng",
        p_username=None,
        username=USERNAME2,
        firstname="admin",
        lastname="user",
        email="admin@admin.com",
        password="Admin-12",
        user_type="admin",
        user_role=None,
        user_environments=None
    )


    output = "User {} added\n".format(USERNAME2)

    captured = capsys.readouterr()


    assert (rc, captured.out.replace("\r","")) == (0, output)


def test_admin_list(capsys):
    rc = user_worker.user_list(
        p_engine="test_eng",
        p_username=None,
        format="csv",
        username = USERNAME2
    )



    output = "\n#Engine name,User name,First name,Last name,E-mail,Auth type,Principal,Role name,Locked,Environment list\n" + \
             "test_eng,{},admin,user,admin@admin.com,NATIVE,,Administrator,Open,\n\n\n".format(USERNAME2)

    captured = capsys.readouterr()

    assert (rc, captured.out.replace('\r','')) == (0, output)

def test_admin_update_to_nonadmin(capsys):
    rc = user_worker.user_update(
        p_engine="test_eng",
        p_username=None,
        username = USERNAME2,
        user_role='DBA',
        user_environments='env1',
        firstname=None,
        lastname=None,
        email=None,
        password=None,
        user_type='nonadmin'
    )

    output = "User {} updated\n".format(USERNAME2)

    captured = capsys.readouterr()
    assert (rc, captured.out.replace("\r","")) == (0, output)


def test_nonadmin_list_with_update(capsys):
    rc = user_worker.user_list(
        p_engine="test_eng",
        p_username=None,
        format="csv",
        username = USERNAME2
    )



    output = "\n#Engine name,User name,First name,Last name,E-mail,Auth type,Principal,Role name,Locked,Environment list\n" + \
             "test_eng,{},admin,user,admin@admin.com,NATIVE,,DBA,Open,env1\n\n\n".format(USERNAME2)

    captured = capsys.readouterr()

    assert (rc, captured.out.replace('\r','')) == (0, output)


def test_user_delete():
    rc = user_worker.user_delete(
        p_engine="test_eng",
        p_username=None,
        username=USERNAME1,
        force=False
    )

    assert rc == 0

def test_user2_delete():
    rc = user_worker.user_delete(
        p_engine="test_eng",
        p_username=None,
        username=USERNAME2,
        force=False
    )

    assert rc == 0