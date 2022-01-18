#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright (c) 2018 by Delphix. All rights reserved.
#
# Author  : Marcin Przepiorowski
# Date    : April 2018

import click
from sys import exit
from dxm.lib.DxApplication.app_worker import application_list
from dxm.lib.DxApplication.app_worker import application_add
from dxm.lib.DxEnvironment.env_worker import environment_list
from dxm.lib.DxEnvironment.env_worker import environment_add
from dxm.lib.DxEnvironment.env_worker import environment_delete
from dxm.lib.DxConnector.conn_worker import connector_list
from dxm.lib.DxConnector.conn_worker import connector_add
from dxm.lib.DxConnector.conn_worker import connector_delete
from dxm.lib.DxConnector.conn_worker import connector_update
from dxm.lib.DxConnector.conn_worker import connector_test
from dxm.lib.DxConnector.conn_worker import connector_fetch
from dxm.lib.DxConnector.conn_worker import database_types
from dxm.lib.DxConnector.conn_worker import file_types
from dxm.lib.DxRuleset.rule_worker import ruleset_list
from dxm.lib.DxRuleset.rule_worker import ruleset_add
from dxm.lib.DxRuleset.rule_worker import ruleset_delete
from dxm.lib.DxRuleset.rule_worker import ruleset_clone
from dxm.lib.DxRuleset.rule_worker import ruleset_export
from dxm.lib.DxRuleset.rule_worker import ruleset_import
from dxm.lib.DxRuleset.rule_worker import ruleset_check
from dxm.lib.DxRuleset.rule_worker import ruleset_addmeta
from dxm.lib.DxRuleset.rule_worker import ruleset_listmeta
from dxm.lib.DxRuleset.rule_worker import ruleset_deletemeta
from dxm.lib.DxRuleset.rule_worker import ruleset_refresh
from dxm.lib.DxEngine.eng_worker import engine_add
from dxm.lib.DxEngine.eng_worker import engine_list
from dxm.lib.DxEngine.eng_worker import engine_delete
from dxm.lib.DxEngine.eng_worker import engine_update
from dxm.lib.DxEngine.eng_worker import engine_logout
from dxm.lib.DxEngine.eng_worker import engine_logs
from dxm.lib.DxEngine.eng_worker import engine_upload
from dxm.lib.DxJobs.jobs_worker import jobs_list
from dxm.lib.DxJobs.jobs_worker import job_add
from dxm.lib.DxJobs.jobs_worker import job_start
from dxm.lib.DxJobs.jobs_worker import job_delete
from dxm.lib.DxJobs.jobs_worker import job_copy
from dxm.lib.DxJobs.jobs_worker import job_update
from dxm.lib.DxJobs.jobs_worker import job_cancel
from dxm.lib.DxJobs.jobs_worker import jobs_report
from dxm.lib.DxColumn.column_worker import column_list
from dxm.lib.DxColumn.column_worker import column_setmasking
from dxm.lib.DxColumn.column_worker import column_unsetmasking
from dxm.lib.DxColumn.column_worker import column_replace
from dxm.lib.DxColumn.column_worker import column_batch
from dxm.lib.DxColumn.column_worker import column_save
from dxm.lib.DxFileFormat.fileformat_worker import fileformat_add
from dxm.lib.DxFileFormat.fileformat_worker import fileformat_list
from dxm.lib.DxFileFormat.fileformat_worker import fileformat_delete
from dxm.lib.DxAlgorithm.alg_worker import algorithm_list
from dxm.lib.DxAlgorithm.alg_worker import algorithm_export
from dxm.lib.DxAlgorithm.alg_worker import algorithm_import
from dxm.lib.DxTable.tab_worker import tab_listtable_details
from dxm.lib.DxTable.tab_worker import tab_listfile_details
from dxm.lib.DxTable.tab_worker import tab_update_meta
from dxm.lib.DxProfile.profile_worker import profile_list
from dxm.lib.DxProfile.profile_worker import expression_list
from dxm.lib.DxProfile.profile_worker import expression_add
from dxm.lib.DxProfile.profile_worker import expression_delete
from dxm.lib.DxProfile.profile_worker import expression_update
from dxm.lib.DxProfile.profile_worker import profile_add
from dxm.lib.DxProfile.profile_worker import profile_delete
from dxm.lib.DxProfile.profile_worker import profile_export
from dxm.lib.DxProfile.profile_worker import profile_addexpression
from dxm.lib.DxProfile.profile_worker import profile_deleteexpression
from dxm.lib.DxJobs.jobs_worker import profilejobs_list
from dxm.lib.DxJobs.jobs_worker import profilejob_start
from dxm.lib.DxJobs.jobs_worker import profilejob_copy
from dxm.lib.DxJobs.jobs_worker import profilejob_add
from dxm.lib.DxJobs.jobs_worker import profilejob_update
from dxm.lib.DxJobs.jobs_worker import profilejob_delete
from dxm.lib.DxJobs.jobs_worker import profilejob_cancel
from dxm.lib.DxJobs.jobs_worker import profilejobs_report
from dxm.lib.DxSync.sync_worker import sync_list
from dxm.lib.DxSync.sync_worker import sync_export
from dxm.lib.DxSync.sync_worker import sync_import
from dxm.lib.DxSync.sync_worker import supported_sync_objects_type
from dxm.lib.DxRole.role_worker import role_list
from dxm.lib.DxUser.user_worker import user_list
from dxm.lib.DxUser.user_worker import user_add
from dxm.lib.DxUser.user_worker import user_delete
from dxm.lib.DxUser.user_worker import user_update
from dxm.lib.DxDomain.domain_worker import domain_list
from dxm.lib.DxDomain.domain_worker import domain_add
from dxm.lib.DxDomain.domain_worker import domain_delete
from dxm.lib.DxDomain.domain_worker import domain_update
from dxm.lib.DxJDBC.jdbc_worker import driver_list
from dxm.lib.DxJDBC.jdbc_worker import driver_add
from dxm.lib.DxJDBC.jdbc_worker import driver_delete


# from lib.DxLogging import print_error
from dxm.lib.DxLogging import logging_est
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message

from dxm.lib.DxEngine.DxConfig import DxConfig

__version__ = "0.9.3"

class dxm_state(object):

    def __init__(self):
        self.logfile = "dxm.log"
        self.debug = False
        self.engine = None
        self.format = None
        self.username = None
        self.configfile = None


pass_state = click.make_pass_decorator(dxm_state, ensure=True)


def debug_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(dxm_state)
        state.debug = value
        logging_est(state.logfile, state.debug)
        return value
    return click.option('--debug',
                        #is_flag=True,
                        count=True,
                        expose_value=False,
                        help='Enables debug mode.',
                        callback=callback)(f)


def engine_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(dxm_state)
        state.engine = value
        return value
    return click.option('--engine',
                        expose_value=False,
                        help='Engine name',
                        callback=callback)(f)


def user_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(dxm_state)
        state.engineuser = value
        return value
    return click.option('--engineuser',
                        expose_value=False,
                        help='User name',
                        callback=callback)(f)


def logfile_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(dxm_state)
        state.logfile = value
        return value
    return click.option('--logfile',
                        expose_value=False,
                        help='Logfile path and name',
                        callback=callback)(f)


def format_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(dxm_state)
        state.format = value
        return value
    return click.option('--format',
                        expose_value=False,
                        help='Output format',
                        type=click.Choice(['fixed', 'csv', 'json']),
                        default='fixed',
                        callback=callback)(f)


def configfile_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(dxm_state)
        state.configfile = value
        return value
    return click.option('--configfile',
                        expose_value=False,
                        help='Config path and name',
                        callback=callback)(f)


def common_options(f):
    f = logfile_option(f)
    f = debug_option(f)
    f = engine_option(f)
    f = format_option(f)
    f = user_option(f)
    f = configfile_option(f)
    return f

def debug_options(f):
    f = engine_option(f)
    f = user_option(f)
    f = debug_option(f)
    return f

def sort_options():
    return click.option('--sortby',
                        help='Sort by column number')


@click.group()
@click.version_option(version=__version__, prog_name ='dxmc')
@pass_state
def dxm(dxm_state):
    """
    dxmc is a Delphix Masking Toolkit command line interface
    This command can be used to run all applications

    If option --engine is not specified, dxm will run all actions against
    masking engines configured with default option set to Y.

    To run command on all engines configured for this toolkit use all
    as a engine_name
    """


@dxm.group()
@common_options
@pass_state
def engine(dxm_state):
    """
    engine is a group of command to add, delete and list Masking engines
    configured with this installation of dxtoolkit
    """


@dxm.group()
@pass_state
def application(dxm_state):
    """
    Application group allow to control applications
    """


@dxm.group()
@pass_state
def environment(dxm_state):
    """
    Environment group allow to control environments
    """


@dxm.group()
@pass_state
def connector(dxm_state):
    """
    Connector group allow to control environments
    """


@dxm.group()
@pass_state
def ruleset(dxm_state):
    """
    Ruleset group allow to control rulesets
    """


@dxm.group()
@pass_state
def job(dxm_state):
    """
    Job group allow to control job
    """


@dxm.group()
@pass_state
def fileformat(dxm_state):
    """
    Filetype group allow to control file types
    """


@dxm.group()
@pass_state
def column(dxm_state):
    """
    Column group allow to control inventory
    """


@dxm.group()
@pass_state
def algorithms(dxm_state):
    """
    Algorithm group allow to control Algorithm
    """


@dxm.group()
@pass_state
def meta(dxm_state):
    """
    Meta group allow to control tables and files metadata
    """

@dxm.group()
@pass_state
def profileset(dxm_state):
    """
    Profileset group allow to control Profile Sets
    """

@dxm.group()
@pass_state
def expression(dxm_state):
    """
    Expression group allow to control Profile expressions
    """

@dxm.group()
@pass_state
def profilejob(dxm_state):
    """
    Profile job group allow to control Profile jobs
    """

@dxm.group()
@pass_state
def sync(dxm_state):
    """
    Sync objects between engines or export/import to files
    """

@dxm.group()
@pass_state
def role(dxm_state):
    """
    Role group allow to control user roles
    """

@dxm.group()
@pass_state
def user(dxm_state):
    """
    User group allow to control users
    """

