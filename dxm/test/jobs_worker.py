from unittest import TestCase
from unittest import main
import mock
import sys

from dxm.lib.DxLogging import logging_est
from masking_api_60.api.masking_job_api import MaskingJobApi
from masking_api_60.models.masking_job import MaskingJob
from masking_api_60.models.masking_job_list import MaskingJobList
from masking_api_60.models.environment import Environment
from masking_api_60.models.environment_list import EnvironmentList
from apis.v5.masking_api_60.models.environment import Environment as env5
from apis.v5.masking_api_60.models.environment_list import EnvironmentList as envlist5
from apis.v5.masking_api_60.api.environment_api import EnvironmentApi as envapi5
from masking_api_60.api.application_api import ApplicationApi
from masking_api_60.api.environment_api import EnvironmentApi
from masking_api_60.models.execution import Execution
from masking_api_60.models.execution_list import ExecutionList
from masking_api_60.api.execution_api import ExecutionApi
from masking_api_60.models.database_ruleset import DatabaseRuleset
from masking_api_60.models.database_ruleset_list import DatabaseRulesetList
from masking_api_60.api.database_ruleset_api import DatabaseRulesetApi
from masking_api_60.api.file_ruleset_api import FileRulesetApi
from masking_api_60.models.file_ruleset_list import FileRulesetList
from masking_api_60.models.database_connector import DatabaseConnector
from masking_api_60.models.database_connector_list import DatabaseConnectorList
from masking_api_60.api.database_connector_api import DatabaseConnectorApi
from masking_api_60.models.file_connector_list import FileConnectorList
from masking_api_60.api.file_connector_api import FileConnectorApi
from masking_api_60.api.system_information_api import SystemInformationApi
from masking_api_60.models.page_info import PageInfo
from dxm.lib.DxJobs.DxJobsList import DxJobsList
from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from dxm.lib.DxJobs.jobs_worker import jobs_list
from dxm.lib.DxJobs.jobs_worker import job_start

from engine import app_load
from engine import env_load
from engine import dbruleset_load
from engine import fileruleset_load
from engine import dbconnector_load
from engine import fileconnector_load
from engine import execution_load
from engine import job_load
from engine import sysinfo_load

@mock.patch.object(
    DxMaskingEngine, 'get_session', return_value=None
)
@mock.patch.object(
   MaskingJobApi, 'get_all_masking_jobs', new=job_load
)
@mock.patch.object(
    SystemInformationApi, 'get_system_information', new=sysinfo_load
)
@mock.patch.object(
    ApplicationApi, 'get_all_applications', new=app_load
)
@mock.patch.object(
    EnvironmentApi, 'get_all_environments', new=env_load
)
@mock.patch.object(
    envapi5, 'get_all_environments', new=env_load
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
    def test_job_list(self, aaa):
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
