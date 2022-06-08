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


from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
import logging
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message
from dxm.lib.Output.DataFormatter import DataFormatter
from dxm.lib.DxTools.DxTools import get_list_of_engines

from dxm.lib.DxConnector.DxConnector import DxConnector
from dxm.lib.DxConnector.DxFileConnector import DxFileConnector
from dxm.lib.DxConnector.OracleConnector import OracleConnector
from dxm.lib.DxConnector.MSSQLConnector import MSSQLConnector
from dxm.lib.DxConnector.SybaseConnector import SybaseConnector
from dxm.lib.DxConnector.ExtendedConnector import ExtendedConnector
from dxm.lib.DxConnector.DxConnectorsList import DxConnectorsList
from dxm.lib.DxEnvironment.DxEnvironmentList import DxEnvironmentList
from dxm.lib.DxJDBC.DxJDBCList import DxJDBCList

# from masking_api_60.models.database_connector import DatabaseConnector

# from masking_api_60.models.connection_info import ConnectionInfo


database_types = ['oracle', 'sybase', 'mssql', 'aurora_postgres', 'db2',
                  'db2_iseries', 'db2_mainframe', 'generic', 'mysql',
                  'postgres', 'rds_oracle', 'rds_postgres', 'extended']

file_types = ['delimited', 'excel', 'fixed_width', 'xml']


def connector_add(p_engine, p_username,  params):
    """
    Add application to Masking engine
    param1: p_engine: engine name from configuration
    param2: params: dict of parameters needed for connector to add
    return 0 if added, non 0 for error
    """

    ret = 0
    logger = logging.getLogger()

    enginelist = get_list_of_engines(p_engine, p_username)

    if enginelist is None:
        return 1

    envname = params['envname']
    schemaName = params['schemaName']
    host = params['host']
    port = params['port']
    password = params['password']
    username = params['username']
    connname = params['connname']

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)

        if engine_obj.get_session():
            continue

        envlist = DxEnvironmentList()
        envlist.LoadEnvironments()
        logger.debug("Envname is %s" % envname)
        envref = envlist.get_environmentId_by_name(envname)

        if envref is None:
            ret = ret + 1
            continue

        connlist = DxConnectorsList()
        if params['type'] in database_types:
            if params['type'] == 'oracle':
                connobj = OracleConnector(engine_obj)
                dbtype = 'ORACLE'
            elif params['type'] == 'mssql':
                connobj = MSSQLConnector(engine_obj)
                dbtype = 'MSSQL'
            elif params['type'] == 'sybase':
                connobj = SybaseConnector(engine_obj)
                dbtype = 'SYBASE'
            elif params['type'] == 'extended':
                connobj = ExtendedConnector(engine_obj)
                dbtype = 'EXTENDED'
            else:
                connobj = DxConnector(engine_obj)
                dbtype = params['type'].upper()

            connobj.create_connector(
                connector_name = connname,
                database_type = dbtype,
                environment_id = envref
            )


            connobj.schema_name = schemaName
            connobj.username = username
            connobj.password = password
            connobj.host = host

            if port:
                connobj.port = int(port)
            connobj.sid = params['sid']
            connobj.jdbc = params['jdbc']
            connobj.instance_name = params['instancename']
            connobj.database_name = params['databasename']

            if params['jdbc_driver_name']:
                jdbclist = DxJDBCList()
                driver_id = jdbclist.get_driver_id_by_name(params['jdbc_driver_name'])
                connobj.jdbc_driver_id = driver_id

        elif params['type'] in file_types:
            path = params['path']
            connmode = params['servertype']
            connobj = DxFileConnector(engine_obj)
            connobj.is_database = False
            connobj.create_connector(
                connector_name = connname,
                file_type = params['type'].upper(),
                environment_id = envref,
                host=host,
                port=port,
                login_name=username,
                password=password,
                path=path,
                connection_mode=connmode.upper()
            )

        else:
            print_error('Wrong connector type %s' % params['type'])
            logger.error('Wrong connector type %s' % params['type'])
            return 1

        if connlist.add(connobj):
            ret = ret + 1

    return ret


