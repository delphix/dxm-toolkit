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

from dxm.lib.DxColumn.DxColumnList import DxColumnList
from dxm.lib.DxColumn.DxDBColumn import DxDBColumn
from dxm.lib.DxRuleset.DxRulesetList import DxRulesetList
from dxm.lib.DxConnector.DxConnectorsList import DxConnectorsList
from dxm.lib.DxEnvironment.DxEnvironmentList import DxEnvironmentList
from dxm.lib.DxTable.DxMetaList import DxMetaList


def columns_copy(engine_obj, meta_id, new_meta_id):
    """
    Copy columns from one meta object to other one
    :param1 engine_obj: Masking engine
    :param2 meta_id: source meta id
    :param3 new_meta_id: destination meta id
    return 0 if OK
    """

    ret = 0

    logger = logging.getLogger()

    collist = DxColumnList()
    if collist.LoadColumns(metadata_id=meta_id, is_masked=True) == 1:
        logger.debug("Problem with loading masked columns for meta %s"
                     % meta_id)
        return 1

    newcollist = DxColumnList()
    if newcollist.LoadColumns(metadata_id=new_meta_id) == 1:
        logger.debug("Problem with loading columns for new meta %s"
                     % new_meta_id)
        return 1

    for colref in collist.get_allref():
        colobj = collist.get_by_ref(colref)
        newcolref = newcollist.get_column_id_by_name(colobj.cf_meta_name)
        newcol = newcollist.get_by_ref(newcolref)
        if type(newcol) == DxDBColumn:
            newcol.from_column(colobj)
            newcol.table_metadata_id = new_meta_id
            newcol.column_metadata_id = newcolref
        else:
            newcol.from_file(colobj)
            newcol.file_field_metadata_id = newcolref
            newcol.file_format_id = new_meta_id
        if newcol.update():
            ret = ret + 1

    return ret

def column_setmasking(p_engine, rulesetname, envname, metaname, columnname,
                      algname, domainname):
    """
    Set masking for column
    :param1 p_engine: masking engine
    :param2 rulesetname: name of ruleset
    :param3 envname: name of environment
    :param4 metaname: name of table or file
    :param5 columnname: name of table column or file field
    :param6 algname: algorithm name
    :param7 domainname: domain name
    """

    return column_worker(p_engine, None, rulesetname, envname, metaname,
                         columnname, None, None, algname, True, domainname,
                         'update_algorithm')


def column_unsetmasking(p_engine, rulesetname, envname, metaname, columnname):
    """
    Set masking for column
    :param1 p_engine: masking engine
    :param2 rulesetname: name of ruleset
    :param3 envname: name of environment
    :param4 metaname: name of table or file
    :param5 columnname: name of table column or file field
    :param6 algname: algorithm name
    :param7 domainname: domain name
    """

    return column_worker(p_engine, None, rulesetname, envname, metaname,
                         columnname, None, None, None, False, None,
                         'update_algorithm')


def column_replace(p_engine, rulesetname, envname, metaname, columnname,
                   algname, newalgname, newdomain):

    return column_worker(p_engine, None, rulesetname, envname, metaname,
                         columnname, algname, None, newalgname, True,
                         newdomain, 'update_algorithm')


def column_check(p_engine, rulesetname, envname, metaname, columnname,
                 algname):

    return column_worker(p_engine, None, rulesetname, envname, metaname,
                         columnname, algname, None, None, None,
                         None, 'found')

def found(**kwargs):
    return 1


def column_list(p_engine, format, sortby, rulesetname, envname, metaname,
                columnname, algname, is_masked):
    """
    Print column list
    param1: p_engine: engine name from configuration
    param2: format: output format
    param3: sortby: sort by output if needed
    param4: rulesetname: ruleset name
    param5: envname: environment name
    param6: metaname: meta name (table or file)
    param7: columnname: column name (column or field)
    param8: algname: algorithm name to filter
    param9: is_masked: is masked fileter
    return 0 if no issues
    """

    data = DataFormatter()
    data_header = [
                    ("Engine name", 30),
                    ("Environment name", 30),
                    ("Ruleset name", 30),
                    ("Metadata name", 32),
                    ("Column name", 32),
                    ("Type", 8),
                    ("Data type", 30),
                    ("Domain name", 32),
                    ("Alg name", 32),
                  ]
    data.create_header(data_header)
    data.format_type = format
    ret = column_worker(
        p_engine, sortby, rulesetname, envname, metaname, columnname,
        algname, is_masked, None, None,
        None, 'do_print', data=data)

    print("")
    print (data.data_output(False, sortby))
    print("")

    return ret



