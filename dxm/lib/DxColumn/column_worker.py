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
from dxm.lib.DxTools.DxTools import algname_mapping_export
from dxm.lib.DxTools.DxTools import algname_mapping_import

from dxm.lib.DxColumn.DxColumnList import DxColumnList
from dxm.lib.DxColumn.DxDBColumn import DxDBColumn
from dxm.lib.DxRuleset.DxRulesetList import DxRulesetList
from dxm.lib.DxConnector.DxConnectorsList import DxConnectorsList
from dxm.lib.DxEnvironment.DxEnvironmentList import DxEnvironmentList
from dxm.lib.DxTable.DxMetaList import DxMetaList

from dxm.lib.DxAlgorithm.DxAlgorithmList import DxAlgorithmList
from collections import namedtuple

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

def column_setmasking(p_engine, p_username,  rulesetname, envname, metaname, columnname,
                      algname, domainname, dateformat, idmethod):
    """
    Set masking for column
    :param1 p_engine: masking engine
    :param2 rulesetname: name of ruleset
    :param3 envname: name of environment
    :param4 metaname: name of table or file
    :param5 columnname: name of table column or file field
    :param6 algname: algorithm name
    :param7 domainname: domain name
    :param8 dateformat: date format for date algorithms
    :param8 idmethod: can column be overwritten by profiler
    """

    return column_worker(p_engine, p_username,  None, rulesetname, envname, metaname,
                         columnname, None, None, algname, True, domainname,
                         'update_algorithm', dateformat=dateformat,
                         idmethod=idmethod)


def column_unsetmasking(p_engine, p_username,  rulesetname, envname, metaname, columnname):
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

    return column_worker(p_engine, p_username,  None, rulesetname, envname, metaname,
                         columnname, None, None, None, False, None,
                         'update_algorithm')


def column_replace(p_engine, p_username,  rulesetname, envname, metaname, columnname,
                   algname, newalgname, newdomain):
    """
    Change masking algorithm from algname to newalgname for columns limited by
    filters
    :param1 p_engine: masking engine
    :param2 rulesetname: name of ruleset
    :param3 envname: name of environment
    :param4 metaname: name of table or file
    :param5 columnname: name of table column or file field
    :param6 algname: algorithm name
    :param7 newalgname: new algorithm name
    :param8 newdomain: domain for new algorithm

    Return 0 if all updates happend without issue, non-zero return for errors
    """
    return column_worker(p_engine, p_username,  None, rulesetname, envname, metaname,
                         columnname, algname, None, newalgname, True,
                         newdomain, 'update_algorithm')


def column_check(p_engine, p_username,  rulesetname, envname, column, columncount):
    """
    Check if column exists for condition set by parameters
    :param1 p_engine: masking engine
    :param2 rulesetname: name of ruleset
    :param3 envname: name of environment
    :param4 metaname: name of table or file
    :param5 columnname: name of table column or file field
    :param6 algname: algorithm name
    :param7 is_masked: is masked

    Return 1 if column exists, 0 if there is no column found
    """
    metaname = column["Metadata name"]
    columnname = column["Column name"]
    colcount = []
    ret = column_worker(p_engine, p_username,  None, rulesetname, envname, metaname,
                         columnname, None, None, None, None,
                         None, 'do_compare', cmpcolumn=column,
                         colcount=colcount)


    if columncount != len(colcount):
        print_error("Number of columns in table {} is different than in file"
                    .format(metaname))
        return 2

    if ret == 0:
        print_error("Column {} not found in ruleset".format(columnname))
        return 1

    if ret == -1:
        return 0

    if ret < -1:
        return 1