@dxm.group()
@pass_state
def domain(dxm_state):
    """
    Domain group allow to control domains
    """

@dxm.group()
@pass_state
def jdbc(dxm_state):
    """
    JDBC group allows to control JDBC drivers
    """

@engine.command()
@click.option('--engine', help='Engine name (or alias)', required=True)
@click.option('--ip',  help='IP or FQDN of engine', required=True)
@click.option(
    '--port', help='Port used by engine (default 8282)', default=80,
    required=True)
@click.option(
    '--protocol', help='Communication protocol (default http)', default='http',
    required=True, type=click.Choice(['http', 'https']))
@click.option(
    '--username', default='admin', required=True,
    help='Username used by toolkit (default admin)')
@click.option(
    '--default', help='Setting engine as default engine for toolkit'
    ' (Default value N)', type=click.Choice(['Y', 'N']), default='N')
@click.option(
    '--password', prompt=True, hide_input=True,
    confirmation_prompt=True, required=True,
    help='Engine password for specified user. If you want to hide input'
    ' don''t specify this parameter and you will be propted')
@click.option(
    '--proxyurl', 
    help='Proxy URL, ex: http://proxy:3128')
@click.option(
    '--proxyuser', 
    help='Username for proxy')
@click.option(
    '--proxypassword', help='Password for proxy'
    'If you want to hide input put '' as value and you will be propted')
@logfile_option
@debug_options
@configfile_option
@pass_state
def add(dxm_state, engine, ip, port, protocol, username, password, default,
        proxyurl, proxyuser, proxypassword):
    """
    Add engine entry to configuration database
    """
    if proxypassword == '':
        proxypassword = click.prompt('Please enter a password', hide_input=True,
                                     confirmation_prompt=True)
    DxConfig(dxm_state.configfile)
    exit(engine_add(engine, ip, username, password,
         protocol, port, default, proxyurl, proxyuser, proxypassword))


@engine.command()
@click.option('--engine', help='Engine name (or alias)', required=True)
@click.option('--ip', help='IP or FQDN of engine')
@click.option('--port', help='Port used by engine (default 8282)')
@click.option(
    '--protocol', help='Communication protocol',
    type=click.Choice(['http', 'https']))
@click.option(
    '--username', help='New username used by toolkit')
@click.option(
    '--engineuser', help='Existing username defined for engine')
@click.option(
    '--default', help='Setting engine as default engine for toolkit',
    type=click.Choice(['Y', 'N']))
@click.option(
    '--password', help='Engine password for specified user. '
    'If you want to hide input put '' as value and you will be propted')
@click.option(
    '--proxyurl', 
    help='Proxy URL, ex: http://proxy:3128')
@click.option(
    '--proxyuser', 
    help='Username for proxy')
@click.option(
    '--proxypassword', help='Password for proxy'
    'If you want to hide input put '' as value and you will be propted')
@debug_options
@pass_state
def update(dxm_state, engine, ip, port, protocol, username, password, default,
           proxyurl, proxyuser, proxypassword, engineuser):
    """
    Update engine entry in configuration database
    """
    if password == '':
        password = click.prompt('Please enter a password', hide_input=True,
                                confirmation_prompt=True)
    if proxypassword == '':
        proxypassword = click.prompt('Please enter a password', hide_input=True,
                                confirmation_prompt=True)
    DxConfig(dxm_state.configfile)
    exit(engine_update(engine, engineuser, ip, username, password,
         protocol, port, default, proxyurl, proxyuser, proxypassword))


@engine.command()
@common_options
@pass_state
def logout(dxm_state):
    """
    Logout user
    """
    DxConfig(dxm_state.configfile)
    exit(engine_logout(dxm_state.engine, dxm_state.engineuser))


@engine.command()
@click.option('--username', help='Filter output by configured username')
@common_options
@pass_state
def list(dxm_state, username):
    """
    List entries from configuration database
    """
    DxConfig(dxm_state.configfile)
    exit(engine_list(dxm_state.engine, username, dxm_state.format))


@engine.command()
@common_options
@pass_state
def delete(dxm_state):
    """
    Delete entry from configuration database
    """
    DxConfig(dxm_state.configfile)
    exit(engine_delete(dxm_state.engine, dxm_state.engineuser))


@engine.command()
@click.option(
    '--enginelog', type=click.File('wt'), required=True,
    help="Name with path of output logfile")
@click.option(
    '--page_size', type=int, required=False, default=1,
    help="How many pages of log to load (Default=1)")
@click.option(
    '--level', type=click.Choice(['ERROR', 'DEBUG','INFO','WARN']), required=False, default='DEBUG',
    help="Define the required log level (Default=DEBUG)")
# """@common_options"""
@debug_options
@pass_state
def logs(dxm_state, enginelog,page_size,level):
    """
    Save Masking Engine log into file
    """
    DxConfig(dxm_state.configfile)
    exit(engine_logs(dxm_state.engine, dxm_state.engineuser, enginelog, page_size,level))


@engine.command()
@click.option(
    '--filename', required=True,
    help="Name with path of the file to upload")
@debug_options
@pass_state
def upload(dxm_state, filename):
    """
    Save Masking Engine log into file
    """
    DxConfig(dxm_state.configfile)
    exit(engine_upload(dxm_state.engine, dxm_state.engineuser, filename))

@application.command()
@click.option('--appname', help='Filter output by application name')
@common_options
@pass_state
def list(dxm_state, appname):
    """
    List command will display applications configured inside Masking Engine.
    If --appname option is not specified, all application will be displayed.
    If --appname is set, output list will be limited by value of this option
    and return non-zero return code if application is not found.
    """
    DxConfig(dxm_state.configfile)
    exit(application_list(dxm_state.engine, dxm_state.engineuser, dxm_state.format, appname))


@application.command()
@click.option(
    '--appname', required=True, help='Application name to add')
@common_options
@pass_state
def add(dxm_state, appname):
    """
    Add command will add application to Masking Engine.
    Option --appname is required. Exit code will be set to 0
    if application was added and to non-zero value if there was an error
    """
    DxConfig(dxm_state.configfile)
    exit(application_add(dxm_state.engine, dxm_state.engineuser, appname))


@environment.command()
@click.option('--envname', help='Filter output by environment name')
@common_options
@pass_state
def list(dxm_state, envname):
    """
    List environments configured inside Masking Engine.
    If --envname option is not specified, all environments will be displayed.
    If --envname is set, output list will be limited by value of this option
    and return non-zero return code if environment is not found.
    """
    DxConfig(dxm_state.configfile)
    exit(environment_list(dxm_state.engine, dxm_state.engineuser, dxm_state.format, envname))


@environment.command()
@click.option('--envname', required=True, help='Environment name to add')
@click.option(
    '--appname', required=True, help='Application name for the environment')
@click.option(
    '--purpose', default='MASK', type=click.Choice(['MASK', 'CUSTOM']),
    help="Purpuse of the environment. (Default value is MASK)")
@common_options
@pass_state
def add(dxm_state, envname, appname, purpose):
    """
    Add command will add environment to Masking Engine.
    Options --envname and --appname are required. Exit code will be set to 0
    if environment was added and to non-zero value if there was an error
    """
    DxConfig(dxm_state.configfile)
    exit(environment_add(dxm_state.engine, dxm_state.engineuser, envname, appname, purpose))


@environment.command()
@click.option('--envname', required=True, help='Environment name to delete')
@common_options
@pass_state
def delete(dxm_state, envname):
    """
    Delete command will remove environment from Masking Engine.
    Option --envname is required. Exit code will be set to 0
    if environemnt was deleted and to non-zero value if there was an error
    """
    DxConfig(dxm_state.configfile)
    exit(environment_delete(dxm_state.engine, dxm_state.engineuser, envname))


@connector.command()
@click.option('--connectorname', help='Filter output by connector name')
@click.option('--envname', help='Filter output by environment name')
@click.option('--details', is_flag=True, help='Display details of connector')
@common_options
@pass_state
def list(dxm_state, connectorname, envname, details):
    """
    List connectors configured inside Masking Engine.
    If no filter options are specified, all connectors will be displayed.
    If --envname or --connectorname is set, output list will be limited
    by value of this option and return non-zero return code
    if connector is not found.

    Option --details will display additional column with connector details
    """
    DxConfig(dxm_state.configfile)
    exit(connector_list(
        dxm_state.engine, dxm_state.engineuser, dxm_state.format, envname, connectorname,
        details))


@connector.command()
@click.option('--connectorname', required=True, help='Connector name to add')
@click.option(
    '--envname', required=True,
    help='Environment name where connector will be added')
@click.option(
    '--connectortype',
    type=click.Choice(database_types + file_types),
    required=True, help='Type of the connector')
@click.option(
    '--host', help='Host where connector will be pointed')
@click.option(
    '--jdbc', help='jdbc connection string for a connector (advanced option)')
@click.option(
    '--port', type=int,
    help='Port used by database connector')
@click.option(
    '--username', required=True,
    help='Username (login) of database (for database connectors)'
    'or host user (for file connectors)')
@click.option(
    '--schemaname', required=True,
    help='Schema name used for ruleset for database connectors')
@click.option(
    '--password', prompt=True, hide_input=True, confirmation_prompt=True,
    help='Connector password for specified user. If you want to hide input'
    ' don''t specify this parameter and you will be propted')
@click.option(
    '--sid', help='Oracle SID of database for Oracle connector type')
@click.option(
    '--instancename', help='MSSQL instance name for MSSQL connector type')
@click.option(
    '--databasename', help='Database name for MSSQL or SYBASE connector type')
@click.option(
    '--path', help='Path of files for FILE connector type')
@click.option(
    '--servertype', type=click.Choice(['sftp', 'ftp']),
    help='Server type for FILE connector type')
@click.option(
    '--jdbc_driver_name',
    help='Driver name')

    
