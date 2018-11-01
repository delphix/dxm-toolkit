from unittest import TestCase
from unittest import main
from mock import call
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
from masking_apis.models.file_ruleset import FileRuleset
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
from dxm.lib.DxRuleset.rule_worker import ruleset_list
from dxm.lib.DxRuleset.rule_worker import ruleset_listmeta
from dxm.lib.DxRuleset.rule_worker import ruleset_addmeta
from dxm.lib.DxRuleset.rule_worker import ruleset_deletemeta
from dxm.lib.DxRuleset.rule_worker import ruleset_add
from dxm.lib.DxRuleset.rule_worker import ruleset_delete
from dxm.lib.DxRuleset.rule_worker import ruleset_clone
from masking_apis.models.table_metadata import TableMetadata
from masking_apis.models.table_metadata_list import TableMetadataList
from masking_apis.apis.table_metadata_api import TableMetadataApi
from masking_apis.apis.file_metadata_api import FileMetadataApi
from masking_apis.models.file_metadata import FileMetadata
from masking_apis.models.file_metadata_list import FileMetadataList
from masking_apis.apis.file_format_api import FileFormatApi
from masking_apis.models.file_format import FileFormat
from masking_apis.models.file_format_list import FileFormatList
from masking_apis.models.column_metadata import ColumnMetadata
from masking_apis.models.column_metadata_list import ColumnMetadataList
from masking_apis.apis.column_metadata_api import ColumnMetadataApi

def createtable(a, b, **kwargs):
    b.table_metadata_id =b.table_metadata_id + b.ruleset_id
    return b

def retok(*args, **kwargs):
    return None

def meta_load(a, **kwargs):
    """
    Create an output for get_all_column_metadata call
    """
    pi = PageInfo(number_on_page=2, total=2)
    if kwargs.get('table_metadata_id') == 1:
        columnfortable = [ColumnMetadata(
                            column_metadata_id=1, table_metadata_id=1,
                            column_name="ENAME", is_masked=True,
                            algorithm_name="LastNameLookup",
                            domain_name="LAST_NAME")]
    elif kwargs.get('table_metadata_id') == 2:
        columnfortable = [ColumnMetadata(
                            column_metadata_id=1, table_metadata_id=2,
                            column_name="DNAME", is_masked=True,
                            algorithm_name="TestNameLookup",
                            domain_name="TEST_NAME")]
    elif kwargs.get('table_metadata_id') == 101:
        columnfortable = [ColumnMetadata(
                            column_metadata_id=1, table_metadata_id=101,
                            column_name="ENAME", is_masked=False)]
    elif kwargs.get('table_metadata_id') == 102:
        columnfortable = [ColumnMetadata(
                            column_metadata_id=1, table_metadata_id=102,
                            column_name="DNAME", is_masked=False)]
    clrpo = ColumnMetadataList(page_info=pi, response_list=columnfortable)
    return clrpo

def fileformat_load(a, **kwargs):
    """
    Create an output for get_all_file_formats call
    """
    pi = PageInfo(number_on_page=2, total=2)
    ff = [FileFormat(file_format_id=1, file_format_name="testformat", file_format_type="DELIMITED")]
    ffrpo = FileFormatList(page_info=pi, response_list=ff)
    return ffrpo

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
    pi = PageInfo(number_on_page=1, total=1)
    fileconnector = [FileConnector(file_connector_id=1, connector_name="File connector", environment_id=1, file_type="DELIMITED")]
    filerpo = FileConnectorList(page_info=pi, response_list=fileconnector)
    return filerpo


