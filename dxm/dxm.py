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
from lib.DxApplication.app_worker import application_list
from lib.DxApplication.app_worker import application_add
from lib.DxEnvironment.env_worker import environment_list
from lib.DxEnvironment.env_worker import environment_add
from lib.DxEnvironment.env_worker import environment_delete
from lib.DxConnector.conn_worker import connector_list
from lib.DxConnector.conn_worker import connector_add
from lib.DxConnector.conn_worker import connector_delete
# from lib.DxConnector.conn_worker import connector_update
from lib.DxConnector.conn_worker import connector_test
from lib.DxConnector.conn_worker import connector_fetch
from lib.DxRuleset.rule_worker import ruleset_list
from lib.DxRuleset.rule_worker import ruleset_add
from lib.DxRuleset.rule_worker import ruleset_delete
from lib.DxRuleset.rule_worker import ruleset_clone
from lib.DxRuleset.rule_worker import ruleset_export
from lib.DxRuleset.rule_worker import ruleset_import
from lib.DxRuleset.rule_worker import ruleset_check
from lib.DxRuleset.rule_worker import ruleset_addmeta
from lib.DxRuleset.rule_worker import ruleset_listmeta
from lib.DxRuleset.rule_worker import ruleset_deletemeta
from lib.DxEngine.eng_worker import engine_add
from lib.DxEngine.eng_worker import engine_list
from lib.DxEngine.eng_worker import engine_delete
from lib.DxEngine.eng_worker import engine_update
from lib.DxEngine.eng_worker import engine_logout
from lib.DxEngine.eng_worker import engine_logs
from lib.DxJobs.jobs_worker import jobs_list
from lib.DxJobs.jobs_worker import job_add
from lib.DxJobs.jobs_worker import job_start
from lib.DxJobs.jobs_worker import job_delete
from lib.DxJobs.jobs_worker import job_copy
from lib.DxJobs.jobs_worker import job_update
from lib.DxJobs.jobs_worker import job_cancel
from lib.DxColumn.column_worker import column_list
from lib.DxColumn.column_worker import column_setmasking
from lib.DxColumn.column_worker import column_unsetmasking
from lib.DxColumn.column_worker import column_replace
from lib.DxColumn.column_worker import column_batch
from lib.DxColumn.column_worker import column_save
from lib.DxFileFormat.fileformat_worker import fileformat_add
from lib.DxFileFormat.fileformat_worker import fileformat_list
from lib.DxFileFormat.fileformat_worker import fileformat_delete
from lib.DxAlgorithm.alg_worker import algorithm_list
from lib.DxAlgorithm.alg_worker import algorithm_export
from lib.DxAlgorithm.alg_worker import algorithm_import
from lib.DxTable.tab_worker import tab_listtable_details
from lib.DxTable.tab_worker import tab_listfile_details
from lib.DxTable.tab_worker import tab_update_meta
from lib.DxProfile.profile_worker import profile_list
from lib.DxProfile.profile_worker import expression_list
from lib.DxProfile.profile_worker import expression_add
from lib.DxProfile.profile_worker import expression_delete
from lib.DxProfile.profile_worker import expression_update
from lib.DxProfile.profile_worker import profile_add
from lib.DxProfile.profile_worker import profile_delete
from lib.DxProfile.profile_worker import profile_export
from lib.DxProfile.profile_worker import profile_addexpression
from lib.DxProfile.profile_worker import profile_deleteexpression
from lib.DxJobs.jobs_worker import profilejobs_list
from lib.DxJobs.jobs_worker import profilejob_start
from lib.DxJobs.jobs_worker import profilejob_copy
from lib.DxJobs.jobs_worker import profilejob_add
from lib.DxJobs.jobs_worker import profilejob_update
from lib.DxJobs.jobs_worker import profilejob_delete
from lib.DxJobs.jobs_worker import profilejob_cancel
from lib.DxSync.sync_worker import sync_list
from lib.DxSync.sync_worker import sync_export
from lib.DxSync.sync_worker import sync_import

# from lib.DxLogging import print_error
from lib.DxLogging import logging_est

__version__ = 0.3

class dxm_state(object):

    def __init__(self):
        self.logfile = "dxm.log"
        self.debug = False
        self.engine = None
        self.format = None


pass_state = click.make_pass_decorator(dxm_state, ensure=True)