def column_save(p_engine, sortby, rulesetname, envname, metaname, columnname,
                algname, is_masked, file):
    """
    Print column list
    param1: p_engine: engine name from configuration
    param2: sortby: sort by output if needed
    param3: rulesetname: ruleset name
    param4: envname: environment name
    param5: metaname: meta name (table or file)
    param6: columnname: column name (column or field)
    param7: algname: algorithm name to filter
    param8: is_masked: is masked fileter
    param9: file: file to write output
    return 0 if no issues
    """

    if p_engine == 'all':
        print_error("you can run column save command on all engines"
                    "at same time")
        return 1

    enginelist = get_list_of_engines(p_engine)

    if enginelist is None:
        return 1

    engine_tuple = enginelist[-1]

    engine_obj = DxMaskingEngine(engine_tuple)

    if engine_obj.get_session():
        return 1

    rulelist = DxRulesetList()
    rulelist.LoadRulesets(envname)
    ruleref = rulelist.get_rulesetId_by_name(rulesetname)

    ruleobj = rulelist.get_by_ref(ruleref)

    if ruleobj is None:
        return 1

    if ruleobj.type == "Database":
        data = DataFormatter()
        data_header = [
                        ("Table Name", 32),
                        ("Type", 5),
                        ("Parent Column Name", 5),
                        ("Column name", 32),
                        ("Data Type", 32),
                        ("Domain", 32),
                        ("Algorithm", 32),
                        ("Is masked", 32)
                      ]
        data.create_header(data_header)
        data.format_type = "csv"
        worker = "do_save_database"
    else:
        data = DataFormatter()
        data_header = [
                        ("File Name", 32),
                        ("Field Name", 5),
                        ("Domain", 32),
                        ("Algorithm", 32),
                        ("Is masked", 32)
                      ]
        data.create_header(data_header)
        data.format_type = "csv"
        worker = "do_save_file"


    ret = column_worker(
        p_engine, sortby, rulesetname, envname, metaname, columnname,
        algname, is_masked, None, None,
        None, worker, data=data)

    if ret == 0:

        output = data.data_output(False, sortby)
        try:
            file.write(output)
            file.close()
            print_message("Columns saved to file %s" % file.name)
            return 0
        except Exception as e:
            print_error("Problem with file %s Error: %s" %
                        (file.name, str(e)))
            return 1

    else:
        return 1


def column_export(p_engine, sortby, rulesetname, envname, metaname, columnname,
                  algname):
    """
    Print column list
    param1: p_engine: engine name from configuration
    param2: sortby: sort by output if needed
    param3: rulesetname: ruleset name
    param4: envname: environment name
    param5: metaname: meta name (table or file)
    param6: columnname: column name (column or field)
    param7: algname: algorithm name to filter
    param8: is_masked: is masked fileter
    param9: file: file to write output
    return 0 if no issues
    """

    data = DataFormatter()
    data_header = [
                    ("Metadata name", 32),
                    ("Column name", 32),
                    ("Alg name", 32),
                    ("Domain name", 32),
                    ("is_masked", 32)
                  ]
    data.create_header(data_header)
    data.format_type = "json"

    ret = column_worker(
        p_engine, sortby, rulesetname, envname, metaname, columnname,
        algname, None, None, None,
        None, 'do_export', data=data)

    if ret == 0:
        return data
    else:
        return None


def do_print(**kwargs):
    """
    Put column information to data object
    for metadata print
    """

    colobj = kwargs.get('colobj')
    ruleobj = kwargs.get('ruleobj')
    metaobj = kwargs.get('metaobj')
    envobj = kwargs.get('envobj')
    data = kwargs.get('data')
    engine = kwargs.get('engine')

    if colobj.is_masked:
        print_algname = colobj.algorithm_name
        print_domain = colobj.domain_name
    else:
        print_algname = ''
        print_domain = ''


    if envobj:
        environment_name = envobj.environment_name
    else:
        environment_name = 'N/A'

    data.data_insert(
                      engine[0],
                      environment_name,
                      ruleobj.ruleset_name,
                      metaobj.meta_name,
                      colobj.cf_meta_name,
                      colobj.cf_meta_column_role,
                      colobj.cf_meta_type,
                      print_domain,
                      print_algname
                    )

    return 0


