import datetime
from apis.v5.masking_apis.models.page_info import PageInfo
from apis.v5.masking_apis.models.application import Application
from apis.v5.masking_apis.models.application_list import ApplicationList
from apis.v5.masking_apis.models.environment import Environment
from apis.v5.masking_apis.models.environment_list import EnvironmentList
from apis.v5.masking_apis.models.file_field_metadata import FileFieldMetadata
from apis.v5.masking_apis.models.file_format import FileFormat
from apis.v5.masking_apis.models.file_format_list import FileFormatList
from masking_apis.models.column_metadata import ColumnMetadata
from masking_apis.models.column_metadata_list import ColumnMetadataList
from apis.v5.masking_apis.models.file_field_metadata_list import FileFieldMetadataList
from apis.v5.masking_apis.models.file_metadata import FileMetadata
from apis.v5.masking_apis.models.file_metadata_list import FileMetadataList
from apis.v5.masking_apis.models.table_metadata import TableMetadata
from apis.v5.masking_apis.models.table_metadata_list import TableMetadataList
from apis.v5.masking_apis.models.file_connector_list import FileConnectorList
from apis.v5.masking_apis.models.file_ruleset_list import FileRulesetList
from apis.v5.masking_apis.models.database_connector import DatabaseConnector
from apis.v5.masking_apis.models.file_connector import FileConnector
from apis.v5.masking_apis.models.database_connector_list import DatabaseConnectorList
from apis.v5.masking_apis.models.execution import Execution
from apis.v5.masking_apis.models.execution_list import ExecutionList
from apis.v5.masking_apis.apis.execution_api import ExecutionApi
from apis.v5.masking_apis.models.database_ruleset import DatabaseRuleset
from apis.v5.masking_apis.models.file_ruleset import FileRuleset
from apis.v5.masking_apis.models.database_ruleset_list import DatabaseRulesetList
from apis.v5.masking_apis.apis.masking_job_api import MaskingJobApi
from apis.v5.masking_apis.models.masking_job import MaskingJob
from apis.v5.masking_apis.models.masking_job_list import MaskingJobList
from apis.v5.masking_apis.models.environment import Environment
from apis.v5.masking_apis.models.environment_list import EnvironmentList
from apis.v5.masking_apis.models.domain import Domain
from apis.v5.masking_apis.models.domain_list import DomainList
from apis.v5.masking_apis.models.system_information import SystemInformation


def sysinfo_load(a, **kwargs):
    """
    Create an output for get_system_information call
    """
    return SystemInformation(version="5.3.0.0")

def app_load(a, **kwargs):
    """
    Create an output for get_all_application call
    """
    pi = PageInfo(number_on_page=2, total=2)
    applist = [Application(application_name="App1"), Application(application_name="App2"), Application(application_name="App3")]
    apo = ApplicationList(page_info=pi, response_list=applist)
    return apo

def env_load(a, **kwargs):
    """
    Create an output for get_all_environments call
    """
    pi = PageInfo(number_on_page=2, total=2)
    envlist = [Environment(environment_id=1, environment_name="Env1", application="App1", purpose="MASK")]
    epo = EnvironmentList(page_info=pi, response_list=envlist)
    return epo

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

def domain_load(a, **kwargs):
    """
    Create an output for get_all_file_formats call
    """
    pi = PageInfo(number_on_page=2, total=2)
    ff = [
            Domain(domain_name="DOMAIN1", classification="CUSTOMER", default_algorithm_code="ALG"),
            Domain(domain_name="DOMAIN2", classification="CUSTOMER", default_algorithm_code="ALG")
         ]
    ffrpo = DomainList(page_info=pi, response_list=ff)
    return ffrpo