def do_delete(**kwargs):
    connref = kwargs.get('connref')
    connlist = kwargs.get('connlist')
    return connlist.delete(connref)

def do_test(**kwargs):
    connref = kwargs.get('connref')
    connlist = kwargs.get('connlist')

    connobj = connlist.get_by_ref(connref)
    return connobj.test()

def do_print_meta(**kwargs):
    connref = kwargs.get('connref')
    connlist = kwargs.get('connlist')
    engine_obj = kwargs.get('engine_obj')
    format = kwargs.get('format')

    connobj = connlist.get_by_ref(connref)

    if connobj.is_database:
        metaname = 'Table name'
    else:
        metaname = 'File name'

    data = DataFormatter()

    data_header = [
                    ("Engine name", 30),
                    ("Connector name", 30),
                    (metaname, 40)
                  ]

    data.create_header(data_header)
    data.format_type = format
    metalist = connobj.fetch_meta()

    if metalist:
        for meta_item in metalist:
            data.data_insert(
                              engine_obj.get_name(),
                              connobj.connector_name,
                              meta_item
                            )
    else:
        print_error("List of tables/files is empty")
        return 1

    print("")
    print (data.data_output(False))
    print("")
    return 0

def connector_delete(p_engine, p_username,  connectorname, envname):
    """
    Delete connector from Masking engine
    param1: p_engine: engine name from configuration
    param2: connectorname: connectorname name
    param3: envname: environment name
    return 0 if added, non 0 for error
    """
    return connector_selector(p_engine, p_username,  connectorname, envname, 'do_delete')

def connector_selector(p_engine, p_username,  connectorname, envname, function_to_call,
                       format='fixed'):
    """
    Select unique connector from Masking engine and run function on it
    param1: p_engine: engine name from configuration
    param2: connectorname: connectorname name
    param3: envname: environment name
    param4: function_to_call: name of function to call on connector
    param5: format: format of output, set to fixed
    return 0 if added, non 0 for error
    """

    ret = 0
    enginelist = get_list_of_engines(p_engine, p_username)

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)

        if engine_obj.get_session():
            continue

        envlist = DxEnvironmentList()
        envlist.LoadEnvironments()
        connlist = DxConnectorsList()
        connlist.LoadConnectors(envname)

        connref = connlist.get_connectorId_by_name(connectorname)

        if connref:
            dynfunc = globals()[function_to_call]
            ret = ret + dynfunc(
                connref=connref,
                engine_obj=engine_obj,
                connlist=connlist,
                format=format)
        else:
            ret = ret + 1
            continue

    return ret

def connector_test(p_engine, p_username,  connectorname, envname):
    """
    Test connector from Masking engine
    param1: p_engine: engine name from configuration
    param2: connectorname: connectorname name
    return 0 if added, non 0 for error
    """
    logger = logging.getLogger()
    logger.debug("starting connector_test")
    return connector_selector(p_engine, p_username,  connectorname, envname, 'do_test')

def connector_fetch(p_engine, p_username,  connectorname, envname, format):
    """
    Test connector from Masking engine
    param1: p_engine: engine name from configuration
    param2: connectorname: connectorname name
    param3: envname: name of environment
    param4: format: output format
    return 0 if added, non 0 for error
    """

    return connector_selector(p_engine, p_username,  connectorname, envname,
                              'do_print_meta', format)