@common_options
@pass_state
def add(dxm_state, connectorname, envname, connectortype, host, port, username,
        schemaname, password, sid, instancename, databasename, path,
        servertype, jdbc, jdbc_driver_name):
    """
    Add connector to Masking Engine.
    List of required parameters depend on connector type:

    \b
        - database connectors:
            connectorname,
            envname,
            connectortype,
            username,
            schemaname,
            host and port or jdbc connection string

        - database depended options or jdbc connection string:
            sid,
            instancename,
            databasename

    \b
        - file connectors:
            connectorname,
            envname,
            connectortype,
            host,
            username,
            path,
            servertype


    Exit code will be set to 0 if connector was added
    and to non-zero value if there was an error
    """
    params = {
        'envname': envname,
        'schemaName': schemaname,
        'host': host,
        'port': port,
        'password': password,
        'username': username,
        'connname': connectorname,
        'sid': sid,
        'instancename': instancename,
        'databasename': databasename,
        'type': connectortype,
        'path': path,
        'servertype': servertype,
        'jdbc': jdbc,
        'jdbc_driver_name': jdbc_driver_name
    }
    DxConfig(dxm_state.configfile)
    exit(connector_add(dxm_state.engine, dxm_state.engineuser, params))


@connector.command()
@click.option('--connectorname', required=True)
@click.option('--host', help='Host where connector will be pointed')
@click.option('--port', type=int, help='Port used by database connector')
@click.option('--username',
              help='Username (login) of database (for database connectors)'
              'or host user (for file connectors)')
@click.option('--schemaname',
              help='Schema name used for ruleset for database connectors')
@click.option('--password',
              help='Connector password for specified user. If you want to hide'
              ' input put '' as password and you will be propted')
@click.option('--sid', help='Oracle SID of database for Oracle connector type')
@click.option('--instancename',
              help='MSSQL instance name for MSSQL connector type')
@click.option('--databasename',
              help='Database name for MSSQL or SYBASE connector type')
@click.option(
    '--jdbc', help='jdbc connection string for a connector (advanced option)')
@click.option(
    '--envname',
    help='Environment name where connector will be added')
@click.option(
    '--path', help='Path of files for FILE connector type')
@click.option(
    '--servertype', type=click.Choice(['sftp', 'ftp']),
    help='Server type for FILE connector type')
@common_options
@pass_state
def update(dxm_state, envname, connectorname, host, port, username,
           schemaname, password, sid, instancename, databasename,
           path, servertype, jdbc):
    """
    Update the connector inside Masking Engine.
    Exit code will be set to 0 if connector was updated
    and to non-zero value if there was an error
    """
    if password == '':
        password = click.prompt('Please enter a password', hide_input=True,
                                confirmation_prompt=True)
    params = {
        'schemaName': schemaname,
        'host': host,
        'port': port,
        'password': password,
        'username': username,
        'connname': connectorname,
        'sid': sid,
        'instancename': instancename,
        'databasename': databasename,
        'envname': envname,
        'servertype': servertype,
        'path': path,
        'jdbc': jdbc
    }
    DxConfig(dxm_state.configfile)
    exit(connector_update(dxm_state.engine, dxm_state.engineuser, params))


@connector.command()
@click.option(
    '--connectorname', required=True, help='Connector name to delete')
@click.option(
    '--envname', help='Environment name of connector to delete')
@common_options
@pass_state
def delete(dxm_state, connectorname, envname):
    """
    Delete command will remove connector from Masking Engine.
    Option --connectorname is required. Exit code will be set to 0
    if connector was deleted and to non-zero value if there was an error
    """
    DxConfig(dxm_state.configfile)
    exit(connector_delete(dxm_state.engine, dxm_state.engineuser, connectorname, envname))


@connector.command()
@click.option('--connectorname', required=True, help='Connector name to test')
@click.option('--envname', help='Environment name of connector')
@common_options
@pass_state
def test(dxm_state, connectorname, envname):
    """
    Test command will test connector on Masking Engine.
    Option --connectorname is required. Exit code will be set to 0
    if test was succesful and to non-zero value if there was an error
    """
    DxConfig(dxm_state.configfile)
    exit(connector_test(dxm_state.engine, dxm_state.engineuser, connectorname, envname))


@connector.command()
@click.option(
    '--connectorname', required=True, help='Connector name to fetch data from')
@click.option(
    '--envname', help='Environment name of connector')
@common_options
@pass_state
def fetch_meta(dxm_state, connectorname, envname):
    """
    Fetch_meta command will display a list of tables or files seen
    by connector. Option --connectorname is required.

    Exit code will be set to non-zero value if there was an error
    """
    DxConfig(dxm_state.configfile)
    exit(connector_fetch(dxm_state.engine, dxm_state.engineuser, connectorname, envname,
                         dxm_state.format))


@ruleset.command()
@click.option(
    '--rulesetname', help='Filter output by ruleset name')
@click.option(
    '--envname', help='Filter output by environment name')
@common_options
@pass_state
def list(dxm_state, rulesetname, envname):
    """
    List rulesets from Masking engine.
    If no filter options are specified, all rulesets will be displayed.
    If --envname or --rulesetname is set, output list will be limited
    by value of this option and return non-zero return code
    if ruleset is not found.
    """
    DxConfig(dxm_state.configfile)
    exit(ruleset_list(
        dxm_state.engine, dxm_state.engineuser, dxm_state.format, rulesetname, envname))


@ruleset.command()
@click.option(
    '--rulesetname', required=True, help='Ruleset name to add')
@click.option(
    '--connectorname', required=True,
    help='Connector name to be used by ruleset')
@click.option(
    '--envname', required=True,
    help='Environment name where ruleset will be created')
@common_options
@pass_state
def add(dxm_state, rulesetname, connectorname, envname):
    """
    Add ruleset to Masking engine.
    List of required parameters:

    \b
        - rulesetname
        - connectorname
        - envname

    Return non-zero code if there was a problem with adding ruleset
    """
    DxConfig(dxm_state.configfile)
    exit(ruleset_add(dxm_state.engine, dxm_state.engineuser, rulesetname, connectorname, envname))


@ruleset.command()
@click.option(
    '--rulesetname', required=True, help='Ruleset name to delete')
@click.option(
    '--envname', help='Environment name of ruleset to delete')
@common_options
@pass_state
def delete(dxm_state, rulesetname, envname):
    """
    Delete ruleset from Masking engine.
    Return non-zero code if there was a problem with deleting ruleset
    """
    DxConfig(dxm_state.configfile)
    exit(ruleset_delete(dxm_state.engine, dxm_state.engineuser, rulesetname, envname))

@ruleset.command()
@click.option(
    '--rulesetname', required=True, help='Ruleset name to delete')
@click.option(
    '--envname', help='Environment name of ruleset to delete')
@common_options
@pass_state
def refresh(dxm_state, rulesetname, envname):
    """
    Refresh a ruleset on the Masking engine
    Return non-zero code if there was a problem with deleting ruleset
    """
    DxConfig(dxm_state.configfile)
    exit(ruleset_refresh(dxm_state.engine, dxm_state.engineuser, rulesetname, envname))

@ruleset.command()
@click.option(
    '--rulesetname', required=True,
    help='Ruleset name of source ruleset to clone')
@click.option(
    '--newrulesetname', required=True, help="Target ruleset name")
@click.option(
    '--envname', help="Environment name where source and target ruleset exist")
@common_options
@pass_state
def clone(dxm_state, rulesetname, envname, newrulesetname):
    """
    Clone ruleset to new one inside same environment
    Return non-zero code if there was a problem with cloning ruleset
    """
    DxConfig(dxm_state.configfile)
    exit(ruleset_clone(dxm_state.engine, dxm_state.engineuser, rulesetname, envname,
                       newrulesetname))


@ruleset.command()
@click.option(
    '--rulesetname', required=True,
    help='Ruleset name of source ruleset to clone')
@click.option(
    '--envname', help="Environment name where source and target ruleset exist")
@click.option(
    '--outputfile', type=click.File('wt'), required=True,
    help="Name with path of output file where ruleset(s) will be exported"
    " in JSON format")
@click.option(
    '--exportmeta', help="Export metadata with ruleset. Default set to yes",
    type=click.Choice(['Y', 'N']), default='Y')
@click.option(
    '--metaname',
    help="Name of table or file to export. If not specified all objects from"
         " ruleset will be exported")
@common_options
@pass_state
def exportrule(dxm_state, rulesetname, envname, outputfile,
               exportmeta, metaname):
    """
    Export ruleset into a JSON file
    """
    DxConfig(dxm_state.configfile)
    exit(ruleset_export(
        dxm_state.engine, dxm_state.engineuser, rulesetname, envname,
        outputfile, exportmeta, metaname))


@ruleset.command()
@click.option(
    '--rulesetname',
    help='Ruleset name of source ruleset to clone')
@click.option(
    '--connectorname',
    help='Connector name to be used by ruleset')
@click.option(
    '--envname', help="Environment name where source and target ruleset exist")
@click.option(
    '--inputfile', type=click.File('rt'), required=True,
    help="Name with path of input file where ruleset(s) will be imported from")
@common_options
@pass_state
def importrule(dxm_state, inputfile, rulesetname, envname, connectorname):
    """
    Import a ruleset from a JSON file created by exportrule command
    """
    DxConfig(dxm_state.configfile)
    exit(ruleset_import(
        dxm_state.engine, dxm_state.engineuser, inputfile, rulesetname, connectorname, envname))

@ruleset.command()
@click.option(
    '--inputfile', type=click.File('rt'), required=True,
    help="Name with path of input file to compare")
@common_options
@pass_state
def checkrule(dxm_state, inputfile):
    """
    Compare ruleset from file generated by exportrule command 
    with ruleset on the Masking engine
    """
    DxConfig(dxm_state.configfile)
    exit(ruleset_check(dxm_state.engine, dxm_state.engineuser, inputfile))

@ruleset.command()
@click.option(
    '--rulesetname', required=True,
    help='Ruleset name where table or file will be added')
@click.option(
    '--envname', help="Environment name where ruleset exist")
@click.option(
    '--metaname',
    help="Name of table or file to add to ruleset")
@click.option('--custom_sql', help="Custom SQL specified for table")
@click.option('--where_clause', help="Where clause specified for table")
@click.option('--having_clause', help="Having clause specified for table")
@click.option('--key_column', help="Key column specified for table")
@click.option('--file_format', help="File format of added file")
@click.option('--file_delimiter', help="Delimited used in added file")
@click.option(
    '--file_eor', type=click.Choice(['linux', 'windows', 'custom']),
    help="End of record used in file. For custom value file_eor_custom"
    " is needed")
