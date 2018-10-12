from unittest import TestCase
from unittest import main
import mock
import sys
import datetime
from dxm.lib.DxLogging import logging_est
from masking_apis.apis.masking_job_api import MaskingJobApi
from masking_apis.models.masking_job import MaskingJob
from masking_apis.models.masking_job_list import MaskingJobList
from masking_apis.models.environment import Environment
from masking_apis.models.environment_list import EnvironmentList
from masking_apis.apis.environment_api import EnvironmentApi
from masking_apis.models.execution import Execution
from masking_apis.models.execution_list import ExecutionList
from masking_apis.apis.execution_api import ExecutionApi
from masking_apis.models.database_ruleset import DatabaseRuleset
from masking_apis.models.database_ruleset_list import DatabaseRulesetList
from masking_apis.apis.database_ruleset_api import DatabaseRulesetApi
from masking_apis.apis.file_ruleset_api import FileRulesetApi
from masking_apis.models.file_ruleset_list import FileRulesetList
from masking_apis.models.database_connector import DatabaseConnector
from masking_apis.models.database_connector_list import DatabaseConnectorList
from masking_apis.apis.database_connector_api import DatabaseConnectorApi
from masking_apis.models.file_connector_list import FileConnectorList
from masking_apis.apis.file_connector_api import FileConnectorApi
from masking_apis.models.page_info import PageInfo
from dxm.lib.DxJobs.DxJobsList import DxJobsList
from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from dxm.lib.DxJobs.jobs_worker import jobs_list
from dxm.lib.DxJobs.jobs_worker import job_start

def dbconnector_load(a, **kwargs):
    """
    Create an output for get_all_database_connectors call
    """
    pi = PageInfo(number_on_page=2, total=2)
    dbconnector = [DatabaseConnector(database_connector_id=1, connector_name="DB connector", environment_id=1, database_type="ORACLE")]
    dbcpo = DatabaseConnectorList(page_info=pi, response_list=dbconnector)
    return dbcpo

def fileconnector_load(a, **kwargs):
    """
    Create an output for get_all_file_connectors call
    """
    pi = PageInfo(number_on_page=0, total=0)
    dbrpo = FileConnectorList(page_info=pi, response_list=[])
    return dbrpo

def fileruleset_load(a, **kwargs):
    """
    Create an output for get_all_file_rulesets call
    """
    pi = PageInfo(number_on_page=0, total=0)
    dbrpo = FileRulesetList(page_info=pi, response_list=[])
    return dbrpo

def dbruleset_load(a, **kwargs):
    """
    Create an output for get_all_database_rulesets call
    """
    pi = PageInfo(number_on_page=2, total=2)
    dbruleset = [DatabaseRuleset(database_ruleset_id=1, ruleset_name="DB Ruleset1", database_connector_id=1)]
    dbrpo = DatabaseRulesetList(page_info=pi, response_list=dbruleset)
    return dbrpo

def job_load(a, **kwargs):
    """
    Create an output for get_all_application call
    """
    pi = PageInfo(number_on_page=2, total=2)
    joblist = [MaskingJob(masking_job_id=1, job_name="Job1", ruleset_id=1, created_by="delphix_admin", email="test@delphix.com")]
    jpo = MaskingJobList(page_info=pi, response_list=joblist)
    return jpo

def execution_load(a, **kwargs):
    """
    Create an output for get_all_executions call
    """
    pi = PageInfo(number_on_page=2, total=2)
    execlist = [Execution(execution_id=1, job_id=1, status="SUCCEEDED", rows_masked=10, rows_total=10,
                          start_time=datetime.datetime(2018, 9, 01, 01, 00, 00),
                          end_time=datetime.datetime(2018, 9, 01, 01, 10, 00))]
    epo = ExecutionList(page_info=pi, response_list=execlist)
    return epo

def env_load(a, **kwargs):
    """
    Create an output for get_all_environments call
    """
    pi = PageInfo(number_on_page=2, total=2)
    envlist = [Environment(environment_id=1, environment_name="Env1", application="App1", purpose="MASK")]
    epo = EnvironmentList(page_info=pi, response_list=envlist)
    return epo


@mock.patch.object(
    DxMaskingEngine, 'get_session', return_value=None)
@mock.patch.object(
   MaskingJobApi, 'get_all_masking_jobs', new=job_load
)
@mock.patch.object(
    EnvironmentApi, 'get_all_environments', new=env_load
)
@mock.patch.object(
    DatabaseRulesetApi, 'get_all_database_rulesets', new=dbruleset_load
)
@mock.patch.object(
    FileRulesetApi, 'get_all_file_rulesets', new=fileruleset_load
)
@mock.patch.object(
    DatabaseConnectorApi, 'get_all_database_connectors', new=dbconnector_load
)
@mock.patch.object(
    FileConnectorApi, 'get_all_file_connectors', new=fileconnector_load
)
@mock.patch.object(
    ExecutionApi, 'get_all_executions', new=execution_load
)
class TestApp(TestCase):
    def test_job_list(self, get_session):
        jobs_list(None, "Job1", None, "csv")
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")

        output = sys.stdout.getvalue().strip()
        self.assertEquals(
            output, '#Engine name,Job name,Ruleset name,Connector name,'
            'Environment name,Completed,Status,Runtime\r\ntesteng,Job1,'
            'DB Ruleset1,DB connector,Env1,2018-09-01 01:10:00,SUCCEEDED,'
            '0:10:00')

    def test_job_start_nowait(self, get_session):
        with mock.patch.object(
                ExecutionApi, 'create_execution',
                return_value=Execution(
                    execution_id=1, job_id=1)) as mock_method:

            job_start(None, ["Job1"], "Env1", None, None,
                      True, 1, None)
            name, args, kwargs = mock_method.mock_calls[0]
            print args[0]
            self.assertEqual(1, args[0].job_id)

    def test_job_start_wait(self, get_session):
        with mock.patch.object(
                ExecutionApi, 'create_execution',
                return_value=Execution(
                    execution_id=1,
                    status='RUNNING',
                    job_id=1)) as mock_method, \
             mock.patch.object(
                ExecutionApi, 'get_execution_by_id',
                return_value=Execution(
                    execution_id=1,
                    status='SUCCEEDED',
                    rows_masked=123,
                    job_id=1)) as mock_exec:


            job_start(None, ["Job1"], "Env1", None, None,
                      False, 1, None)
            if not hasattr(sys.stdout, "getvalue"):
                self.fail("need to run in buffered mode")

            output = sys.stdout.getvalue().strip()
            self.assertEquals(
                output, 'Waiting for job Job1 to start processing rows\n'
                'Masking job Job1 finished.\n123 rows masked')

if __name__ == '__main__':
    logging_est('test.log', False)
    main(buffer=True, verbosity=2)