def debug_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(dxm_state)
        state.debug = value
        logging_est(state.logfile, state.debug)
        return value
    return click.option('--debug',
                        is_flag=True,
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


def common_options(f):
    f = logfile_option(f)
    f = debug_option(f)
    f = engine_option(f)
    f = format_option(f)
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

@engine.command()
@click.option('--engine', help='Engine name (or alias)', required=True)
@click.option('--ip',  help='IP or FQDN of engine', required=True)
@click.option(
    '--port', help='Port used by engine (default 8282)', default=8282,
    required=True)
@click.option(
    '--protocol', help='Communication protocol (default http)', default='http',
    required=True, type=click.Choice(['http', 'https']))
@click.option(
    '--username', default='delphix_admin', required=True,
    help='Username used by toolkit (default delphix_admin)')
@click.option(
    '--default', help='Setting engine as default engine for toolkit'
    ' (Default value N)', type=click.Choice(['Y', 'N']), default='N')
@click.option(
    '--password', prompt=True, hide_input=True,
    confirmation_prompt=True, required=True,
    help='Engine password for specified user. If you want to hide input'
    ' don''t specify this parameter and you will be propted')
@logfile_option
@pass_state
def add(dxm_state, engine, ip, port, protocol, username, password, default):
    """
    Add engine entry to configuration database
    """
    engine_add(engine, ip, username, password,
               protocol, port, default)


@engine.command()
@click.option('--engine', help='Engine name (or alias)', required=True)
@click.option('--ip', help='IP or FQDN of engine')
@click.option('--port', help='Port used by engine (default 8282)')
@click.option(
    '--protocol', help='Communication protocol',
    type=click.Choice(['http', 'https']))
@click.option(
    '--username', help='Username used by toolkit')
@click.option(
    '--default', help='Setting engine as default engine for toolkit',
    type=click.Choice(['Y', 'N']))
@click.option(
    '--password', help='Engine password for specified user. '
    'If you want to hide input put '' as value and you will be propted')
@debug_option
@pass_state
def update(dxm_state, engine, ip, port, protocol, username, password, default):
    """
    Update engine entry in configuration database
    """
    if password == '':
        password = click.prompt('Please enter a password', hide_input=True,
                                confirmation_prompt=True)
    exit(engine_update(engine, ip, username, password,
                  protocol, port, default))


@engine.command()
@click.option('--engine', help='Engine name (or alias)', required=True)
@debug_option
@pass_state
def logout(dxm_state, engine):
    """
    Logout user
    """
    exit(engine_logout(engine))


@engine.command()
@click.option('--username', help='Filter output by configured username')
@common_options
@pass_state
def list(dxm_state, username):
    """
    List entries from configuration database
    """
    exit(engine_list(dxm_state.engine, username, dxm_state.format))


@engine.command()
@common_options
@pass_state
def delete(dxm_state):
    """
    Delete entry from configuration database
    """
    exit(engine_delete(dxm_state.engine, None))


@engine.command()
@click.option(
    '--enginelog', type=click.File('wt'), required=True,
    help="Name with path of output logfile")
@common_options
@pass_state
def logs(dxm_state, enginelog):
    """
    Save Masking Engine log into file
    """
    exit(engine_logs(dxm_state.engine, enginelog))


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
    exit(application_list(dxm_state.engine, dxm_state.format, appname))


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
    exit(application_add(dxm_state.engine, appname))


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
    exit(environment_list(dxm_state.engine, dxm_state.format, envname))


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
    exit(environment_add(dxm_state.engine, envname, appname, purpose))


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
    exit(environment_delete(dxm_state.engine, envname))


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
    exit(connector_list(
        dxm_state.engine, dxm_state.format, envname, connectorname,
        details))


@connector.command()
@click.option('--connectorname', required=True, help='Connector name to add')
@click.option(
    '--envname', required=True,
    help='Environment name where connector will be added')
@click.option(
    '--connectortype',
    type=click.Choice(['oracle', 'sybase', 'mssql', 'delimited', 'excel',
                      'fixed_width', 'xml']),
    required=True, help='Type of the connector')
@click.option(
    '--host', required=True, help='Host where connector will be pointed')
@click.option(
    '--port', required=True, type=int,
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
@common_options
@pass_state
def add(dxm_state, connectorname, envname, connectortype, host, port, username,
        schemaname, password, sid, instancename, databasename, path,
        servertype):
    """
    Add connector to Masking Engine.
    List of required parameters depend on connector type:

    \b
        - database connectors:
            connectorname,
            envname,
            connectortype,
            host,
            port,
            username,
            schemaname,
        - database depended options:
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


    Exit code will be set to 0 if environment was added
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
        'servertype': servertype
    }
    exit(connector_add(dxm_state.engine, params))

# API issue - not in use now
# @connector.command()
# @click.option('--connectorname', required=True)
# @click.option('--host')
# @click.option('--port', type=int)
# @click.option('--username')
# @click.option('--schemaname')
# @click.option('--password')
# @click.option('--sid')
# @click.option('--instancename')
# @click.option('--databasename')
# @common_options
# @pass_state
# def update(dxm_state, connectorname, host, port, username,
#         schemaname, password, sid, instancename, databasename):
#     """ tobedone """
#     params = {
#         'schemaName': schemaname,
#         'host': host,
#         'port': port,
#         'password': password,
#         'username': username,
#         'connname': connectorname,
#         'sid': sid,
#         'instancename': instancename,
#         'databasename': databasename
#     }
#     exit(connector_update(dxm_state.engine, params))


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
    exit(connector_delete(dxm_state.engine, connectorname, envname))


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
    exit(connector_test(dxm_state.engine, connectorname, envname))


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
    exit(connector_fetch(dxm_state.engine, connectorname, envname))


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
    exit(ruleset_list(
        dxm_state.engine, dxm_state.format, rulesetname, envname))


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
    exit(ruleset_add(dxm_state.engine, rulesetname, connectorname, envname))


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
    exit(ruleset_delete(dxm_state.engine, rulesetname, envname))


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
    exit(ruleset_clone(dxm_state.engine, rulesetname, envname,
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
    exit(ruleset_export(
        dxm_state.engine, rulesetname, envname,
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
    Export
    """
    exit(ruleset_import(
        dxm_state.engine, inputfile, rulesetname, connectorname, envname))

@ruleset.command()
@click.option(
    '--inputfile', type=click.File('rt'), required=True,
    help="Name with path of input file where ruleset(s) will be imported from")
@common_options
@pass_state
def checkrule(dxm_state, inputfile):
    """
    Check
    """
    exit(ruleset_check(dxm_state.engine, inputfile))

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
@common_options
@pass_state
def addmeta(dxm_state, rulesetname, metaname, custom_sql, where_clause,
            having_clause, key_column, inputfile, file_format,
            file_delimiter, file_eor, file_enclosure, file_name_regex,
            file_eor_custom, envname):
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
        "envname": envname
    }
    exit(ruleset_addmeta(dxm_state.engine, params, inputfile))


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
    exit(ruleset_listmeta(
        dxm_state.engine, dxm_state.format, rulesetname, envname, metaname))


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
    exit(ruleset_deletemeta(dxm_state.engine, rulesetname, metaname, envname))


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
    exit(jobs_list(dxm_state.engine, jobname, envname, dxm_state.format))


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
    '--prescript', type=click.File('rt'),
    help="File name and path used as prescript")
