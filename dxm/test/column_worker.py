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
from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
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
from masking_apis.apis.file_field_metadata_api import FileFieldMetadataApi
from masking_apis.models.file_field_metadata_list import FileFieldMetadataList
from dxm.lib.DxColumn.column_worker import column_list

from masking_apis.models.file_field_metadata import FileFieldMetadata


def createtable(a, b, **kwargs):
    b.table_metadata_id = b.table_metadata_id + b.ruleset_id
    return b

def retok(*args, **kwargs):
    return None

def filefieldmeta_load(a, **kwargs):
    """
    Create an output for get_all_column_metadata call
    """
    pi = PageInfo(number_on_page=1, total=1)

    if kwargs.get('file_format_id') == 1:
        columnforfile = [
            FileFieldMetadata(
                field_name="Col1",
                field_position_number=1
                )
        ]

    clrpo = FileFieldMetadataList(page_info=pi, response_list=columnforfile)
    return clrpo

def meta_load(a, **kwargs):
    """
    Create an output for get_all_column_metadata call
    """
    pi = PageInfo(number_on_page=2, total=2)

    if kwargs.get('table_metadata_id') == 1:
        columnfortable = [ColumnMetadata(
                            column_metadata_id=1, table_metadata_id=1,
                            column_name="ENAME", is_masked=True,
                            data_type="VARCHAR2", column_length=30,
                            is_foreign_key=True,
                            algorithm_name="LastNameLookup",
                            domain_name="LAST_NAME")]
    elif kwargs.get('table_metadata_id') == 2:
        columnfortable = [ColumnMetadata(
                            column_metadata_id=1, table_metadata_id=2,
                            column_name="DNAME", is_masked=True,
                            data_type="VARCHAR2", column_length=66,
                            is_index=True,
                            algorithm_name="TestNameLookup",
                            domain_name="TEST_NAME")]
    elif kwargs.get('table_metadata_id') == 101:
        columnfortable = [ColumnMetadata(
                            column_metadata_id=1, table_metadata_id=101,
                            data_type="VARCHAR2", column_length=30,
                            column_name="ENAME", is_masked=False)]
    elif kwargs.get('table_metadata_id') == 102:
        columnfortable = [ColumnMetadata(
                            column_metadata_id=1, table_metadata_id=102,
                            data_type="VARCHAR2", column_length=66,
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

    if kwargs.get('ruleset_id') == 2:
        pi = PageInfo(number_on_page=1, total=1)
        files = [FileMetadata(
                            file_metadata_id=2,
                            file_format_id=1,
                            file_name="FILE",
                            ruleset_id=2)]
        filesrpo = FileMetadataList(page_info=pi, response_list=files)
    else:
        pi = PageInfo(number_on_page=0, total=0)
        filesrpo = FileMetadataList(page_info=pi, response_list=[])

    return filesrpo

def tablemeta_load(a, **kwargs):
    """
    Create an output for get_all_table_metadata call
    """

    if kwargs.get('ruleset_id') == 1:
        pi = PageInfo(number_on_page=2, total=2)
        tables = [
            TableMetadata(table_metadata_id=1, table_name="EMP", ruleset_id=1),
            TableMetadata(table_metadata_id=2, table_name="DEPT", ruleset_id=1)]
        tablesrpo = TableMetadataList(page_info=pi, response_list=tables)
    else:
        pi = PageInfo(number_on_page=0, total=0)
        tablesrpo = TableMetadataList(page_info=pi, response_list=[])

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
@mock.patch.object(
    FileFieldMetadataApi, 'get_all_file_field_metadata', new=filefieldmeta_load
)
class TestRuleset(TestCase):
    def test_column_list(self, get_session):
        column_list(None, "csv", None, None, None, None, None, None, None)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")

        output = sys.stdout.getvalue().strip()
        self.assertEquals(
            output, '#Engine name,Environment name,Ruleset name,Metadata name,'
            'Column name,Type,Data type,Domain name,Alg name\r\n53,Env1,DB Ruleset1,EMP,'
            'ENAME,FK,VARCHAR2(30),LAST_NAME,LastNameLookup\r\n53,Env1,DB Ruleset1,DEPT,'
            'DNAME,IX,VARCHAR2(66),TEST_NAME,TestNameLookup\r\n53,Env1,File Ruleset1,FILE,Col1,,pos 1,,'
        )


if __name__ == '__main__':
    logging_est('test.log', True)
    main(buffer=True, verbosity=2)