def do_export(**kwargs):
    """
    Put column information to data object
    for metadata save
    """

    colobj = kwargs.get('colobj')
    metaobj = kwargs.get('metaobj')
    data = kwargs.get('data')

    if colobj.is_masked:
        print_algname = colobj.algorithm_name
        print_domain = colobj.domain_name
        print_ismasked = 'Y'
    else:
        print_algname = ''
        print_domain = ''
        print_ismasked = 'N'

    data.data_insert(
                      metaobj.meta_name,
                      colobj.cf_meta_name,
                      print_algname,
                      print_domain,
                      print_ismasked
                    )

    return 0

def do_save_database(**kwargs):
    """
    Put column information to data object
    for metadata save
    """

    colobj = kwargs.get('colobj')
    metaobj = kwargs.get('metaobj')
    data = kwargs.get('data')

    if colobj.is_masked:
        print_algname = colobj.algorithm_name
        print_domain = colobj.domain_name
        print_ismasked = 'Y'
    else:
        print_algname = ''
        print_domain = ''
        print_ismasked = 'N'

    data.data_insert(
                      metaobj.meta_name,
                      colobj.cf_meta_column_role,
                      "-",
                      colobj.cf_meta_name,
                      colobj.cf_meta_type,
                      print_domain,
                      print_algname,
                      print_ismasked
                    )

    return 0

def do_save_file(**kwargs):
    """
    Put column information to data object
    for metadata save
    """

    colobj = kwargs.get('colobj')
    metaobj = kwargs.get('metaobj')
    data = kwargs.get('data')

    if colobj.is_masked:
        print_algname = colobj.algorithm_name
        print_domain = colobj.domain_name
        print_ismasked = 'Y'
    else:
        print_algname = ''
        print_domain = ''
        print_ismasked = 'N'

    data.data_insert(
                      metaobj.meta_name,
                      colobj.cf_meta_name,
                      print_domain,
                      print_algname,
                      print_ismasked
                    )

    return 0

def column_worker(p_engine, sortby, rulesetname, envname, metaname, columnname,
                  filter_algname, filter_is_masked, algname, is_masked,
                  domainname, function_to_call, data=None):
    """
    Select a column using all filter parameters
    and run action defined in function_to_call

    param1: p_engine: engine name from configuration
    param2: sortby: sort by output if needed
    param3: rulesetname: ruleset name
    param4: envname: environment name
    param5: metaname: meta name (table or file)
    param6: columnname: column name (column or field)
    param7: filter_algname: algorithm name to filter
    param8: filter_is_masked: is masked fileter
    param9: algname: new algorithm to set
    param10: is_masked: set masking False/True
    param11: domainname: new domain to set
    param12: function_to_call: function name to call
    param13: data: output object
    return 0 action is processed without issues
    """

    ret = 0

    logger = logging.getLogger()

    enginelist = get_list_of_engines(p_engine)

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)

        if engine_obj.get_session():
            continue

        envlist = DxEnvironmentList()
        envlist.LoadEnvironments()
        rulelist = DxRulesetList()
        rulelist.LoadRulesets(envname)
        connlist = DxConnectorsList()
        connlist.LoadConnectors(envname)
        metalist = DxMetaList()

        rulesetref_list = []

        if rulesetname:
            ruleref = rulelist.get_rulesetId_by_name(rulesetname)
            if ruleref:
                rulesetref_list.append(ruleref)
        else:
            rulesetref_list = rulelist.get_allref()

        for ruleref in rulesetref_list:
            ruleobj = rulelist.get_by_ref(ruleref)
            connobj = connlist.get_by_ref(ruleobj.connectorId)

            if connobj:
                envobj = envlist.get_by_ref(connobj.environment_id)
            else:
                envobj = None

            metalist.LoadMeta(ruleobj.ruleset_id)

            metasetref_list = []

            if metaname:
                metaref = metalist.get_MetadataId_by_name(metaname, 1)
                if metaref:
                    metasetref_list.append(metaref)
            else:
                metasetref_list = metalist.get_allref()

            for metaid in metasetref_list:
                metaobj = metalist.get_by_ref(metaid)
                collist = DxColumnList()
                collist.LoadColumns(
                    metadata_id=metaid,
                    is_masked=filter_is_masked)

                colsetref_list = []

                if columnname:
                    colref = collist.get_column_id_by_name(columnname)
                    logger.debug("Column ref with name %s : %s" %
                                 (columnname, colref))
                    if colref:
                        colsetref_list.append(colref)
                else:
                    colsetref_list = collist.get_allref()

                logger.debug("List of columns to process : %s" %
                             colsetref_list)

                if filter_algname:
                    colsetref_masked = collist.get_column_id_by_algorithm(
                                            filter_algname
                                       )
                    logger.debug("List of columns with algorithm %s : %s"
                                 % (filter_algname, colsetref_masked))
                    colsetref_list = list(set(colsetref_list)
                                          & set(colsetref_masked))
                    logger.debug("Intersection with column name filter %s"
                                 % colsetref_masked)

                for colref in colsetref_list:
                    colobj = collist.get_by_ref(colref)

                    dynfunc = globals()[function_to_call]
                    ret = ret + dynfunc(data=data, engine=engine_tuple,
                                        envobj=envobj, ruleobj=ruleobj,
                                        metaobj=metaobj, colobj=colobj,
                                        algname=algname, is_masked=is_masked,
                                        domainname=domainname)
    return ret


