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
from dxm.lib.DxRuleset.rule_worker import ruleset_list
from dxm.lib.DxRuleset.rule_worker import ruleset_listmeta
from masking_apis.models.table_metadata import TableMetadata
from masking_apis.models.table_metadata_list import TableMetadataList
from masking_apis.apis.table_metadata_api import TableMetadataApi
from masking_apis.apis.file_metadata_api import FileMetadataApi
from masking_apis.models.file_metadata import FileMetadata
from masking_apis.models.file_metadata_list import FileMetadataList

def filemeta_load(a, **kwargs):
    """
    Create an output for get_all_file_metadata call
    """
    pi = PageInfo(number_on_page=2, total=2)
    # files = [FileMetadata(file_metadata_id=2, file_name="FILE", ruleset_id=2)]
    filesrpo = FileMetadataList(page_info=pi, response_list=[])
    return filesrpo

def tablemeta_load(a, **kwargs):
    """
    Create an output for get_all_table_metadata call
    """
    pi = PageInfo(number_on_page=2, total=2)
    tables = [
        TableMetadata(table_metadata_id=1, table_name="EMP", ruleset_id=1),
        TableMetadata(table_metadata_id=2, table_name="DEPT", ruleset_id=1)]
    tablesrpo = TableMetadataList(page_info=pi, response_list=tables)
    return tablesrpo

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
    TableMetadataApi, 'get_all_table_metadata', new=tablemeta_load
)
@mock.patch.object(
    FileMetadataApi, 'get_all_file_metadata', new=filemeta_load
)
class TestRuleset(TestCase):
    def test_ruleset_list(self, get_session):
        ruleset_list(None, "csv", "DB Ruleset1", None)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")

        output = sys.stdout.getvalue().strip()
        self.assertEquals(
            output, '#Engine name,Ruleset name,Connector name,Metadata type,'
            'Connector type,Environent name\r\ntesteng,DB Ruleset1,DB connector'
            ',Database,ORACLE,Env1'
        )

    def test_ruleset_listmeta(self, get_session):
        ruleset_listmeta(None, "csv", "DB Ruleset1", None, None)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")

        output = sys.stdout.getvalue().strip()
        self.assertEquals(
            output, '#Engine name,Environent name,Ruleset name,Metadata type,'
            'Metadata name\r\ntesteng,Env1,DB Ruleset1,'
            'Database,EMP\r\ntesteng,Env1,DB Ruleset1,'
            'Database,DEPT'
        )

    def test_ruleset_listmeta_by_name(self, get_session):
        ruleset_listmeta(None, "csv", "DB Ruleset1", None, 'EMP')
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")

        output = sys.stdout.getvalue().strip()
        self.assertEquals(
            output, '#Engine name,Environent name,Ruleset name,Metadata type,'
            'Metadata name\r\ntesteng,Env1,DB Ruleset1,'
            'Database,EMP'
        )


if __name__ == '__main__':
    logging_est('test.log', False)
    main(buffer=True, verbosity=2)
