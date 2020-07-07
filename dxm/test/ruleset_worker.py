import datetime
import sys
from unittest import TestCase, main

import mock
from masking_api_60.api.column_metadata_api import ColumnMetadataApi
from masking_api_60.api.database_connector_api import DatabaseConnectorApi
from masking_api_60.api.database_ruleset_api import DatabaseRulesetApi
from masking_api_60.api.environment_api import EnvironmentApi
from masking_api_60.api.async_task_api import AsyncTaskApi
from masking_api_60.api.execution_api import ExecutionApi
from masking_api_60.api.file_connector_api import FileConnectorApi
from masking_api_60.api.file_format_api import FileFormatApi
from masking_api_60.api.file_metadata_api import FileMetadataApi
from masking_api_60.api.file_ruleset_api import FileRulesetApi
from masking_api_60.api.masking_job_api import MaskingJobApi
from masking_api_60.api.table_metadata_api import TableMetadataApi
from masking_api_60.models.database_ruleset import DatabaseRuleset
# from masking_api_60.models.page_info import PageInfo
from masking_api_60.models.table_metadata import TableMetadata
from masking_api_60.models.file_metadata import FileMetadata
from masking_api_60.models.async_task import AsyncTask
from masking_api_60.rest import ApiException
from mock import call

from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from dxm.lib.DxJobs.DxJobsList import DxJobsList
from dxm.lib.DxLogging import logging_est
from dxm.lib.DxRuleset.rule_worker import (ruleset_add, ruleset_addmeta,
                                           ruleset_clone, ruleset_delete,
                                           ruleset_deletemeta, ruleset_list,
                                           ruleset_listmeta)
from engine import (createtable, dbconnector_load, dbruleset_load, env_load,
                    execution_load, fileconnector_load, fileformat_load,
                    filemeta_load, fileruleset_load, job_load, meta_load,
                    retok, tablemeta_load)
from apis.v5.masking_api_60.models.environment import Environment as env5
from apis.v5.masking_api_60.models.environment_list import EnvironmentList as envlist5
from apis.v5.masking_api_60.api.environment_api import EnvironmentApi as envapi5
from masking_api_60.api.system_information_api import SystemInformationApi
from masking_api_60.api.application_api import ApplicationApi
from engine import app_load
from engine import sysinfo_load

def create_table_fromfetch(a, b):
    e = ApiException(status=500, reason="Test exception")
    e.body = "Test"
    raise e

def fetch_table(a, b, **kwargs):
    return ["DEPT", "EMP"]

#@mock.create_autospec
def async_return(self, a, **kwargs):
    return AsyncTask(async_task_id=1, status="SUCCEEDED")

@mock.patch.object(
    SystemInformationApi, 'get_system_information', new=sysinfo_load
)
@mock.patch.object(
    ApplicationApi, 'get_all_applications', new=app_load
)
@mock.patch.object(
    envapi5, 'get_all_environments', new=env_load
)
@mock.patch.object(
    AsyncTaskApi, 'get_async_task', new=async_return)
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
@mock.patch.object(
    DatabaseConnectorApi, 'fetch_table_metadata', new=fetch_table
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
            ret = ruleset_addmeta(None, params, None, None, False)
            name, args, kwargs = mock_method.mock_calls[0]
            print args[0]
            self.assertEqual("TESTTABLE", args[0].table_name)
            self.assertEqual("id>1000", args[0].where_clause)
            self.assertEqual(1, args[0].ruleset_id)
            self.assertEqual(0, ret)

    def test_ruleset_addmetafromfetch(self, get_session):
        params = {
            "rulesetname": 'DB Ruleset1',
            "metaname": None,
            "envname": 'Env1',
            "fetchfilter": None
        }
        with mock.patch.object(
                TableMetadataApi, 'create_table_metadata') as mock_method:
            ret = ruleset_addmeta(None, params, None, True, False)
            retval = mock_method.call_args_list
            self.assertEqual(retval[0][0][0].table_name, 'DEPT')
            self.assertEqual(retval[1][0][0].table_name, 'EMP')
            self.assertEqual(ret, 0)


    def test_ruleset_addmetafromfetch_bulk(self, get_session):
        params = {
            "rulesetname": 'DB Ruleset1',
            "metaname": None,
            "envname": 'Env1',
            "fetchfilter": None
        }

        c = {'table_metadata': [{'custom_sql': None,
                     'having_clause': None,
                     'key_column': None,
                     'ruleset_id': 1,
                     'table_metadata_id': None,
                     'table_name': 'DEPT',
                     'where_clause': None},
                    {'custom_sql': None,
                     'having_clause': None,
                     'key_column': None,
                     'ruleset_id': 1,
                     'table_metadata_id': None,
                     'table_name': 'EMP',
                     'where_clause': None}]}

        with mock.patch.object(
                DatabaseRulesetApi, 'bulk_table_update',
                return_value=AsyncTask(async_task_id=1)) as mock_method:
            ret = ruleset_addmeta(None, params, None, True, True)
            retval = mock_method.call_args_list
            self.assertDictEqual(retval[0][0][1].to_dict(), c)
            self.assertEqual(ret, 0)

    def test_ruleset_addmetafromfetch_exception(self, get_session):
        params = {
            "rulesetname": 'DB Ruleset1',
            "metaname": None,
            "envname": 'Env1',
            "fetchfilter": None
        }
        with mock.patch.object(
                TableMetadataApi, 'create_table_metadata', 
                new=create_table_fromfetch):
            ret = ruleset_addmeta(None, params, None, True, False)
            self.assertNotEqual(ret, 0)

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
            ret = ruleset_addmeta(None, params, None, None, False)
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

