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
from masking_apis.models.file_connector import FileConnector
from masking_apis.models.database_connector_list import DatabaseConnectorList
from masking_apis.apis.database_connector_api import DatabaseConnectorApi
from masking_apis.models.file_connector_list import FileConnectorList
from masking_apis.apis.file_connector_api import FileConnectorApi
from masking_apis.models.page_info import PageInfo
from dxm.lib.DxJobs.DxJobsList import DxJobsList
from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from dxm.lib.DxConnector.conn_worker import connector_list
from dxm.lib.DxConnector.conn_worker import connector_add



def dbconnector_load(a, **kwargs):
    """
    Create an output for get_all_database_connectors call
    """
    pi = PageInfo(number_on_page=2, total=2)
    dbconnector = [
        DatabaseConnector(database_connector_id=1, connector_name="DB connector", environment_id=1, database_type="ORACLE"),
        DatabaseConnector(database_connector_id=2, connector_name="DB connector2", environment_id=1, database_type="SYBASE")
        ]
    dbconnector1 = []
    dbcpo = DatabaseConnectorList(page_info=pi, response_list=dbconnector)
    return dbcpo


def fileconnector_load(a, **kwargs):
    """
    Create an output for get_all_file_connectors call
    """
    pi = PageInfo(number_on_page=0, total=0)
    fileconnector = [FileConnector(file_connector_id=1, connector_name="File connector", environment_id=1, file_type="DELIMITED")]
    filerpo = FileConnectorList(page_info=pi, response_list=fileconnector)
    return filerpo


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
    EnvironmentApi, 'get_all_environments', new=env_load
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
            ',ORACLE\r\ntesteng,Env1,DB connector2'
            ',SYBASE\r\ntesteng,Env1,File connector,DELIMITED'
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
                    'type': 'oracle'
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