@click.option('--file_eor_custom', help="Custom end of record in added file")
@click.option('--file_enclosure', help="Enclosure of fields in added file")
@click.option(
    '--file_name_regex', is_flag=True,
    help="Flag is file name is a regular expression and not a single"
    "file name")
@click.option(
    '--inputfile', type=click.File('rt'),
    help="Name and path of CSV file used to load metadata")
@click.option(
    '--fromconnector', is_flag=True,
    help="Add tables fetched from connector filtered by filter if fetchfilter is specified")
@click.option(
    '--fetchfilter',
    help="Filter metadata fetched from connector ( * is allowed as a wildcard, ex. EMP* to load all tables started with EMP)")
@click.option(
    '--bulk', is_flag=True,
    help="Use bulk method to add medatata from file or connector table list")
@common_options
@pass_state
def addmeta(dxm_state, rulesetname, metaname, custom_sql, where_clause,
            having_clause, key_column, inputfile, file_format,
            file_delimiter, file_eor, file_enclosure, file_name_regex,
            file_eor_custom, envname, fromconnector, fetchfilter, bulk):
    """
    Add metadata (table or file) to ruleset.

    List of required and optional parameters depend on metadata type:

    \b
        - table:
            rulesetname
            metaname (aka table name)
            envname (optional)
            custom_sql (optional)
            where_clause (optional)
            key_column (optional)

    \b
        - file:
            rulesetname
            metaname (aka file name)
            file_format
            file_delimiter
            file_eor
            envname (optional)
            file_enclosure (optional)
            file_name_regex (optional)
            file_eor_custom (optional)

    For batch load from CSV file use --inputfile option.

    If file_delimiter is comma, it has to be enclosed by double qoute
    like this ",".
    If file_enclosure is double quote, it has to be esaped by \ character
    like this \\".

    File format for tables:
    \b
    tablename, custom_sql, where_clause, having_clause, key_column

    \b
    metaname,file_name_regex,file_format,file_delimiter,file_eor,file_enclosure

    Exit code will be set to 0 if metadata was added
    and to non-zero value if there was an error
    """
    params = {
        "rulesetname": rulesetname,
        "metaname": metaname,
        "custom_sql": custom_sql,
        "where_clause": where_clause,
        "having_clause": having_clause,
        "key_column": key_column,
        "file_format": file_format,
        "file_delimiter": file_delimiter,
        "file_eor": file_eor,
        "file_enclosure": file_enclosure,
        "file_name_regex": file_name_regex,
        "file_eor_custom": file_eor_custom,
        "envname": envname,
        "fetchfilter": fetchfilter
    }
    DxConfig(dxm_state.configfile)
    exit(ruleset_addmeta(dxm_state.engine, dxm_state.engineuser, params, inputfile, fromconnector, bulk))


@ruleset.command()
@click.option('--rulesetname', help='Filter output by ruleset name')
@click.option('--envname', help='Filter output by environment name')
@click.option('--metaname', help='Filter output by meta name')
@common_options
@pass_state
def listmeta(dxm_state, rulesetname, envname, metaname):
    """
    Display list of metadata (tables or files) defined in ruleset.

    If no filter options are specified, all metadata will be displayed.
    If --envname or --rulesetname or --metaname is set, output list will
    be limited by value of this option and return non-zero return code
    if metaname is not found.
    """
    DxConfig(dxm_state.configfile)
    exit(ruleset_listmeta(
        dxm_state.engine, dxm_state.engineuser, dxm_state.format, rulesetname, envname, metaname))


@ruleset.command()
@click.option(
    '--metaname', required=True,
    help='Name of table or file to be deleted')
@click.option(
    '--rulesetname', required=True,
    help='Ruleset name of table or file to be deleted')
@click.option('--envname', help="Environment name where rulesetname exist")
@common_options
@pass_state
def deletemeta(dxm_state, metaname, rulesetname, envname):
    """
    Delete a table or file from ruleset.
    Return non-zero return code for error.
    """
    DxConfig(dxm_state.configfile)
    exit(ruleset_deletemeta(dxm_state.engine, dxm_state.engineuser, rulesetname, metaname, envname))


@job.command()
@click.option('--jobname', help="Filter jobs using jobname")
@click.option('--envname', help='Filter jobs belongs to one environment')
@common_options
@pass_state
def list(dxm_state, jobname, envname):
    """
    Display list of jobs defined in Masking Engine

    If no filter options are specified, all jobs will be displayed.
    If --envname or --jobname is set, output list will
    be limited by value of this option and return non-zero return code
    if jobname is not found.
    """
    DxConfig(dxm_state.configfile)
    exit(jobs_list(dxm_state.engine, dxm_state.engineuser, jobname, envname, dxm_state.format))

@job.command()
@click.option('--jobname', help="Filter jobs using jobname")
@click.option('--envname', help='Filter jobs belongs to one environment')
@click.option('--last', help='Display only last execution', is_flag=True)
@click.option('--details', help='Display execution details', is_flag=True, default=False)
@click.option('--startdate', help='Display jobs started after startdate', type=click.DateTime())
@click.option('--enddate', help='Display jobs finished before enddate', type=click.DateTime())
@common_options
@pass_state
def report(dxm_state, jobname, envname, last, startdate, enddate, details):
    """
    Display report of jobs defined in Masking Engine

    If no filter options are specified, all jobs will be displayed.
    If --envname or --jobname is set, output list will
    be limited by value of this option and return non-zero return code
    if jobname is not found.
    """
    DxConfig(dxm_state.configfile)
    exit(jobs_report(dxm_state.engine, dxm_state.engineuser, jobname, envname, dxm_state.format, 
                     last, startdate, enddate, details))

@job.command()
@click.option(
    '--jobname', required=True, help="Name of job to add")
@click.option(
    '--envname', required=True,
    help="Name of environment where job will be added")
@click.option(
    '--rulesetname', required=True,
    help="Name of ruleset which will be used for masking job")
@click.option(
    '--jobdesc', help="Desciption of the job")
@click.option(
    '--email', help="e-mail address used for job notification")
@click.option(
    '--on_the_fly_src_connector', help="source connector name for on the fly job")
@click.option(
    '--on_the_fly_src_envname', help="source environment name for on the fly job")
@click.option(
    '--feedback_size', type=int,
    help="Feedback size of masking job")
@click.option(
    '--max_memory', type=int,
    help="Maximum size of memory used by masking job")
@click.option(
    '--min_memory', type=int,
    help="Minimum size of memory used by masking job")
@click.option(
    '--num_streams', type=int,
    help="Number of concurrent objects (tables/files) being masked by job")
@click.option(
    '--commit_size', type=int,
    help="Number of rows after which commit will be issued")
@click.option(
    '--threads', type=int, default=1,
    help="Number of threads masking single object. "
    "DON'T CHANGE UNLESS YOU KNOW WHAT YOU ARE DOING")
@click.option(
    '--on_the_fly', type=click.Choice(['Y', 'N']),
    help="Define job as 'on the fly' masking")
@click.option(
    '--multi_tenant', type=click.Choice(['Y', 'N']),
    help="Define job as multi-tenant")
@click.option(
    '--batch_update', type=click.Choice(['Y', 'N']),
    help="Enable batch update for job."
    "DON'T CHANGE UNLESS YOU KNOW WHAT YOU ARE DOING")
@click.option(
    '--disable_constraints', type=click.Choice(['Y', 'N']),
    help="Disable constraints for duration of masking job")
@click.option(
    '--drop_indexes', type=click.Choice(['Y', 'N']),
    help="Drop indexes for duration of masking job")
@click.option(
    '--disable_triggers', type=click.Choice(['Y', 'N']),
    help="Disable triggers for duration of masking job")
@click.option(
    '--truncate_tables', type=click.Choice(['Y', 'N']),
    help="Truncate table before starting load. "
    "Use for on the fly masking only")
@click.option(
    '--bulk_data', type=click.Choice(['Y', 'N']),
    help="Use bulk update for jobs. It's use by default")
@click.option(
    '--prescript', type=click.File('rt'),
    help="File name and path used as prescript")
@click.option(
    '--postscript', type=click.File('rt'),
    help="File name and path used as postscript")
@common_options
@pass_state
def add(dxm_state, jobname, envname, rulesetname, email, feedback_size,
        max_memory, min_memory, jobdesc, num_streams, on_the_fly,
        on_the_fly_src_connector, on_the_fly_src_envname, commit_size, threads, multi_tenant, batch_update,
        disable_constraints, drop_indexes, disable_triggers, truncate_tables,
        prescript, postscript, bulk_data):
    """
    Add a new job to Masking engine

    List of required parameters:

    \b
        jobname
        envname
        rulesetname

    Return non zero code if there was problem with adding a new job
    """

    params = {
        "envname": envname,
        "jobname": jobname,
        "rulesetname": rulesetname,
        "email": email,
        "feedback_size": feedback_size,
        "max_memory": max_memory,
        "min_memory": min_memory,
        "job_description": jobdesc,
        "num_input_streams": num_streams,
        "on_the_fly_masking": on_the_fly,
        "on_the_fly_src_connector": on_the_fly_src_connector,
        "on_the_fly_src_envname": on_the_fly_src_envname,
        "commit_size": commit_size,
        "num_output_threads_per_stream": threads,
        "multi_tenant": multi_tenant,
        "batch_update": batch_update,
        "bulk_data": bulk_data,
        "disable_constraints": disable_constraints,
        "drop_indexes": drop_indexes,
        "disable_triggers": disable_triggers,
        "truncate_tables": truncate_tables,
        "prescript": prescript,
        "postscript": postscript
    }
    DxConfig(dxm_state.configfile)
    exit(job_add(dxm_state.engine, dxm_state.engineuser, params))


@job.command()
@click.option('--jobname', required=True, help="Name of job to update")
@click.option(
    '--envname', help="Name of environment where job will be updated")
@click.option(
    '--rulesetname', help="Name of ruleset which will be used for masking job")
@click.option(
    '--jobdesc', help="Desciption of the job")
@click.option(
    '--email', help="e-mail address used for job notification")
@click.option(
    '--on_the_fly_source', help="connector name for on the fly job")
@click.option(
    '--feedback_size', type=int,
    help="Feedback size of masking job")