def do_compare(**kwargs):
    cmpcolumn = kwargs.get('cmpcolumn')
    enginecolumn = kwargs.get('colobj')

    if cmpcolumn["is_masked"] == 'Y':
        cmp_is_masked = True
    else:
        cmp_is_masked = False

    if cmpcolumn["idmethod"] == 'Y':
        cmp_is_profiler_writable = True
    else:
        cmp_is_profiler_writable = False

    if cmpcolumn["Alg name"] != '':
        cmp_algorithm_name = cmpcolumn["Alg name"]
    else:
        cmp_algorithm_name = None

    if cmpcolumn["Domain name"] != '':
        cmp_domain_name = cmpcolumn["Domain name"]
    else:
        cmp_domain_name = None

    if cmpcolumn["dateformat"] != '':
        cmp_dateformat = cmpcolumn["dateformat"]
    else:
        cmp_dateformat = None

    ret = -1

    if cmp_is_masked != enginecolumn.is_masked:
        print_error("Masking flag for table {} column {} is different"
                    .format(cmpcolumn["Metadata name"],
                            cmpcolumn["Column name"]))
        ret = ret - 1

    if cmp_is_profiler_writable != enginecolumn.is_profiler_writable:
        print_error("ID method for table {} column {} is different"
                    .format(cmpcolumn["Metadata name"],
                            cmpcolumn["Column name"]))
        ret = ret - 1

    if cmp_algorithm_name != enginecolumn.algorithm_name:
        print_error("Algorithm name for table {} column {} is different"
                    .format(cmpcolumn["Metadata name"],
                            cmpcolumn["Column name"]))
        ret = ret - 1
    if cmp_domain_name != enginecolumn.domain_name:
        print_error("Domain name for table {} column {} is different"
                    .format(cmpcolumn["Metadata name"],
                            cmpcolumn["Column name"]))
        ret = ret - 1

    if cmp_dateformat != enginecolumn.date_format:
        print_error("Date format for table {} column {} is different"
                    .format(cmpcolumn["Metadata name"],
                            cmpcolumn["Column name"]))
        ret = ret - 1

    return ret


def column_list(p_engine, p_username,  format, sortby, rulesetname, envname, metaname,
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
                    ("Date format", 15),
                    ("Domain name", 32),
                    ("Alg name", 32),
                  ]
    data.create_header(data_header)
    data.format_type = format
    ret = column_worker(
        p_engine, p_username, sortby, rulesetname, envname, metaname, columnname,
        algname, is_masked, None, None,
        None, 'do_print', data=data)

    print("")
    print (data.data_output(False, sortby))
    print("")

    return ret



def column_save(p_engine, p_username,  sortby, rulesetname, envname, metaname, columnname,
                algname, is_masked, file, inventory):
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
        print_error("you can't run column save command on all engines"
                    "at same time")
        return 1

    enginelist = get_list_of_engines(p_engine, p_username)

    if enginelist is None:
        return 1

    engine_tuple = enginelist[-1]

    engine_obj = DxMaskingEngine(engine_tuple)

    if engine_obj.get_session():
        return 1

    rulelist = DxRulesetList(envname)
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
                        ("Column Name", 32),
                        ("Data Type", 32),
                        ("Domain", 32),
                        ("Algorithm", 32),
                        ("Is Masked", 32),
                        ("ID Method", 32),
                        ("Row Type", 32),
                        ("Date Format", 32)
                      ]
        worker = "do_save_database"

        if inventory is True:
            data_header = data_header + [("Notes",30)]

        if engine_obj.version_ge("6.0.8"):
            data_header = data_header + [("Multi-Column Logical Field", 10),
                                         ("Group Number", 10)]      

    else:
        data = DataFormatter()
        data_header = [
                        ("File Name", 32),
                        ("Field Name", 5),
                        ("Domain", 32),
                        ("Algorithm", 32),
                        ("Is Masked", 32),
                        ("Priority", 8),
                        ("Record Type", 15),
                        ("Position", 8),
                        ("Length", 8),
                        ("Date Format", 32)
                      ]
        worker = "do_save_file"

        if inventory is True:
            data_header = data_header + [("Notes",30)]

        if engine_obj.version_ge("6.0.8"):
            data_header = data_header + [("Multi-Column Logical Field", 10),
                                         ("Group Number", 10)]  

    if inventory is True:
        data_header = [("Environment Name", 32),
                       ("Rule Set", 32)] + data_header



    data.create_header(data_header, inventory)
    data.format_type = "csv"

    ret = column_worker(
        p_engine, p_username, sortby, rulesetname, envname, metaname, columnname,
        algname, is_masked, None, None,
        None, worker, data=data, inventory=inventory)

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
        return ret