def connector_update(p_engine, p_username,  params):
    """
    Update connector from Masking engine
    param1: p_engine: engine name from configuration
    param2: connectorname: connectorname name
    param3: params: dict of parameters needed for connector to add
    return 0 if added, non 0 for error
    """

    ret = 0

    logger = logging.getLogger()

    enginelist = get_list_of_engines(p_engine, p_username)

    if enginelist is None:
        return 1

    connectorname = params['connname']
    envname = params['envname']

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)

        if engine_obj.get_session():
            continue

        DxConnectorsList(envname)
        connref = DxConnectorsList.get_connectorId_by_name(connectorname)

        if connref is None:
            ret = ret + 1
            continue

        connobj = DxConnectorsList.get_by_ref(connref)

        if params['schemaName']:
            connobj.schema_name = params['schemaName']



        if params['jdbc']:
            connobj.host = None
            connobj.port = None
            if hasattr(connobj, 'sid'):
                connobj.sid = None
            if hasattr(connobj, 'instance_name'):
                connobj.instance_name = None
            if hasattr(connobj, 'database_name'):
                connobj.database_name = None    
            connobj.jdbc = params['jdbc']
        else:
            connobj.jdbc = None
            if params['host']:
                connobj.host = params['host']

            if params['port']:
                connobj.port = params['port']
            if hasattr(connobj, 'sid'):
                if params['sid']:
                    connobj.sid = params['sid']

            if hasattr(connobj, 'instance_name'):
                if params['instancename']:
                    connobj.instance_name = params['instancename']

            if hasattr(connobj, 'database_name'):
                if params['databasename']:
                    connobj.database_name = params['databasename']

        if params['password']:
            connobj.password = params['password']

        if params['username']:
            connobj.username = params['username']

        # if params['connname']:
        #     connobj.connector_name = params['connname']



        if connobj.update():
            ret = ret + 1

    return ret

def connector_list(p_engine, p_username,  format, envname, connector_name, details):
    """
    Print list of connectors
    param1: p_engine: engine name from configuration
    param2: format: output format
    param3: envname: environemnt name filter for connectors
    param4: connector_name: connector name to list
    param5: details: print connector details
    return 0 if connector found
    """

    ret = 0

    enginelist = get_list_of_engines(p_engine, p_username)

    if enginelist is None:
        return 1

    data = DataFormatter()

    if details:
        data_header = [
                        ("Engine name", 30),
                        ("Environment name", 30),
                        ("Connector name", 30),
                        ("Connector type", 15),
                        ("Hostname", 30),
                        ("Port", 5),
                        ("Schema name", 30),
                        ("Type depended", 100)
                      ]
    else:
        data_header = [
                        ("Engine name", 30),
                        ("Environment name", 30),
                        ("Connector name", 30),
                        ("Connector type", 15)
                      ]

    data.create_header(data_header)
    data.format_type = format
    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)

        if engine_obj.get_session():
            continue

        # connlist = DxConnectorsList()
        # envlist = DxEnvironmentList()
        # envlist.LoadEnvironments()
        # connlist.LoadConnectors(envname)

        DxConnectorsList(envname)

        if connector_name is None:
            connectors = DxConnectorsList.get_allref()
        else:
            connectors = DxConnectorsList.get_all_connectorId_by_name(connector_name)
            if connectors is None:
                ret = ret + 1
                continue

        for connref in connectors:
            connobj = DxConnectorsList.get_by_ref(connref)
            if details:
                rest = ''.join(['%s = %s ' % (key, value)
                               for (key, value)
                               in connobj.get_type_properties().items()])
                data.data_insert(
                                  engine_tuple[0],
                                  DxEnvironmentList.get_by_ref(connobj.environment_id)
                                  .environment_name,
                                  connobj.connector_name,
                                  connobj.connector_type,
                                  connobj.host,
                                  connobj.port,
                                  connobj.schema_name,
                                  rest
                                )
            else:
                data.data_insert(
                                  engine_tuple[0],
                                  DxEnvironmentList.get_by_ref(connobj.environment_id)
                                  .environment_name,
                                  connobj.connector_name,
                                  connobj.connector_type
                                )

    print("")
    print (data.data_output(False))
    print("")
    return ret