@click.option(
    '--max_memory', type=int,
    help="Maximum size of memory used by masking job")
@click.option(
    '--min_memory', type=int,
    help="Minimum size of memory used by masking job")
@click.option(
    '--num_streams', type=int,
    help="Number of concurrent objects (tables/files) being masked by job")
@click.option(
    '--commit_size', type=int,
    help="Number of rows after which commit will be issued")
@click.option(
    '--threads', type=int, default=1,
    help="Number of threads masking single object. "
    "DON'T CHANGE UNLESS YOU KNOW WHAT YOU ARE DOING")
@click.option(
    '--on_the_fly', type=click.Choice(['Y', 'N']),
    help="Define job as 'on the fly' masking")
@click.option(
    '--multi_tenant', type=click.Choice(['Y', 'N']),
    help="Define job as multi-tenant")
@click.option(
    '--batch_update', type=click.Choice(['Y', 'N']),
    help="Enable batch update for job."
    "DON'T CHANGE UNLESS YOU KNOW WHAT YOU ARE DOING")
@click.option(
    '--disable_constraints', type=click.Choice(['Y', 'N']),
    help="Disable constraints for duration of masking job")
@click.option(
    '--drop_indexes', type=click.Choice(['Y', 'N']),
    help="Drop indexes for duration of masking job")
@click.option(
    '--disable_triggers', type=click.Choice(['Y', 'N']),
    help="Disable triggers for duration of masking job")
@click.option(
    '--truncate_tables', type=click.Choice(['Y', 'N']),
    help="Truncate table before starting load. "
    "Use for on the fly masking only")
@click.option(
    '--bulk_data', type=click.Choice(['Y', 'N']),
    help="Use bulk update for jobs. It's use by default")
@click.option(
    '--prescript', 
    help="File name and path used as prescript")
@click.option(
    '--postscript',
    help="File name and path used as postscript")
@common_options
@pass_state
def update(dxm_state, jobname, envname, rulesetname, email, feedback_size,
           max_memory, min_memory, jobdesc, num_streams, on_the_fly,
           on_the_fly_source, commit_size, threads, multi_tenant, batch_update,
           disable_constraints, drop_indexes, disable_triggers,
           truncate_tables, prescript, postscript, bulk_data):
    """
    Update an existing job on Masking engine
    Return non zero code if there was problem with updating a job
    """

    f_prescript = None
    f_postscript = None

    try:
        if prescript is not None:
            if prescript == '':
                f_prescript = prescript
            else:
                f_prescript = open(prescript)

        if postscript is not None:
            if postscript == '':
                f_postscript = postscript
            else:
                f_postscript = open(postscript)

    except FileNotFoundError:
        print_error("File {} not found".format(prescript))
        DxConfig(dxm_state.configfile)
    exit(1)


    params = {
        "rulesetname": rulesetname,
        "email": email,
        "feedback_size": feedback_size,
        "max_memory": max_memory,
        "min_memory": min_memory,
        "job_description": jobdesc,
        "num_input_streams": num_streams,
        "on_the_fly_masking": on_the_fly,
        "on_the_fly_masking_source": on_the_fly_source,
        "commit_size": commit_size,
        "num_output_threads_per_stream": threads,
        "multi_tenant": multi_tenant,
        "batch_update": batch_update,
        "bulk_data": bulk_data,
        "disable_constraints": disable_constraints,
        "drop_indexes": drop_indexes,
        "disable_triggers": disable_triggers,
        "truncate_tables": truncate_tables,
        "prescript": f_prescript,
        "postscript": f_postscript
    }
    DxConfig(dxm_state.configfile)
    exit(job_update(dxm_state.engine, dxm_state.engineuser, jobname, envname, params))


@job.command()
@click.option(
    '--jobname', required=True, help="Name of job to update", multiple=True)
@click.option(
    '--envname', help="Name of environment where job will be started")
@click.option(
    '--tgt_connector', help="Name of target connector for multi tenant job")
@click.option(
    '--tgt_connector_env', help="Name of target connector environment "
    "for multi tenant job")
@click.option('--nowait', is_flag=True, help="No wait for job to finish")
@click.option(
    '--parallel', type=int, help="Number of parallel jobs",
    default=1
)
@click.option('--monitor', is_flag=True, help="Display progress bars")
@common_options
@pass_state
def start(dxm_state, jobname, envname, tgt_connector, tgt_connector_env,
          nowait, parallel, monitor):
    """
    Start masking job. By default control is returned when job is finished.
    If --nowait flag is specified script doesn't monitor job and release
    control after job is started.
    """
    DxConfig(dxm_state.configfile)
    exit(job_start(dxm_state.engine, dxm_state.engineuser, jobname, envname, tgt_connector,
                   tgt_connector_env, nowait, parallel, monitor))


@job.command()
@click.option(
    '--jobname', required=True, help="Name of job to be deleted")
@click.option(
    '--envname', help="Name of environment where job will be deleted")
@common_options
@pass_state
def delete(dxm_state, jobname, envname):
    """
    Delete an existing job from Masking Engine.
    Return non zero code if there was problem with deleting a job
    """
    DxConfig(dxm_state.configfile)
    exit(job_delete(dxm_state.engine, dxm_state.engineuser, jobname, envname))

# clarification with API develeopers needed about canceling job
# @job.command()
# @click.option(
#     '--jobname', required=True, help="Name of job to be canceled")
# @click.option(
#     '--envname', help="Name of environment where job will be canceled")
# @common_options
# @pass_state
# def cancel(dxm_state, jobname, envname):
#     """
#     Cancel execution of running job.
#     Return non zero code if there was problem with canceling a job
#     """
#     DxConfig(dxm_state.configfile)
#     exit(job_cancel(dxm_state.engine, dxm_state.engineuser, jobname, envname))


@job.command()
@click.option(
    '--jobname', required=True, help="Name of source job")
@click.option(
    '--envname', help="Name of environment for source and target job")
@click.option(
    '--newjobname', required=True, help="Name of target job")
@common_options
@pass_state
def copy(dxm_state, jobname, envname, newjobname):
    """
    Copy an existing job to a new one.
    Return non zero code if there was problem with canceling a job
    """
    DxConfig(dxm_state.configfile)
    exit(job_copy(dxm_state.engine, dxm_state.engineuser, jobname, envname, newjobname))


@fileformat.command()
@click.option('--fileformatname', required=True)
@common_options
@pass_state
def delete(dxm_state, fileformatname):
    """ FileFormat list """
    DxConfig(dxm_state.configfile)
    exit(fileformat_delete(dxm_state.engine, dxm_state.engineuser, fileformatname))


@fileformat.command()
@click.option('--fileformattype', type=click.Choice(['DELIMITED', 'EXCEL',
                                                     'FIXED_WIDTH', 'XML']))
@click.option('--fileformatname')
@common_options
@pass_state
def list(dxm_state, fileformattype, fileformatname):
    """ FileFormat list """
    DxConfig(dxm_state.configfile)
    exit(fileformat_list(
        dxm_state.engine, dxm_state.engineuser, dxm_state.format, fileformattype, fileformatname))


@fileformat.command()
@click.option('--fileformattype', required=True,
              type=click.Choice(['delimited', 'excel',
                                 'fixed_width', 'xml']))
@click.option('--fileformatfile', type=click.File('rt'), required=True)
@common_options
@pass_state
def add(dxm_state, fileformattype, fileformatfile):
    """ FileFormat add """
    DxConfig(dxm_state.configfile)
    exit(fileformat_add(dxm_state.engine, dxm_state.engineuser, fileformattype, fileformatfile))


@column.command()
@click.option(
    '--columnname', help="Filter output by a column name")
@click.option(
    '--metaname', help="Filter output by a meta name (table or file name)")
@click.option('--rulesetname', help="Filter output by a ruleset name")
@click.option('--envname', help="Filter output by an environment name")
@click.option('--algname', help="Filter output by an algorithm name")
@click.option(
    '--is_masked', is_flag=True, help="Filter output to masked columns only")
@sort_options()
@common_options
@pass_state
def list(dxm_state, rulesetname, envname, metaname, columnname, algname,
         is_masked, sortby):
    """
    Display list of columns (inventory) defined in Masking Engine

    If no filter options are specified, all columns will be displayed.

    Possible filters can be specified by:

        \b
        columnname
        metaname (table or file name)
        rulesetname
        envname
        algname
        is_masked

    output list will be limited by value of above filter
    and return non-zero return code if columnname is not found.
    """
    DxConfig(dxm_state.configfile)
    exit(column_list(
        dxm_state.engine, dxm_state.engineuser, dxm_state.format, sortby, rulesetname, envname,
        metaname, columnname, algname, is_masked))


@column.command()
@click.option('--columnname', help="Filter output by a column name")
@click.option(
    '--metaname', help="Filter output by a meta name (table or file name)")
@click.option('--rulesetname', help="Filter output by a ruleset name",
              required=True)
@click.option('--envname', help="Filter output by an environment name")
@click.option('--algname', help="Filter output by an algorithm name")
@click.option(
    '--is_masked', is_flag=True, help="Filter output to masked columns only")
@click.option(
    '--outputfile', type=click.File('wt'), required=True,
    help="Name with path of output file where masking inventory will be saved"
    " in CSV format")
@click.option('--inventory', help="Output will compatible with GUI inventory",
              is_flag=True)
@sort_options()
@common_options
@pass_state
def save(dxm_state, rulesetname, envname, metaname, columnname, algname,
         is_masked, sortby, outputfile, inventory):
    """
    Save column masking rules (inventory) into CSV file which can be loaded
    later using toolkit.
    """
    DxConfig(dxm_state.configfile)
    exit(column_save(dxm_state.engine, dxm_state.engineuser, sortby, rulesetname, envname, metaname,
         columnname, algname, is_masked, outputfile, inventory))


@column.command()
@click.option(
    '--columnname', required=True,
    help="Column name for masking algorithm to set")
@click.option(
    '--metaname', help="Metaname (table/file) for masking algorithm to set")
@click.option(
    '--rulesetname', required=True,
    help="Ruleset name for masking algorithm to set")
@click.option(
    '--envname', help="Environment name for masking algorithm to set")
@click.option(
    '--algname', required=True,
    help="Name of algoritm to set for column")
