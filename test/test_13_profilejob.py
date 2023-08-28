import pytest
import os
from dxm.lib.DxJobs import jobs_worker
from dxm.lib.DxColumn import column_worker
from dxm.lib.DxEngine.DxConfig import DxConfig
from dxm.lib.DxLogging import logging_est


CONFIGPATH='./test/testdb.db'
ALGNAME1="dlpx-core:FirstName"
RULESETNAME="rs_test_1"
ENVNAME="env1"
JOBNAME="profjob1"
PROFILESET="Standard"


#logging_est('dxm.log', True)

@pytest.fixture(autouse=True)
def open_config_file():
    DxConfig(CONFIGPATH)



@pytest.mark.dependency()
def test_profjob_list_ignore(capsys):
    rc = jobs_worker.profilejobs_list(
        p_engine="test_eng",
        p_username=None,
        p_format="csv",
        envname=ENVNAME,
        jobname=JOBNAME
    )

    if rc == 1:
        pytest.skip("Job non-exist")
    else:
        assert True

    


@pytest.mark.dependency(depends=['test_profjob_list_ignore'])
def test_profjob_delete_old_job():
    rc = jobs_worker.profilejob_delete(
        p_engine="test_eng",
        p_username=None,
        envname=ENVNAME,
        jobname=JOBNAME
    )

    assert rc == 0


def test_add_profjob_single(capsys):

    params = {
        "envname": ENVNAME,
        "jobname": JOBNAME,
        "rulesetname": RULESETNAME,
        "profilename": PROFILESET,
        "email": None,
        "feedback_size": None,
        "max_memory": None,
        "min_memory": None,
        "job_description": None,
        "num_input_streams": None,
        "multi_tenant": None
    }


    rc = jobs_worker.profilejob_add(
        p_engine="test_eng",
        p_username=None,
        params = params
    )


    output = "Profile job {} added\n".format(JOBNAME)

    captured = capsys.readouterr()


    assert (rc, captured.out.replace("\r","")) == (0, output)



def test_job_list(capsys):
    rc = jobs_worker.profilejobs_list(
        p_engine="test_eng",
        p_username=None,
        p_format="csv",
        envname=ENVNAME,
        jobname=JOBNAME
    )


    assert rc == 0



def test_start_job_single(capsys):

    job_list = [ JOBNAME ]
        
    rc = jobs_worker.profilejob_start(
        p_engine="test_eng",
        p_username=None,
        jobname = job_list,
        envname = None,
        tgt_connector = None,
        tgt_connector_env = None,
        nowait = None,
        monitor= None,
        parallel= 1
    )


    output = "Waiting for profilejob profjob1 to finish\n" + \
             "Profile job {} finished.".format(JOBNAME) + \
             "\n\n\n\n"

    captured = capsys.readouterr()


    assert (rc, captured.out.replace("\r","")) == (0, output)


def test_job_report_single(capsys):

    rc = jobs_worker.profilejobs_report(
        p_engine="test_eng",
        p_username=None,
        p_format="csv",
        envname=ENVNAME,
        jobname=JOBNAME,
        last=False,
        startdate=None,
        enddate=None,
        details=False
    )

    output = "\n#Engine name,Environment name,Job name,Ruleset Type,ExecId,Started,Completed,Status,Runtime\n" + \
             "test_eng,env1,{},Database,SUCCEEDED\n\n".format(JOBNAME)

    captured = capsys.readouterr()


    output_from_command = []

    for line in captured.out.splitlines():
        if "test_eng" in line:
            line_list = line.split(',')
            output_from_command.append(",".join(line_list[0:4])+','+line_list[7])
        else:
            output_from_command.append(line.replace("\r",""))


    assert (rc, "\n".join(output_from_command)) == (0, output)
