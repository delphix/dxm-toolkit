from unittest import TestCase
from unittest import main
import mock
import sys
import datetime
from dxm.lib.DxLogging import logging_est
from masking_api_60.api.masking_job_api import MaskingJobApi
from masking_api_60.models.masking_job import MaskingJob
from masking_api_60.models.masking_job_list import MaskingJobList
from masking_api_60.models.environment import Environment
from masking_api_60.models.environment_list import EnvironmentList
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
from masking_api_60.models.file_connector import FileConnector
from masking_api_60.models.database_connector_list import DatabaseConnectorList
from masking_api_60.api.database_connector_api import DatabaseConnectorApi
from masking_api_60.models.file_connector_list import FileConnectorList
from masking_api_60.api.file_connector_api import FileConnectorApi
from masking_api_60.models.page_info import PageInfo
from dxm.lib.DxJobs.DxJobsList import DxJobsList
from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from dxm.lib.DxConnector.conn_worker import connector_list
from dxm.lib.DxConnector.conn_worker import connector_add
from apis.v5.masking_api_60.models.environment import Environment as env5
from apis.v5.masking_api_60.models.environment_list import EnvironmentList as envlist5
from apis.v5.masking_api_60.api.environment_api import EnvironmentApi as envapi5
from masking_api_60.api.system_information_api import SystemInformationApi
from masking_api_60.api.application_api import ApplicationApi
from engine import env_load
from engine import dbruleset_load
from engine import fileruleset_load
from engine import dbconnector_load
from engine import fileconnector_load
from engine import tablemeta_load
from engine import filemeta_load
from engine import retok
from engine import meta_load
from engine import filefieldmeta_load
from engine import fileformat_load
from engine import app_load
from engine import sysinfo_load




@mock.patch.object(
    SystemInformationApi, 'get_system_information', new=sysinfo_load
)
@mock.patch.object(
    ApplicationApi, 'get_all_applications', new=app_load
)
@mock.patch.object(
    DxMaskingEngine, 'get_session', return_value=None)
@mock.patch.object(
    EnvironmentApi, 'get_all_environments', new=env_load
)
@mock.patch.object(
    envapi5, 'get_all_environments', new=env_load
)
@mock.patch.object(
    DatabaseConnectorApi, 'get_all_database_connectors', new=dbconnector_load
)
@mock.patch.object(
    FileConnectorApi, 'get_all_file_connectors', new=fileconnector_load
)
class TestConnector(TestCase):
    def test_connector_listselect(self, get_session):
        connector_list(None, "csv", None, "DB connector", None)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")

        output = sys.stdout.getvalue().strip()
        self.assertEquals(
            output, '#Engine name,Environment name,Connector name,Connector '
            'type\r\ntesteng,Env1,DB connector'
            ',ORACLE'
        )

    def test_connector_list(self, get_session):
        connector_list(None, "csv", None, None, None)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")

        output = sys.stdout.getvalue().strip()
        self.assertEquals(
            output, '#Engine name,Environment name,Connector name,Connector '
            'type\r\ntesteng,Env1,DB connector'
            ',ORACLE\r\ntesteng,Env1,File connector,DELIMITED'
        )

    def test_connector_add(self, get_session):

        dbresposne = DatabaseConnector(
                        database_connector_id=1,
                        connector_name="DB connector",
                        environment_id=1,
                        database_type="ORACLE")
        with mock.patch.object(
                DatabaseConnectorApi, 'create_database_connector',
                return_value=dbresposne) as mock_method:

                params = {
                    'envname': 'Env1',
                    'schemaName': 'SCOTT',
                    'host': '10.10.10.10',
                    'port': 1521,
                    'password': 'TIGER',
                    'username': 'SCOTT',
                    'connname': 'DB new',
                    'sid': 'ORCL',
                    'type': 'oracle',
                    'jdbc': None,
                    'instancename': None,
                    'databasename': None
                }

                ret = connector_add(None, params)
                name, args, kwargs = mock_method.mock_calls[0]
                print args[0]
                self.assertEqual(1, args[0].environment_id)
                self.assertEqual(1521, args[0].port)
                self.assertEqual(0, ret)

if __name__ == '__main__':
    logging_est('test.log', False)
    main(buffer=True, verbosity=2)