@click.option(
    '--domainname', required=True,
    help="Name of domain to set for column")
@click.option(
    '--dateformat',
    help="Date format for DATE algorithms")
@click.option(
    '--idmethod', type=click.Choice(['Y', 'N']),
    help="Can a column be overwrite by profiler")
@common_options
@pass_state
def setmasking(dxm_state, rulesetname, envname, metaname, columnname, algname,
               domainname, dateformat, idmethod):
    """
    Setting a masking algorithm for defined column and flagging column as
    masked.
    Return non-zero return code if there was a problem with setting masking.
    """
    DxConfig(dxm_state.configfile)
    exit(column_setmasking(dxm_state.engine, dxm_state.engineuser, rulesetname, envname,
         metaname, columnname, algname, domainname, dateformat, idmethod))


@column.command()
@click.option(
    '--columnname', required=True,
    help="Column name for masking algorithm to unset")
@click.option(
    '--metaname', help="Metaname (table/file) for masking algorithm to unset")
@click.option(
    '--rulesetname', required=True,
    help="Ruleset name for masking algorithm to unset")
@click.option(
    '--envname', help="Environment name for masking algorithm to unset")
@common_options
@pass_state
def unsetmasking(dxm_state, rulesetname, envname, metaname, columnname):
    """
    Deleting a masking algorithm from defined column and flagging column as
    unmasked.
    Return non-zero return code if there was a problem with setting unmasking.
    """
    DxConfig(dxm_state.configfile)
    exit(column_unsetmasking(dxm_state.engine, dxm_state.engineuser, rulesetname, envname,
         metaname, columnname))


@column.command()
@click.option(
    '--newalgname', required=True,
    help="New algothitm to set")
@click.option(
    '--newdomain', required=True,
    help="New domain to set")
@click.option(
    '--algname', required=True, help="Filter algorithm to change")
@click.option(
    '--columnname', help="Filter column name to change")
@click.option(
    '--rulesetname', help="Ruleset name for masking algorithm to change")
@click.option(
    '--envname', help="Environment name for masking algorithm to change")
@click.option(
    '--metaname', help="Metaname (table/file) for masking algorithm to change")
@sort_options()
@common_options
@pass_state
def replace(dxm_state, rulesetname, envname, metaname, columnname, algname,
            newalgname, newdomain, sortby):
    """
    Change an algorithm for column(s) from algname to newalgname.
    Return non-zero return code if there was a problem with changing algorithm
    """
    DxConfig(dxm_state.configfile)
    exit(column_replace(dxm_state.engine, dxm_state.engineuser, rulesetname, envname, metaname,
         columnname, algname, newalgname, newdomain))


@column.command()
@click.option(
    '--rulesetname', required=True,
    help="Ruleset name for masking algorithm to batch set")
@click.option(
    '--envname', help="Environment name for masking algorithm to batch set")
@click.option(
    '--inputfile', type=click.File('rt'), required=True,
    help="Input file for batch set")
@click.option('--inventory', help="Input is compatible with GUI inventory",
              is_flag=True)
@common_options
@pass_state
def batch(dxm_state, rulesetname, envname, inputfile, inventory):
    """
    Set / unset masking for columns specified in CSV file.

    File format for databases rulesets is a part
    of GUI inventory export format:

    Table Name, Type, Parent Column Name, Column Name, Data Type, Domain, Algorithm, Is Masked, ID method, Row Type, Date Format

    Columns: Type, Parent Column Name, Data Type, Row Type are IGNORED.

    Ex. database ruleset input file:

    #Table Name,Type,Parent Column Name,Column name,Data Type,Domain,Algorithm,Is masked,ID Method,Row type,Date Format
    EMP,,,ENAME,VARCHAR2(10),LAST_NAME,LastNameLookup,Y,User,All Row,yyyy-MM-dd
    DEPT,IX,-,DEPTNO,NUMBER(2),,,N,Auto,All Row,-

    File format for file rulesets is a part of GUI inventory export format:

    File Name, Field Name, Domain, Algorithm, Is Masked, Priority,Record Type,Position,Length,Date Format

    Ex. file ruleset input file:

    #File Name,Field Name,Domain,Algorithm,Is masked,Priority,Record Type,Position,Length,Date Format
    1.txt,col1,ADDRESS,AddrLookup,Y,-,All Records,1,0,
    1.txt,col2,,,N,-,All Records,2,0,-
    1.txt,col3,,,N,-,All Records,3,0,-


    """
    DxConfig(dxm_state.configfile)
    exit(column_batch(dxm_state.engine, dxm_state.engineuser, rulesetname, envname, inputfile,
                      inventory))


@algorithms.command()
@click.option('--algname', help="Filter list based on algorithm name")
@common_options
@pass_state
def list(dxm_state, algname):
    """
    Display a list algorithms.
    Output list will be limited by value of --algname options if set
    and return non-zero return code if algname is not found.
    """
    DxConfig(dxm_state.configfile)
    exit(algorithm_list(dxm_state.engine, dxm_state.engineuser, dxm_state.format, algname))


# @algorithms.command()
# @click.option('--algname', help="Filter list based on algorithm name")
# @common_options
# @pass_state
# def export(dxm_state, algname):
#     """
#     Display a list algorithms.
#     Output list will be limited by value of --algname options if set
#     and return non-zero return code if algname is not found.
#     """
#     DxConfig(dxm_state.configfile)
#     exit(algorithm_export(dxm_state.engine, dxm_state.engineuser, algname, None))
#
#
# @algorithms.command()
# @click.option('--algname', help="Filter list based on algorithm name")
# @common_options
# @pass_state
# def load(dxm_state, algname):
#     """
#     Display a list algorithms.
#     Output list will be limited by value of --algname options if set
#     and return non-zero return code if algname is not found.
#     """
#     DxConfig(dxm_state.configfile)
#     exit(algorithm_import(dxm_state.engine, dxm_state.engineuser, None))


@meta.command()
@click.option(
    '--rulesetname', help="Filter ruleset name for metadata details")
@click.option(
    '--envname', help="Filter environment name for metadata details")
@click.option(
    '--metaname', help="Filter table name for table details")
@common_options
@pass_state
def list_table_details(dxm_state, rulesetname, envname, metaname):
    """
    Display table details.
    Output list will be limited by value of --rulesetname, --envname
    or --metaname options if set
    and return non-zero return code if metaname is not found.
    """
    DxConfig(dxm_state.configfile)
    exit(tab_listtable_details(
        dxm_state.engine,
        dxm_state.engineuser,
        dxm_state.format,
        rulesetname,
        envname,
        metaname))


@meta.command()
@click.option(
    '--rulesetname', help="Filter ruleset name for metadata details")
@click.option(
    '--envname', help="Filter environment name for metadata details")
@click.option(
    '--metaname', help="Filter file name for file details")
@common_options
@pass_state
def list_file_details(dxm_state, rulesetname, envname, metaname):
    """
    Display file details.
    Output list will be limited by value of --rulesetname, --envname
    or --metaname options if set
    and return non-zero return code if metaname is not found.
    """
    DxConfig(dxm_state.configfile)
    exit(tab_listfile_details(
        dxm_state.engine,
        dxm_state.engineuser,
        dxm_state.format,
        rulesetname,
        envname,
        metaname))


@meta.command()
@click.option(
    '--rulesetname', help='Ruleset name where table or file will be updated')
@click.option(
    '--envname', help="Environment name where ruleset exist")
@click.option(
    '--metaname', required=True,
    help="Name of table or file to be updated")
@click.option(
    '--custom_sql', help="Custom SQL specified for table")
@click.option(
    '--where_clause', help="Where clause specified for table")
@click.option(
    '--having_clause', help="Having clause specified for table")
@click.option(
    '--key_column', help="Key column specified for table")
@click.option(
    '--file_format', help="File format of updated file")
@click.option(
    '--file_delimiter', help="Delimited used in updated file")
@click.option(
    '--file_eor', type=click.Choice(['linux', 'windows', 'custom']),
    help="End of record used in file. For custom value file_eor_custom"
    " is needed")
@click.option(
    '--file_eor_custom', help="Custom end of record in updated file")
@click.option(
    '--file_enclosure', help="Enclosure of fields in updated file")
@click.option(
    '--file_name_regex', is_flag=True,
    help="Flag is file name is a regular expression and not a single"
    "file name")
@common_options
@pass_state
def update(dxm_state, rulesetname, metaname, custom_sql, where_clause,
           having_clause, key_column, file_format,
           file_delimiter, file_eor, file_enclosure, file_name_regex,
           file_eor_custom, envname):
    """
    Update table or file in ruleset
    Return non-zero code if there was a problem with adding table or file
    """
    params = {
        "rulesetname": rulesetname,
        "metaname": metaname,
        "custom_sql": custom_sql,
        "where_clause": where_clause,
        "having_clause": having_clause,
        "key_column": key_column,
        "file_format": file_format,
        "file_delimiter": file_delimiter,
        "file_eor": file_eor,
        "file_enclosure": file_enclosure,
        "file_name_regex": file_name_regex,
        "file_eor_custom": file_eor_custom,
        "envname": envname
    }
    DxConfig(dxm_state.configfile)
    exit(tab_update_meta(dxm_state.engine, dxm_state.engineuser, params))


@profileset.command()
@click.option(
    '--profilename', help="Profile set name")
@common_options
@pass_state
def list(dxm_state, profilename):
    """
    Display profile list.
    Output list will be limited by value of --profilename options if set
    and return non-zero return code if profilename is not found.
    """
    DxConfig(dxm_state.configfile)
    exit(profile_list(
            dxm_state.engine, profilename, None, dxm_state.format, None))


@profileset.command()
@click.option(
    '--profilename', help="Profile set name")
@click.option(
    '--exportfile', type=click.File('wt'), required=True,
    help="Name with path of export file")
@common_options
@pass_state
def export(dxm_state, profilename, exportfile):
    """
    Export profile with expression list into csv file with the following format
    profile_name,expression_name
    File name has to be provided using exportfile option.
    Output list will be limited by value of --profilename options if set
    and return non-zero return code if profilename is not found.
    """
    DxConfig(dxm_state.configfile)
    exit(profile_export(dxm_state.engine, dxm_state.engineuser, profilename, exportfile))