def update_algorithm(**kwargs):
    """
    Update algorithm
    """

    colobj = kwargs.get('colobj')
    algname = kwargs.get('algname')
    domainname = kwargs.get('domainname')
    ruleobj = kwargs.get('ruleobj')
    metaobj = kwargs.get('metaobj')
    is_masked = kwargs.get('is_masked')

    colobj.is_masked = is_masked

    if algname == 'None':
        algname = None
        domainname = None
        colobj.is_masked = False

    colobj.algorithm_name = algname
    colobj.domain_name = domainname
    if colobj.update():
        print_error("Problem with updating column for "
                    "ruleset %s meta %s column %s"
                    % (ruleobj.ruleset_name, metaobj.meta_name,
                       colobj.cf_meta_name))
        return 1
    else:
        print_message("Algorithm %s domain %s updated for "
                      "ruleset %s meta %s column %s"
                      % (algname, domainname,
                         ruleobj.ruleset_name,
                         metaobj.meta_name,
                         colobj.cf_meta_name))
        return 0

def column_batch(p_engine, rulesetname, envname, inputfile):
    """
    Update all columns defined in file
    param1: p_engine: engine name from configuration
    param2: rulesetname: ruleset name
    param3: envname: environment name
    param4: inputfile: file handler with entries
    return 0 if all rows processed without issues
    """

    ret = 0

    logger = logging.getLogger()

    enginelist = get_list_of_engines(p_engine)

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)

        if engine_obj.get_session():
            continue

        envlist = DxEnvironmentList()
        envlist.LoadEnvironments()
        rulelist = DxRulesetList()
        rulelist.LoadRulesets(envname)
        metalist = DxMetaList()

        ruleref = rulelist.get_rulesetId_by_name(rulesetname)
        if ruleref:
            ruleobj = rulelist.get_by_ref(ruleref)
        else:
            return 1

        metalist.LoadMeta(ruleobj.ruleset_id)

        metacolumn_list = {}

        for line in inputfile:
            if line.startswith('#'):
                continue
            try:
                logger.debug("readling line %s" % line)
                if ruleobj.type == "Database":
                    (metaname, column_role, parent_column, column_name,
                     type, domain_name, algname,
                     is_masked_YN) = line.strip().split(',')
                else:
                    (metaname, column_name, domain_name, algname,
                     is_masked_YN) = line.strip().split(',')

            except ValueError:
                logger.error("not all columns in file have value")
                print_error("not all columns in file have value")
                logger.error("line %s" % line)
                print_error("line %s" % line)
                ret = ret + 1
                continue

            metaref = metalist.get_MetadataId_by_name(metaname)
            if metaref is None:
                ret = ret + 1
                continue

            metaobj = metalist.get_by_ref(metaref)

            if metaref not in metacolumn_list:
                logger.debug("reading columns from engine for %s " % metaname)
                collist = DxColumnList()
                collist.LoadColumns(metadata_id=metaref)
                metacolumn_list[metaref] = collist

            colref = metacolumn_list[metaref].get_column_id_by_name(
                column_name)

            if colref:
                colobj = metacolumn_list[metaref].get_by_ref(colref)
                if is_masked_YN == 'Y':
                    is_masked = True
                else:
                    is_masked = False

                if algname == '':
                    algname = 'None'

                if domain_name == '':
                    domain_name = 'None'

                update_algorithm(colobj=colobj,
                                 algname=algname,
                                 domainname=domain_name,
                                 metaobj=metaobj,
                                 ruleobj=ruleobj,
                                 is_masked=is_masked)
            else:
                ret = ret + 1
                continue

    return ret
