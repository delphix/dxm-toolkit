from unittest import TestCase
from unittest import main
import mock
import sys
from dxm.lib.DxLogging import logging_est
from masking_apis.apis.environment_api import EnvironmentApi
from masking_apis.apis.database_ruleset_api import DatabaseRulesetApi
from masking_apis.apis.file_ruleset_api import FileRulesetApi
from masking_apis.apis.database_connector_api import DatabaseConnectorApi
from masking_apis.apis.file_connector_api import FileConnectorApi
from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from masking_apis.apis.table_metadata_api import TableMetadataApi
from masking_apis.apis.file_metadata_api import FileMetadataApi
from masking_apis.apis.file_format_api import FileFormatApi
from masking_apis.apis.column_metadata_api import ColumnMetadataApi
from masking_apis.apis.file_field_metadata_api import FileFieldMetadataApi
from dxm.lib.DxColumn.column_worker import column_list
from apis.v5.masking_apis.models.environment import Environment as env5
from apis.v5.masking_apis.models.environment_list import EnvironmentList as envlist5
from apis.v5.masking_apis.apis.environment_api import EnvironmentApi as envapi5
from masking_apis.apis.system_information_api import SystemInformationApi
from masking_apis.apis.application_api import ApplicationApi
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
    envapi5, 'get_all_environments', new=env_load
)
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
            'Column name,Type,Data type,Domain name,Alg name\r\ntesteng,Env1,DB Ruleset1,EMP,'
            'ENAME,FK,VARCHAR2(30),LAST_NAME,LastNameLookup\r\ntesteng,Env1,DB Ruleset1,DEPT,'
            'DNAME,IX,VARCHAR2(66),TEST_NAME,TestNameLookup\r\ntesteng,Env1,File Ruleset1,FILE,Col1,,pos 1,,'
        )


if __name__ == '__main__':
    logging_est('test.log', True)
    main(buffer=True, verbosity=2)