@profileset.command()
@click.option(
    '--profilename', help="Profile set name")
@click.option(
    '--expressionname', help="Expression name")
@common_options
@pass_state
def listmapping(dxm_state, profilename, expressionname):
    """
    Display profile with expression used by it.
    Output list will be limited by value of --profilename or expressionname
    options if set and return non-zero return code if profilename or
    expressionname is not found.
    """
    DxConfig(dxm_state.configfile)
    exit(profile_list(
            dxm_state.engine,
            dxm_state.engineuser,
            profilename,
            expressionname,
            dxm_state.format,
            True))


@profileset.command()
@click.option(
    '--profilename', help="Profile set name", required=True)
@click.option(
    '--expressionname', help="Expression name", multiple=True, required=True)
@click.option(
    '--description', help="Profile set description")
@common_options
@pass_state
def add(dxm_state, profilename, expressionname, description):
    """
    Add new profile. At least one expressionname is required.
    """
    DxConfig(dxm_state.configfile)
    exit(profile_add(
            dxm_state.engine,
            dxm_state.engineuser,
            profilename,
            expressionname,
            description))


@profileset.command()
@click.option(
    '--profilename', help="Profile set name", required=True)
@common_options
@pass_state
def delete(dxm_state, profilename):
    """
    Delete an existing profile.
    """
    DxConfig(dxm_state.configfile)
    exit(profile_delete(
            dxm_state.engine,
            dxm_state.engineuser,
            profilename))


@profileset.command()
@click.option(
    '--profilename', help="Profile set name", required=True)
@click.option(
    '--expressionname', help="Expression name [can be use multiple times]",
    multiple=True, required=True)
@common_options
@pass_state
def addexpression(dxm_state, profilename, expressionname):
    """
    Add expression to an existing profile.
    """
    DxConfig(dxm_state.configfile)
    exit(profile_addexpression(
            dxm_state.engine,
            dxm_state.engineuser,
            profilename,
            expressionname))


@profileset.command()
@click.option(
    '--profilename', help="Profile set name", required=True)
@click.option(
    '--expressionname', help="Expression name [can be use multiple times]",
    multiple=True, required=True)
@common_options
@pass_state
def deleteexpression(dxm_state, profilename, expressionname):
    """
    Delete expression from an existing profile.
    """
    DxConfig(dxm_state.configfile)
    exit(profile_deleteexpression(
            dxm_state.engine,
            dxm_state.engineuser,
            profilename,
            expressionname))

@expression.command()
@click.option(
    '--expressionname', help="Expression name")
@common_options
@pass_state
def list(dxm_state, expressionname):
    """
    Display expressions
    Output list will be limited by value of expressionname
    options if set and return non-zero return code if expressionname
    is not found.
    """
    DxConfig(dxm_state.configfile)
    exit(expression_list(
            dxm_state.engine,
            dxm_state.engineuser,
            expressionname,
            dxm_state.format))


@expression.command()
@click.option(
    '--expressionname', help="Expression name", required=True)
@click.option(
    '--domainname', required=True,
    help="Name of domain to set for column")
@click.option(
    '--level', type=click.Choice(['column', 'data']), default="column",
    help="Set level expression of expression. Default - column")
@click.option(
    '--regex', required=True,
    help="Regular expression to set")
@common_options
@pass_state
def add(dxm_state, expressionname, domainname, level, regex):
    """
    Add new expresson to engine
    """
    DxConfig(dxm_state.configfile)
    exit(expression_add(
            dxm_state.engine,
            dxm_state.engineuser,
            expressionname,
            domainname,
            level,
            regex))


@expression.command()
@click.option(
    '--expressionname', help="Expression name", required=True)
@common_options
@pass_state
def delete(dxm_state, expressionname):
    """
    Delete expresson from engine
    """
    DxConfig(dxm_state.configfile)
    exit(expression_delete(
            dxm_state.engine,
            dxm_state.engineuser,
            expressionname))


@expression.command()
@click.option(
    '--expressionname', help="Expression name", required=True)
@click.option(
    '--domainname',
    help="Name of domain to set for column")
@click.option(
    '--level', type=click.Choice(['column', 'data']), default="column",
    help="Set level expression of expression. Default - column")
@click.option(
    '--regex',
    help="Regular expression to set")
@common_options
@pass_state
def update(dxm_state, expressionname, domainname, level, regex):
    """
    Update an existing expresson on engine
    """
    DxConfig(dxm_state.configfile)
    exit(expression_update(
            dxm_state.engine,
            dxm_state.engineuser,
            expressionname,
            domainname,
            level,
            regex))

@profilejob.command()
@click.option('--jobname', help="Filter jobs using jobname")
@click.option('--envname', help='Filter jobs belongs to one environment')
@common_options
@pass_state
def list(dxm_state, jobname, envname):
    """
    Display list of jobs defined in Masking Engine

    If no filter options are specified, all jobs will be displayed.
    If --envname or --jobname is set, output list will
    be limited by value of this option and return non-zero return code
    if jobname is not found.
    """
    DxConfig(dxm_state.configfile)
    exit(profilejobs_list(dxm_state.engine, dxm_state.engineuser, jobname, envname, dxm_state.format))



@profilejob.command()
@click.option('--jobname', help="Filter jobs using jobname")
@click.option('--envname', help='Filter jobs belongs to one environment')
@click.option('--last', help='Display only last execution', is_flag=True)
@click.option('--details', help='Display execution details', is_flag=True, default=False)
@click.option('--startdate', help='Display jobs started after startdate', type=click.DateTime())
@click.option('--enddate', help='Display jobs finished before enddate', type=click.DateTime())
@common_options
@pass_state
def report(dxm_state, jobname, envname, last, startdate, enddate, details):
    """
    Display report of jobs defined in Masking Engine

    If no filter options are specified, all jobs will be displayed.
    If --envname or --jobname is set, output list will
    be limited by value of this option and return non-zero return code
    if jobname is not found.
    """
    DxConfig(dxm_state.configfile)
    exit(profilejobs_report(dxm_state.engine, dxm_state.engineuser, jobname, envname, dxm_state.format, 
                     last, startdate, enddate, details))

@profilejob.command()
@click.option(
    '--jobname', required=True, help="Name of job to update", multiple=True)
@click.option(
    '--envname', help="Name of environment where job will be started")
@click.option('--nowait', is_flag=True, help="No wait for job to finish")
@click.option(
    '--parallel', type=int, help="Number of parallel jobs",
    default=1
)
@click.option(
    '--tgt_connector', help="Name of target connector for multi tenant job")
@click.option(
    '--tgt_connector_env', help="Name of target connector environment "
    "for multi tenant job")
@click.option('--monitor', is_flag=True, help="Display progress bars")
@common_options
@pass_state
def start(dxm_state, jobname, envname,
          nowait, parallel, monitor, tgt_connector, tgt_connector_env):
    """
    Start masking job. By default control is returned when job is finished.
    If --nowait flag is specified script doesn't monitor job and release
    control after job is started.
    """
    DxConfig(dxm_state.configfile)
    exit(profilejob_start(dxm_state.engine, dxm_state.engineuser, jobname, envname,
                          nowait, parallel, monitor, tgt_connector,
                          tgt_connector_env))

@profilejob.command()
@click.option(
    '--jobname', required=True, help="Name of source job")
@click.option(
    '--envname', help="Name of environment for source and target job")
@click.option(
    '--newjobname', required=True, help="Name of target job")
@common_options
@pass_state
def copy(dxm_state, jobname, envname, newjobname):
    """
    Copy an existing job to a new one.
    Return non zero code if there was problem with canceling a job
    """
    DxConfig(dxm_state.configfile)
    exit(profilejob_copy(dxm_state.engine, dxm_state.engineuser, jobname, envname, newjobname))

@profilejob.command()
@click.option(
    '--jobname', required=True, help="Name of job to add")
@click.option(
    '--envname', required=True,
    help="Name of environment where job will be added")
@click.option(
    '--rulesetname', required=True,
    help="Name of ruleset which will be used for masking job")
@click.option(
    '--profilename', required=True,
    help="Name of profileset to be executed in job")
@click.option(
    '--jobdesc', help="Desciption of the job")
@click.option(
    '--email', help="e-mail address used for job notification")
@click.option(
    '--feedback_size', type=int,
    help="Feedback size of masking job")
@click.option(
    '--max_memory', type=int,
    help="Maximum size of memory used by masking job")
@click.option(
    '--min_memory', type=int,
    help="Minimum size of memory used by masking job")
@click.option(
    '--num_streams', type=int,
    help="Number of concurrent objects (tables/files) being masked by job")
@click.option(
    '--multi_tenant', type=click.Choice(['Y', 'N']),
    help="Define job as multi-tenant")
@common_options
@pass_state
def add(dxm_state, jobname, envname, rulesetname, email, feedback_size,
        max_memory, min_memory, jobdesc, num_streams, profilename,
        multi_tenant):
    """
    Add a new profile job to Masking engine

    List of required parameters:

    \b
        jobname
        envname
        rulesetname
        profilename

    Return non zero code if there was problem with adding a new job
    """

    params = {
        "envname": envname,
        "jobname": jobname,
        "rulesetname": rulesetname,
        "profilename": profilename,
        "email": email,
        "feedback_size": feedback_size,
        "max_memory": max_memory,
        "min_memory": min_memory,
        "job_description": jobdesc,
        "num_input_streams": num_streams,
        "multi_tenant": multi_tenant
    }
    DxConfig(dxm_state.configfile)
    exit(profilejob_add(dxm_state.engine, dxm_state.engineuser, params))

@profilejob.command()
@click.option('--jobname', required=True, help="Name of job to update")
@click.option(
    '--envname', help="Name of environment where job will be updated")
@click.option(
    '--rulesetname', help="Name of ruleset which will be used for masking job")
@click.option(
    '--profilename',
    help="Name of profileset to be executed in job")
@click.option(
    '--jobdesc', help="Desciption of the job")
@click.option(
    '--email', help="e-mail address used for job notification")
@click.option(
    '--feedback_size', type=int,
    help="Feedback size of masking job")
@click.option(
    '--max_memory', type=int,
    help="Maximum size of memory used by masking job")