def fileruleset_load(a, **kwargs):
    """
    Create an output for get_all_file_rulesets call
    """
    pi = PageInfo(number_on_page=1, total=1)
    fileruleset = [FileRuleset(file_ruleset_id=2, ruleset_name="File Ruleset1", file_connector_id=1)]
    filerpo = FileRulesetList(page_info=pi, response_list=fileruleset)
    return filerpo


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
@mock.patch.object(
    TableMetadataApi, 'delete_table_metadata', new=retok
)
@mock.patch.object(
    FileFormatApi, 'get_all_file_formats', new=fileformat_load
)
@mock.patch.object(
    DatabaseRulesetApi, 'delete_database_ruleset', new=retok
)
@mock.patch.object(
    ColumnMetadataApi, 'get_all_column_metadata', new=meta_load
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

    def test_ruleset_addmeta(self, get_session):
        params = {
            "rulesetname": 'DB Ruleset1',
            "metaname": 'TESTTABLE',
            "custom_sql": None,
            "where_clause": 'id>1000',
            "having_clause": None,
            "key_column": None,
            "file_format": None,
            "file_delimiter": None,
            "file_eor": None,
            "file_enclosure": None,
            "file_name_regex": None,
            "file_eor_custom": None,
            "envname": 'Env1'
        }
        with mock.patch.object(
                TableMetadataApi, 'create_table_metadata',
                return_value=TableMetadata(
                    table_metadata_id=123,
                    table_name="TESTTABLE",
                    ruleset_id=1)) as mock_method:
            ret = ruleset_addmeta(None, params, None)
            name, args, kwargs = mock_method.mock_calls[0]
            print args[0]
            self.assertEqual("TESTTABLE", args[0].table_name)
            self.assertEqual("id>1000", args[0].where_clause)
            self.assertEqual(1, args[0].ruleset_id)
            self.assertEqual(0, ret)

    def test_ruleset_deletemeta(self, get_session):
        ret = ruleset_deletemeta(None, 'DB Ruleset1', 'DEPT', 'Env1')
        self.assertEqual(0, ret)

    def test_ruleset_addmeta_file(self, get_session):
        params = {
            "rulesetname": 'File Ruleset1',
            "metaname": 'TESTFILE',
            "custom_sql": None,
            "where_clause": None,
            "having_clause": None,
            "key_column": None,
            "file_format": 'testformat',
            "file_delimiter": ',',
            "file_eor": 'linux',
            "file_enclosure": '"',
            "file_name_regex": None,
            "file_eor_custom": None,
            "envname": 'Env1'
        }
        with mock.patch.object(
                FileMetadataApi, 'create_file_metadata',
                return_value=FileMetadata(
                    file_metadata_id=124,
                    file_name="TESTFILE",
                    ruleset_id=1)) as mock_method:
            ret = ruleset_addmeta(None, params, None)
            name, args, kwargs = mock_method.mock_calls[0]
            print args[0]
            self.assertEqual("TESTFILE", args[0].file_name)
            self.assertEqual(1, args[0].file_format_id)
            self.assertEqual(2, args[0].ruleset_id)
            self.assertEqual('\n', args[0].end_of_record)
            self.assertEqual(0, ret)

    def test_ruleset_add(self, get_session):
        with mock.patch.object(
                DatabaseRulesetApi, 'create_database_ruleset',
                return_value=DatabaseRuleset(
                    database_ruleset_id=123,
                    ruleset_name="newdbrule",
                    )) as mock_method:
            ret = ruleset_add(None, "newdbrule", "DB connector", "Env1")
            name, args, kwargs = mock_method.mock_calls[0]
            print args[0]
            self.assertEqual(123, args[0].database_ruleset_id)
            self.assertEqual(0, ret)

    def test_ruleset_add_error(self, get_session):
        with mock.patch.object(
                DatabaseRulesetApi, 'create_database_ruleset',
                return_value=DatabaseRuleset(
                    database_ruleset_id=123,
                    ruleset_name="newdbrule",
                    )) as mock_method:
            ret = ruleset_add(None, "newdbrule", "DB conn", "Env1")
            self.assertEqual(1, ret)

    def test_ruleset_delete(self, get_session):
        ret = ruleset_delete(None, 'DB Ruleset1', None)
        self.assertEqual(0, ret)

    def test_ruleset_delete_error(self, get_session):
        ret = ruleset_delete(None, 'non exitsing', None)
        self.assertEqual(1, ret)

    def test_ruleset_clone(self, get_session):
        with mock.patch.object(
                DatabaseRulesetApi, 'create_database_ruleset',
                return_value=DatabaseRuleset(
                    database_ruleset_id=100,
                    ruleset_name="newdbrule",
                    )) as mock_ruleset, \
             mock.patch.object(
                TableMetadataApi, 'create_table_metadata',
                new=createtable), \
             mock.patch.object(
                ColumnMetadataApi, 'update_column_metadata',
                return_value=None) as mock_column:
            ret = ruleset_clone(None, 'DB Ruleset1', None, "New ruleset")
            name, args, kwargs = mock_ruleset.mock_calls[0]
            print args
            self.assertEqual(100, args[0].database_ruleset_id)
            name, args, kwargs = mock_column.mock_calls[0]
            print args
            self.assertEqual(args[1].table_metadata_id, 101)
            self.assertEqual(args[1].column_metadata_id, 1)
            self.assertEqual(args[1].algorithm_name, "LastNameLookup")
            name, args, kwargs = mock_column.mock_calls[1]
            print args
            self.assertEqual(args[1].table_metadata_id, 102)
            self.assertEqual(args[1].column_metadata_id, 1)
            self.assertEqual(args[1].algorithm_name, "TestNameLookup")
            self.assertEqual(0, ret)



if __name__ == '__main__':
    logging_est('test.log', False)
    main(buffer=True, verbosity=2)