@click.option(
    '--postscript', type=click.File('rt'),
    help="File name and path used as postscript")
@common_options
@pass_state
def add(dxm_state, jobname, envname, rulesetname, email, feedback_size,
        max_memory, min_memory, jobdesc, num_streams, on_the_fly,
        on_the_fly_source, commit_size, threads, multi_tenant, batch_update,
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
        "prescript": prescript,
        "postscript": postscript
    }
    exit(job_add(dxm_state.engine, params))


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
    '--prescript', type=click.File('rt'),
    help="File name and path used as prescript")
@click.option(
    '--postscript', type=click.File('rt'),
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
        "prescript": prescript,
        "postscript": postscript
    }
    exit(job_update(dxm_state.engine, jobname, envname, params))


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
    exit(job_start(dxm_state.engine, jobname, envname, tgt_connector,
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
    exit(job_delete(dxm_state.engine, jobname, envname))

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
#     exit(job_cancel(dxm_state.engine, jobname, envname))


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
    exit(job_copy(dxm_state.engine, jobname, envname, newjobname))


@fileformat.command()
@click.option('--fileformatname', required=True)
@common_options
@pass_state
def delete(dxm_state, fileformatname):
    """ FileFormat list """
    exit(fileformat_delete(dxm_state.engine, fileformatname))


@fileformat.command()
@click.option('--fileformattype', type=click.Choice(['DELIMITED', 'EXCEL',
                                                     'FIXED_WIDTH', 'XML']))
@click.option('--fileformatname')
@common_options
@pass_state
def list(dxm_state, fileformattype, fileformatname):
    """ FileFormat list """
    exit(fileformat_list(
        dxm_state.engine, dxm_state.format, fileformattype, fileformatname))


@fileformat.command()
@click.option('--fileformattype', required=True,
              type=click.Choice(['delimited', 'excel',
                                 'fixed_width', 'xml']))
@click.option('--fileformatfile', type=click.File('rt'), required=True)
@common_options
@pass_state
def add(dxm_state, fileformattype, fileformatfile):
    """ FileFormat add """
    exit(fileformat_add(dxm_state.engine, fileformattype, fileformatfile))


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
    exit(column_list(
        dxm_state.engine, dxm_state.format, sortby, rulesetname, envname,
        metaname, columnname, algname, is_masked))


@column.command()
@click.option('--columnname', help="Filter output by a column name")
@click.option(
    '--metaname', help="Filter output by a meta name (table or file name)")
@click.option('--rulesetname', help="Filter output by a ruleset name")
@click.option('--envname', help="Filter output by an environment name")
@click.option('--algname', help="Filter output by an algorithm name")
@click.option(
    '--is_masked', is_flag=True, help="Filter output to masked columns only")
@click.option(
    '--outputfile', type=click.File('wt'), required=True,
    help="Name with path of output file where masking inventory will be saved"
    " in CSV format")
@sort_options()
@common_options
@pass_state
def save(dxm_state, rulesetname, envname, metaname, columnname, algname,
         is_masked, sortby, outputfile):
    """
    Save column masking rules (inventory) into CSV file which can be loaded
    later using toolkit.
    """
    exit(column_save(dxm_state.engine, sortby, rulesetname, envname, metaname,
         columnname, algname, is_masked, outputfile))


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
@common_options
@pass_state
def setmasking(dxm_state, rulesetname, envname, metaname, columnname, algname,
               domainname):
    """
    Setting a masking algorithm for defined column and flagging column as
    masked.
    Return non-zero return code if there was a problem with setting masking.
    """
    exit(column_setmasking(dxm_state.engine, rulesetname, envname,
         metaname, columnname, algname, domainname))


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
    exit(column_unsetmasking(dxm_state.engine, rulesetname, envname,
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
    exit(column_replace(dxm_state.engine, rulesetname, envname, metaname,
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
@common_options
@pass_state
def batch(dxm_state, rulesetname, envname, inputfile):
    """
    Set / unset masking for columns specified in CSV file.

    File format is as follow:

    tablename, columnname, algorithm_name, domain_name, is_masked [Y|N]
    """
    exit(column_batch(dxm_state.engine, rulesetname, envname, inputfile))


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
    exit(algorithm_list(dxm_state.engine, dxm_state.format, algname))


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
#     exit(algorithm_export(dxm_state.engine, algname, None))
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
#     exit(algorithm_import(dxm_state.engine, None))


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
    exit(tab_listtable_details(
        dxm_state.engine,
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
    exit(tab_listfile_details(
        dxm_state.engine,
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
    exit(tab_update_meta(dxm_state.engine, params))


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
    exit(profile_export(dxm_state.engine, profilename, exportfile))


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
    exit(profile_list(
            dxm_state.engine,
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
    exit(profile_add(
            dxm_state.engine,
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
    exit(profile_delete(
            dxm_state.engine,
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
    exit(profile_addexpression(
            dxm_state.engine,
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
    exit(profile_deleteexpression(
            dxm_state.engine,
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
    exit(expression_list(
            dxm_state.engine,
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
    exit(expression_add(
            dxm_state.engine,
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
    exit(expression_delete(
            dxm_state.engine,
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
    exit(expression_update(
            dxm_state.engine,
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
    exit(profilejobs_list(dxm_state.engine, jobname, envname, dxm_state.format))

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
@click.option('--monitor', is_flag=True, help="Display progress bars")
@common_options
@pass_state
def start(dxm_state, jobname, envname,
          nowait, parallel, monitor):
    """
    Start masking job. By default control is returned when job is finished.
    If --nowait flag is specified script doesn't monitor job and release
    control after job is started.
    """
    exit(profilejob_start(dxm_state.engine, jobname, envname,
                          nowait, parallel, monitor))

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
    exit(profilejob_copy(dxm_state.engine, jobname, envname, newjobname))

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
    exit(profilejob_add(dxm_state.engine, params))

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
    exit(profilejob_update(dxm_state.engine, jobname, envname, params))

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
    exit(profilejob_delete(dxm_state.engine, jobname, envname))


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
#     exit(profilejob_cancel(dxm_state.engine, jobname, envname))

@sync.command()
@click.option('--objecttype', help="Filter object using a type")
@click.option('--objectname', help="Filter object using a name")
@click.option('--envname', help="Filter using a environment name")
@common_options
@pass_state
def list(dxm_state, objecttype, objectname, envname):
    """
    Display list of syncable objects from Masking Engine

    If no filter options are specified, all objects types will be displayed.
    """
    exit(sync_list(dxm_state.engine, objecttype, objectname,
                   envname, dxm_state.format))

@sync.command()
@click.option('--objecttype', help="Filter object using a type")
@click.option('--objectname', help="Filter object using a name")
@click.option('--envname', help="Filter using a environment name")
@common_options
@pass_state
def export(dxm_state, objecttype, objectname, envname):
    """
    Display list of syncable objects from Masking Engine

    If no filter options are specified, all objects types will be displayed.
    """
    exit(sync_export(dxm_state.engine, objecttype, objectname,
                   envname, dxm_state.format))


@sync.command()
@click.option('--target_envname', help="Filter using a environment name")
@common_options
@pass_state
def load(dxm_state, target_envname):
    """
    Display list of syncable objects from Masking Engine

    If no filter options are specified, all objects types will be displayed.
    """
    exit(sync_import(dxm_state.engine, target_envname, None))