@click.option(
    '--min_memory', type=int,
    help="Minimum size of memory used by masking job")
@click.option(
    '--num_streams', type=int,
    help="Number of concurrent objects (tables/files) being masked by job")
@click.option(
    '--multi_tenant', type=click.Choice(['Y', 'N']),
    help="Define job as multi-tenant")
@common_options
@pass_state
def update(dxm_state, jobname, envname, rulesetname, email, feedback_size,
           max_memory, min_memory, jobdesc, num_streams, profilename,
           multi_tenant):
    """
    Update an existing proflejob on Masking engine
    Return non zero code if there was problem with updating a job
    """

    params = {
        "envname": envname,
        "jobname": jobname,
        "rulesetname": rulesetname,
        "profilename": profilename,
        "email": email,
        "feedback_size": feedback_size,
        "max_memory": max_memory,
        "min_memory": min_memory,
        "job_description": jobdesc,
        "num_input_streams": num_streams,
        "multi_tenant": multi_tenant
    }
    DxConfig(dxm_state.configfile)
    exit(profilejob_update(dxm_state.engine, dxm_state.engineuser, jobname, envname, params))

@profilejob.command()
@click.option(
    '--jobname', required=True, help="Name of job to be deleted")
@click.option(
    '--envname', help="Name of environment where job will be deleted")
@common_options
@pass_state
def delete(dxm_state, jobname, envname):
    """
    Delete an existing job from Masking Engine.
    Return non zero code if there was problem with deleting a job
    """
    DxConfig(dxm_state.configfile)
    exit(profilejob_delete(dxm_state.engine, dxm_state.engineuser, jobname, envname))


# doesn't work with profile job
# @profilejob.command()
# @click.option(
#     '--jobname', required=True, help="Name of job to be canceled")
# @click.option(
#     '--envname', help="Name of environment where job will be canceled")
# @common_options
# @pass_state
# def cancel(dxm_state, jobname, envname):
#     """
#     Cancel execution of running job.
#     Return non zero code if there was problem with canceling a job
#     """
#     DxConfig(dxm_state.configfile)
    exit(profilejob_cancel(dxm_state.engine, dxm_state.engineuser, jobname, envname))

@sync.command()
@click.option('--objectname', help="Filter object using a name")
@click.option('--objecttype', help="Filter object using a type",
              type=click.Choice(
                supported_sync_objects_type
              ))
@click.option('--envname', help="Filter using a environment name")
@common_options
@pass_state
def list(dxm_state, objecttype, objectname, envname):
    """
    Display list of syncable objects from Masking Engine

    If no filter options are specified, all objects types will be displayed.
    """
    DxConfig(dxm_state.configfile)
    exit(sync_list(dxm_state.engine, dxm_state.engineuser, objecttype, objectname,
                   envname, dxm_state.format))

@sync.command()
@click.option('--objecttype', help="Filter object using a type", 
              type=click.Choice(
                supported_sync_objects_type
              ))
@click.option('--objectname', help="Filter object using a name")
@click.option('--envname', help="Filter using a environment name")
@click.option('--path', help="Path to export", required=True)
@common_options
@pass_state
def export(dxm_state, objecttype, objectname, envname, path):
    """
    Export an object to file in specified path
    """
    DxConfig(dxm_state.configfile)
    exit(sync_export(dxm_state.engine, dxm_state.engineuser, objecttype, objectname,
                     envname, path))


@sync.command()
@click.option('--target_envname', help="Target environment name "
              "(ignored for global obejcts)")
@click.option('--force', is_flag=True, default=False,
              help="Force object overwrite")
@click.option(
    '--inputfile', type=click.File('rb'),
    help="Name with path to imported object")
@click.option('--inputpath', help="Path to object to load")
@common_options
@pass_state
def load(dxm_state, target_envname, inputfile, inputpath, force):
    """
    Load an object from file into Masking Engine
    """
    DxConfig(dxm_state.configfile)
    exit(sync_import(dxm_state.engine, dxm_state.engineuser, target_envname, inputfile,
                     inputpath, force))

@role.command()
@click.option('--rolename', help="Filter roles using a name")
@common_options
@pass_state
def list(dxm_state, rolename):
    """
    Display list of roles from Masking Engine

    If no filter options are specified, all roles will be displayed.
    """
    DxConfig(dxm_state.configfile)
    exit(role_list(dxm_state.engine, dxm_state.engineuser, dxm_state.format, rolename))


@user.command()
@click.option('--username', help="Filter users using a name")
@common_options
@pass_state
def list(dxm_state, username):
    """
    Display list of users from Masking Engine

    If no filter options are specified, all users will be displayed.
    """
    DxConfig(dxm_state.configfile)
    exit(user_list(dxm_state.engine, dxm_state.engineuser, dxm_state.format, username))

@user.command()
@click.option('--username', help="User name", required=True)
@click.option('--firstname', help="User first name", required=True)
@click.option('--lastname', help="User last name", required=True)
@click.option('--email', help="User email", required=True)
@click.option(
    '--password', prompt=True, hide_input=True, confirmation_prompt=True,
    help='Password for specified user. If you want to hide input'
    ' don''t specify this parameter and you will be propted')
@click.option('--user_type', help="User type ( admin / nonadmin)",
              required=True, type=click.Choice(['admin', 'nonadmin']))
@click.option('--user_role', help="User role")
@click.option('--user_environments', help="User environments")
@common_options
@pass_state
def add(dxm_state, username, firstname, lastname, email, password, user_type,
        user_environments, user_role):
    """
    Add user to Masking Engine
    """
    DxConfig(dxm_state.configfile)
    exit(user_add(dxm_state.engine, dxm_state.engineuser, username, firstname, lastname, email,
                  password, user_type, user_environments, user_role))

@user.command()
@click.option('--username', help="Filter users using a name")
@click.option('--force', is_flag=True, help="Force user deletion for admin users")
@common_options
@pass_state
def delete(dxm_state, username, force):
    """
    Delete an user from Masking Engine
    To delete admin user, please use force option. Use this with care !!!
    """
    DxConfig(dxm_state.configfile)
    exit(user_delete(dxm_state.engine, dxm_state.engineuser, username, force))

@user.command()
@click.option('--username', help="User name", required=True)
@click.option('--firstname', help="User first name")
@click.option('--lastname', help="User last name")
@click.option('--email', help="User email")
@click.option(
    '--password',
    help='Password for specified user.'
    'If you want to hide input put '' as value and you will be propted')
@click.option('--user_type', help="User type ( admin / nonadmin)",
              type=click.Choice(['admin', 'nonadmin']))
@click.option('--user_role', help="User role")
@click.option('--user_environments', help="User environments")
@common_options
@pass_state
def update(dxm_state, username, firstname, lastname, email, password, user_type,
           user_environments, user_role):
    """
    Update user in Masking Engine
    """
    if password == '':
        password = click.prompt('Please enter a password', hide_input=True,
                                confirmation_prompt=True)
    DxConfig(dxm_state.configfile)
    exit(user_update(dxm_state.engine, dxm_state.engineuser, username, firstname, lastname, email,
                     password, user_type, user_environments, user_role))

@domain.command()
@click.option('--domainname', help="Filter domains using a name")
@common_options
@pass_state
def list(dxm_state, domainname):
    """
    Display list of domains from Masking Engine

    If no filter options are specified, all domains will be displayed.
    """
    DxConfig(dxm_state.configfile)
    exit(domain_list(dxm_state.engine, dxm_state.engineuser, dxm_state.format, domainname))


@domain.command()
@click.option('--domainname', help="Domain name to add", required=True)
@click.option('--classification', help="Domain classification", required=True,
              type=click.Choice(['CUSTOMER', 'EMPLOYEE', 'COMPANY']))
@click.option('--algname', help="Default algorithm name", required=True)
@common_options
@pass_state
def add(dxm_state, domainname, classification, algname):
    """
    Add a domain to the Masking Engine

    If no filter options are specified, all domains will be displayed.
    """
    DxConfig(dxm_state.configfile)
    exit(domain_add(dxm_state.engine, dxm_state.engineuser, domainname, classification, algname))

@domain.command()
@click.option('--domainname', help="Domain name to delete", required=True)
@common_options
@pass_state
def delete(dxm_state, domainname):
    """
    Delete the domain from the Masking Engine
    """
    DxConfig(dxm_state.configfile)
    exit(domain_delete(dxm_state.engine, dxm_state.engineuser, domainname))

@domain.command()
@click.option('--domainname', help="Domain name to update", required=True)
@click.option('--classification', help="Domain classification",
              type=click.Choice(['CUSTOMER', 'EMPLOYEE', 'COMPANY']))
@click.option('--algname', help="Default algorithm name")
@common_options
@pass_state
def update(dxm_state, domainname, classification, algname):
    """
    Update the domain in the Masking Engine

    """
    DxConfig(dxm_state.configfile)
    exit(domain_update(dxm_state.engine, dxm_state.engineuser, domainname, classification, algname))


@jdbc.command()
@click.option('--driver_name', help="Filter jdbc drivers using a name")
@common_options
@pass_state
def list(dxm_state, driver_name):
    """
    Display list of JDBC drivers from Masking Engine

    If no filter options are specified, all drivers will be displayed.
    """
    DxConfig(dxm_state.configfile)
    exit(driver_list(dxm_state.engine, dxm_state.engineuser, dxm_state.format, driver_name))


@jdbc.command()
@click.option('--driver_name', help="Name of JDBC driver to add", required=True)
@click.option('--driver_class', help="Name of JDBC driver class to add", required=True)
@click.option('--driver_file', help="Path to driver JAR file", required=True)
@common_options
@pass_state
def add(dxm_state, driver_name, driver_class, driver_file):
    """
    Add JDBC driver to Delphix Engine
    """
    DxConfig(dxm_state.configfile)
    exit(driver_add(dxm_state.engine, dxm_state.engineuser, driver_name, driver_class, driver_file))

@jdbc.command()
@click.option('--driver_name', help="Filter jdbc drivers using a name", required=True)
@common_options
@pass_state
def delete(dxm_state, driver_name):
    """
    Delete JDBC driver from Delphix Engine
    """
    DxConfig(dxm_state.configfile)
    exit(driver_delete(dxm_state.engine, dxm_state.engineuser, driver_name))