def column_export(p_engine, p_username,  sortby, rulesetname, envname, metaname, columnname,
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
                    ("is_masked", 32),
                    ("idmethod", 32),
                    ("dateformat", 32)
                  ]
    data.create_header(data_header)
    data.format_type = "json"

    ret = column_worker(
        p_engine, p_username, sortby, rulesetname, envname, metaname, columnname,
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


    if hasattr(colobj, "date_format") and colobj.date_format:
        date_format = colobj.date_format
    else:
        date_format = "-"

    data.data_insert(
                      engine[0],
                      environment_name,
                      ruleobj.ruleset_name,
                      metaobj.meta_name,
                      colobj.cf_meta_name,
                      colobj.cf_meta_column_role,
                      colobj.cf_meta_type,
                      date_format,
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

    if colobj.is_profiler_writable:
        print_idmethod = 'Y'
    else:
        print_idmethod = 'N'

    if colobj.date_format is None:
        print_dateformat = ''
    else:
        print_dateformat = colobj.date_format

    data.data_insert(
                      metaobj.meta_name,
                      colobj.cf_meta_name,
                      print_algname,
                      print_domain,
                      print_ismasked,
                      print_idmethod,
                      print_dateformat
                    )

    return 0

def do_save_database(**kwargs):
    """
    Put column information to data object
    for metadata save
    param: DxColumn colobj: column object to save
    param: DxTable metaobj: table object to save
    param: Output data: output data object
    """

    colobj = kwargs.get('colobj')
    metaobj = kwargs.get('metaobj')
    data = kwargs.get('data')
    inventory = kwargs.get('inventory')
    envobj = kwargs.get('envobj')
    ruleobj = kwargs.get('ruleobj')
    engine_obj = kwargs.get('engine_obj')
    alg_list = kwargs.get('alg_list')

    if inventory is True:
        mapping = algname_mapping_export()
    else:
        mapping = None

    if colobj.is_masked:
        print_algname = colobj.algorithm_name
        print_domain = colobj.domain_name
        print_ismasked = 'Y'
        if mapping is not None:
            # if algorithm is in mapping - change name if not - well leave a name 
            if colobj.algorithm_name in mapping:
                print_algname = mapping[colobj.algorithm_name]
            else:
                print_algname = colobj.algorithm_name
    else:
        print_algname = ''
        print_domain = ''
        print_ismasked = 'N'

    if colobj.is_profiler_writable:
        print_idmethod = 'Auto'
    else:
        print_idmethod = 'User'

    if colobj.date_format is None:
        print_dateformat = '-'
    else:
        print_dateformat = colobj.date_format

    if colobj.algorithm_group_no is not None:
        algobj = alg_list.get_by_ref(colobj.algorithm_name)
        group = colobj.algorithm_group_no
        field = [ x.name for x in algobj.fields if x.field_id == colobj.algorithm_field_id ][0]

    else:
        field = ''
        group = ''


    if inventory is True:

        if field == '':
            field = '-'
            group = '-'

        if engine_obj.version_ge("6.0.8"):

            data.data_insert(
                            envobj.environment_name,
                            ruleobj.ruleset_name,
                            metaobj.meta_name,
                            colobj.cf_meta_column_role,
                            "-",
                            colobj.cf_meta_name,
                            colobj.cf_meta_type,
                            print_domain,
                            print_algname,
                            print_ismasked,
                            print_idmethod,
                            "All Row",
                            print_dateformat,
                            colobj.notes,
                            field,
                            group
                            )
        else:
            data.data_insert(
                            envobj.environment_name,
                            ruleobj.ruleset_name,
                            metaobj.meta_name,
                            colobj.cf_meta_column_role,
                            "-",
                            colobj.cf_meta_name,
                            colobj.cf_meta_type,
                            print_domain,
                            print_algname,
                            print_ismasked,
                            print_idmethod,
                            "All Row",
                            print_dateformat
                            )
    else:
        if engine_obj.version_ge("6.0.8"):
            data.data_insert(
                            metaobj.meta_name,
                            colobj.cf_meta_column_role,
                            "-",
                            colobj.cf_meta_name,
                            colobj.cf_meta_type,
                            print_domain,
                            print_algname,
                            print_ismasked,
                            print_idmethod,
                            "All Row",
                            print_dateformat,
                            field,
                            group
                            )
        else:
            data.data_insert(
                            metaobj.meta_name,
                            colobj.cf_meta_column_role,
                            "-",
                            colobj.cf_meta_name,
                            colobj.cf_meta_type,
                            print_domain,
                            print_algname,
                            print_ismasked,
                            print_idmethod,
                            "All Row",
                            print_dateformat
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
    inventory = kwargs.get('inventory')
    envobj = kwargs.get('envobj')
    ruleobj = kwargs.get('ruleobj')

    if inventory is True:
        mapping = algname_mapping_export()
    else:
        mapping = None

    if colobj.is_masked:
        print_algname = colobj.algorithm_name
        print_domain = colobj.domain_name
        print_ismasked = 'Y'
        if mapping is not None:
            print_algname = mapping[colobj.algorithm_name]
    else:
        print_algname = ''
        print_domain = ''
        print_ismasked = 'N'

    if colobj.date_format is None:
        print_dateformat = '-'
    else:
        print_dateformat = colobj.date_format


    if inventory is True:
        data.data_insert(
                          envobj.environment_name,
                          ruleobj.ruleset_name,
                          metaobj.meta_name,
                          colobj.cf_meta_name,
                          print_domain,
                          print_algname,
                          print_ismasked,
                          "-",
                          "All Records",
                          colobj.field_position_number,
                          colobj.field_length,
                          print_dateformat
                        )
    else:
        data.data_insert(
                          metaobj.meta_name,
                          colobj.cf_meta_name,
                          print_domain,
                          print_algname,
                          print_ismasked,
                          "-",
                          "All Records",
                          colobj.field_position_number,
                          colobj.field_length,
                          print_dateformat
                        )

    return 0

def column_worker(p_engine, p_username,  sortby, rulesetname, envname, metaname, columnname,
                  filter_algname, filter_is_masked, algname, is_masked,
                  domainname, function_to_call, data=None, inventory=None,
                  **kwargs):
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

    enginelist = get_list_of_engines(p_engine, p_username)

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)

        if engine_obj.get_session():
            continue

        envlist = DxEnvironmentList()
        envlist.LoadEnvironments()
        rulelist = DxRulesetList(envname)
        connlist = DxConnectorsList(envname)
        metalist = DxMetaList()

        alg_list = DxAlgorithmList(sync=False)

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

                colcount = kwargs.get("colcount")
                if colcount is not None:
                    colcount.extend(collist.get_allref())

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
                                        domainname=domainname,
                                        inventory=inventory,
                                        engine_obj=engine_obj,
                                        alg_list=alg_list,
                                        **kwargs)
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
    dateformat = kwargs.get('dateformat')
    idmethod = kwargs.get('idmethod')

    colobj.is_masked = is_masked

    if dateformat is not None:
        colobj.date_format = dateformat

    if idmethod is not None:
        if idmethod == 'Y':
            colobj.is_profiler_writable = True
        else:
            colobj.is_profiler_writable = False

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

def column_batch(p_engine, p_username,  rulesetname, envname, inputfile, inventory):
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

    enginelist = get_list_of_engines(p_engine, p_username)

    if enginelist is None:
        return 1

    if inventory is True:
        mapping = algname_mapping_import()
    else:
        mapping = None


    database_list = "metaname column_role parent_column column_name \
                     type domain_name algname is_masked_YN idmethod rowtype dateformat"

    file_list = "metaname column_name domain_name algname \
                 is_masked_YN priority recordtype position \
                 length dateformat"

    inventory_addition = "env ruleset"

    multicolumn_addition = "fieldid groupid"

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)

        if engine_obj.get_session():
            continue

        envlist = DxEnvironmentList()
        envlist.LoadEnvironments()
        rulelist = DxRulesetList(envname)
        metalist = DxMetaList()

        alg_list = DxAlgorithmList(sync=False)

        ruleref = rulelist.get_rulesetId_by_name(rulesetname)
        if ruleref:
            ruleobj = rulelist.get_by_ref(ruleref)
        else:
            return 1

        metalist.LoadMeta(ruleobj.ruleset_id)

        metacolumn_list = {}


        setversion = False


        for line in inputfile:
            if not setversion:
                setversion = True
                
                if ruleobj.type == "Database":  
                    collist = database_list
                else:
                    collist = file_list

                if inventory is True:
                    collist = inventory_addition + " " + collist

                if "Multi-Column" in line:
                    # we have a 6.0.8 or higher inventory 
                    if inventory is True:
                        collist = collist + " notes " + multicolumn_addition
                    else:
                        collist = collist + " " + multicolumn_addition

                linetype = namedtuple("linetype", collist)

            if line.startswith('#'):
                continue
            try:
                logger.debug("readling line %s" % line)
                lineobj = linetype(*line.strip().split(','))

            except ValueError as e:
                if str(e) == "too many values to unpack":
                    logger.error("to few values in inputfile - maybe add "
                                 "--inventory if you are loading an inventory"
                                 "file from GUI")
                    print_error("to few values in inputfile - maybe add "
                                "--inventory if you are loading an inventory"
                                "file from GUI")
                    logger.error("line %s" % line)
                    print_error("line %s" % line)
                    ret = ret + 1
                    break
                else:
                    logger.error("not all columns in file have value")
                    print_error("not all columns in file have value")
                    logger.error("line %s" % line)
                    print_error("line %s" % line)
                    ret = ret + 1
                    break

            metaref = metalist.get_MetadataId_by_name(lineobj.metaname)
            if metaref is None:
                ret = ret + 1
                continue

            metaobj = metalist.get_by_ref(metaref)

            if metaref not in metacolumn_list:
                logger.debug("reading columns from engine for %s " % lineobj.metaname)
                collist = DxColumnList()
                collist.LoadColumns(metadata_id=metaref)
                metacolumn_list[metaref] = collist

            colref = metacolumn_list[metaref].get_column_id_by_name(
                lineobj.column_name)

            if colref:
                colobj = metacolumn_list[metaref].get_by_ref(colref)
                if lineobj.is_masked_YN == 'Y' or lineobj.is_masked_YN == 'true':
                    is_masked = True
                else:
                    is_masked = False

                if lineobj.algname == '' or lineobj.algname == '-':
                    algname = 'None'
                else:
                    algname = lineobj.algname

                if lineobj.domain_name == '' or lineobj.domain_name == '-':
                    domain_name = 'None'
                else:
                    domain_name = lineobj.domain_name 


                if hasattr(lineobj, 'fieldid'):
                    if lineobj.fieldid == '' or lineobj.fieldid == '-':
                        fieldid = None
                    else:
                        fieldid = lineobj.fieldid 
                else:
                    fieldid = None

                if ruleobj.type == "Database":
                    if lineobj.idmethod == 'Auto':
                        colobj.is_profiler_writable = True
                    elif lineobj.idmethod == 'User':
                        colobj.is_profiler_writable = False
                    else:
                        print_error("Wrong id method")
                        return 1

                if lineobj.dateformat == '-':
                    colobj.date_format = None
                else:
                    colobj.date_format = lineobj.dateformat

                if fieldid is not None:
                    algobj = alg_list.get_by_ref(lineobj.algname)
                    field_id = [ x.field_id for x in algobj.fields if x.name == fieldid ][0]
                    group_id = lineobj.groupid
                else:
                    field_id = None
                    group_id = None


                if mapping is not None and algname != 'None' and algname in mapping:
                    logger.debug("changing a name of algorithm for inventory import: from {} to {}".format(algname, mapping[algname]))
                    algname = mapping[algname]

                ret = ret + update_algorithm(colobj=colobj,
                                             algname=algname,
                                             domainname=domain_name,
                                             metaobj=metaobj,
                                             ruleobj=ruleobj,
                                             is_masked=is_masked,
                                             algorithm_field_id=field_id,
                                             algorithm_group_no=group_id)
            else:
                ret = ret + 1
                continue

    return ret
