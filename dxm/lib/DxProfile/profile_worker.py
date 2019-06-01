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
# Date    : September 2018


from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from dxm.lib.DxTools.DxTools import get_list_of_engines
from dxm.lib.Output.DataFormatter import DataFormatter
from dxm.lib.DxProfile.DxProfilesList import DxProfilesList
from dxm.lib.DxProfile.DxProfileExpList import DxProfileExpList
from dxm.lib.DxProfile.DxProfileExt import DxProfileExt
from dxm.lib.DxProfile.DxProfile import DxProfile
import logging
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message

def expression_add(p_engine, expname, domainname, level, regex):
    """
    Add expression to engine
    param1: p_engine: engine name from configuration
    param2: expname: expression name
    param3: domainname: domain name
    param4: datalevel: data level
    param5: regex: regular expression
    return 0 if expression was added
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

        # load all objects
        profileexplist = DxProfileExpList()
        peobj = DxProfileExt()
        peobj.expression_name = expname
        peobj.domain_name = domainname
        if level:
            if level == 'data':
                peobj.data_level_profiling = True
            else:
                peobj.data_level_profiling = False
        peobj.regular_expression = regex

        if profileexplist.add(peobj):
            ret = ret + 1

    return ret

def profile_add(p_engine, profilename, expname, description):
    """
    Add profile to engine
    param1: p_engine: engine name from configuration
    param2: profilename: profile name
    param3: expname: expression list names
    param4: description: profile description
    return 0 if profile was added
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

        # load all objects
        profilelist = DxProfilesList()
        probj = DxProfile()
        probj.profile_set_name = profilename
        probj.created_by = engine_obj.get_username()
        probj.description = description
        if probj.set_expressions_using_names(expname):
            ret = ret + 1
        else:
            if profilelist.add(probj):
                ret = ret + 1

    return ret

def expression_list(p_engine, expname, p_format):
    """
    Print list of expressions
    param1: p_engine: engine name from configuration
    param2: expname: expression name to list
    param3: p_format: output format
    return 0 if profile name found
    """

    data = DataFormatter()
    data_header = [
                    ("Engine name", 30),
                    ("Expression name", 30),
                    ("Domain name", 30),
                    ("Created by", 30),
                    ("Column/Data level", 30),
                    ("Regular expression", 30)
                  ]

    data.create_header(data_header)
    data.format_type = p_format

    ret = expression_worker(p_engine=p_engine,
                            expname=expname,
                            function_to_call='do_expresionlist',
                            p_format=p_format,
                            data=data)

    print("")
    print (data.data_output(False))
    print("")
    return ret

def expression_update(p_engine, expname, domainname, level, regex):
    """
    Update expression definition on engine
    param1: p_engine: engine name from configuration
    param2: expname: expression name
    param3: domainname: domain name
    param4: level: data level
    param5: regex: regular expression
    return 0 if expression updated
    """

    return expression_worker(p_engine=p_engine,
                             expname=expname,
                             domainname=domainname,
                             level=level,
                             regex=regex,
                             function_to_call='do_expresionupdate')


def expression_delete(p_engine, expname):
    """
    Remove expression from engine
    param1: p_engine: engine name from configuration
    param2: expname: expression name to remove from engine
    return 0 if expression deleted
    """

    return expression_worker(p_engine=p_engine,
                             expname=expname,
                             function_to_call='do_expressiondelete')


def do_expressiondelete(**kwargs):
    """
    Worker to remove expression from engine
    proexpobj: expression object
    profileexplist: expression list object
    return 0 if expression deleted
    """

    proexpobj = kwargs.get('proexpobj')
    profileexplist = kwargs.get('profileexplist')

    if profileexplist.delete(proexpobj.profile_expression_id):
        return 1
    else:
        return 0

def do_expresionupdate(**kwargs):
    """
    Worker to update expression on engine
    proexpobj: expression object
    domainname: domain name
    level: expression level
    regex: expression regular expression
    return 0 if expression deleted
    """
    proexpobj = kwargs.get('proexpobj')
    domainname = kwargs.get('domainname')
    level = kwargs.get('level')
    regex = kwargs.get('regex')

    if domainname:
        proexpobj.domain_name = domainname

    if regex:
        proexpobj.regular_expression = regex

    if level:
        if level == 'data':
            proexpobj.data_level_profiling = True
        else:
            proexpobj.data_level_profiling = False

    if proexpobj.update():
        return 1
    else:
        return 0


def do_expresionlist(**kwargs):
    """
    Worker to add expression to dataouttput object
    proexpobj: expression object
    engine_obj: engine object
    data: dataouttput object
    """
    engine_obj = kwargs.get('engine_obj')
    proexpobj = kwargs.get('proexpobj')
    data = kwargs.get('data')

    if proexpobj.data_level_profiling:
        dcswitch = "Data"
    else:
        dcswitch = "Column"
    data.data_insert(
                      engine_obj.get_name(),
                      proexpobj.expression_name,
                      proexpobj.domain_name,
                      proexpobj.created_by,
                      dcswitch,
                      proexpobj.regular_expression
                    )
    return 0


def expression_worker(**kwargs):
    """
    Expression worker - run a dynamic action on expression object
    p_engine: engine name from configuration
    expname: expression name to list
    function_to_call: function name to call for every expression object
    kwargs: passed to dynamic action
    return sum of return codes of dynamic action run on all selected
    expressions
    """

    p_engine = kwargs.get('p_engine')
    expname = kwargs.get('expname')
    function_to_call = kwargs.get('function_to_call')

    enginelist = get_list_of_engines(p_engine)

    if enginelist is None:
        return 1

    ret = 0

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)
        if engine_obj.get_session():
            continue

        # load all objects
        profileexplist = DxProfileExpList()
        expressions = []

        if expname is None:
            expressions = profileexplist.get_allref()
        else:
            expression = profileexplist.get_profileExpId_by_name(expname)
            expressions.append(expression)
            if expression is None:
                ret = ret + 1
                continue

        for peref in expressions:
            proexpobj = profileexplist.get_by_ref(peref)
            dynfunc = globals()[function_to_call]
            ret = ret + dynfunc(
                            proexpobj=proexpobj,
                            profileexplist=profileexplist,
                            engine_obj=engine_obj,
                            **kwargs)

    return ret


def profile_addexpression(p_engine, profilename, expname):
    """
    Add expression to Profile set
    param1: p_engine: engine name from configuration
    param2: profilename: profile name to list
    param3: expname: expression name to add to profile
    return 0 if profile name found
    """
    return profile_worker(p_engine=p_engine, profilename=profilename,
                          expname=expname, function_to_call='do_addexpression')


def profile_deleteexpression(p_engine, profilename, expname):
    """
    Delete expression from Profile set
    param1: p_engine: engine name from configuration
    param2: profilename: profile name to list
    param3: expname: expression name to remove from
    return 0 if profile name found
    """
    return profile_worker(
            p_engine=p_engine,
            profilename=profilename,
            expname=expname,
            function_to_call='do_deleteexpression')


def profile_list(p_engine, profilename, expname, p_format, mapping):
    """
    Print list of Profile sets
    param1: p_engine: engine name from configuration
    param2: profilename: profile name to list
    param3: expname: expression name to list if details is true
    param4: p_format: output format
    param5: mapping: print expressions mapping for each profile
    return 0 if profile name found
    """
    data = DataFormatter()
    if not mapping:
        data_header = [
                        ("Engine name", 30),
                        ("Profile name", 30),
                        ("Number of expressions", 30),
                        ("Created by", 30),
                        ("Created time", 30),
                        ("Description", 30)
                      ]
    else:
        data_header = [
                        ("Engine name", 30),
                        ("Profile name", 30),
                        ("Expression name", 30),
                        ("Domain name", 30),
                        ("Created by", 30),
                        ("Column/Data level", 30),
                        ("Regular expression", 30)
                      ]

    data.create_header(data_header)
    data.format_type = p_format
    ret = profile_worker(p_engine=p_engine, profilename=profilename,
                         expname=expname, function_to_call='do_profilelist',
                         p_format=p_format, mapping=mapping, data=data)

    print("")
    print (data.data_output(False))
    print("")
    return ret


def profile_delete(p_engine, profilename):
    """
    Print list of Profile sets
    param1: p_engine: engine name from configuration
    param2: profilename: profile name to list
    return 0 if profile deleted
    """
    exit(profile_worker(p_engine=p_engine, profilename=profilename,
                        function_to_call='do_deleteprofile'))


def profile_export(p_engine, profilename, exportfile):
    """
    Export list of Profile sets into csv
    param1: p_engine: engine name from configuration
    param2: profilename: profile name to list
    param3: exportfile: file location
    return 0 if profile name found
    """
    data = DataFormatter()
    data_header = [
                    ("Profile name", 30),
                    ("Expression name", 30)
                  ]

    data.create_header(data_header)
    data.format_type = "csv"
    ret = profile_worker(
        p_engine=p_engine,
        profilename=profilename,
        exportfile=exportfile,
        function_to_call='do_profileexport',
        data=data,
        mapping=True)

    if ret == 0:
        output = data.data_output(False)
        try:
            exportfile.write(output)
            exportfile.close()
            print_message("Profile(s) saved to file %s" % exportfile.name)
            return 0
        except Exception as e:
            print_error("Problem with file %s Error: %s" %
                        (exportfile.name, str(e)))
            return 1

    else:
        return 1


def do_addexpression(**kwargs):
    """
    Worker to add expression to profile
    profobj: Profile object
    expname: list of expression names to add
    return 0 if sucessful
    """
    profobj = kwargs.get('profobj')
    expname = kwargs.get('expname')
    logger = logging.getLogger()
    existing = profobj.profile_expression_ids

    logger.debug("list of existing expressions " + str(existing))

    if profobj.set_expressions_using_names(expname):
        return 1

    logger.debug("list of new expressions "
                 + str(profobj.profile_expression_ids))

    profobj.profile_expression_ids.extend(existing)

    logger.debug("sum of expressions "
                 + str(profobj.profile_expression_ids))

    if set(existing) != set(profobj.profile_expression_ids):
        # we are adding a expressions which are not on the profile list yet
        # remove duplictates
        profobj.profile_expression_ids = list(
            set(profobj.profile_expression_ids))

        logger.debug("sum of expressions after deduplicate "
                     + str(profobj.profile_expression_ids))

        if profobj.update():
            return 1
        else:
            return 0
    else:
        # there is no change needed
        print_error("Expression already is part of profile")
        logger.error("Expression already is part of profile")
        return 0


def do_deleteexpression(**kwargs):
    """
    Worker to delete expression from profile
    profobj: Profile object
    expname: list of expression names to delete
    return 0 if sucessful
    """
    profobj = kwargs.get('profobj')
    expname = kwargs.get('expname')
    logger = logging.getLogger()
    existing = profobj.profile_expression_ids

    logger.debug("list of existing expressions " + str(existing))

    expressions = DxProfileExpList()

    for exp in expname:
        expref = expressions.get_profileExpId_by_name(exp)
        if expref:
            if expref in profobj.profile_expression_ids:
                profobj.profile_expression_ids.remove(expref)
            else:
                logger.error("Expression name %s not found in profile" % exp)
                print_error("Expression name %s not found in profile" % exp)
                return 1
        else:
            logger.error("Expression name %s not found" % exp)
            return 1

    if len(profobj.profile_expression_ids) < 1:
        logger.error("At least one expression need to be assigne to profile")
        print_error("At least one expression need to be assigne to profile")
        return 1

    if profobj.update():
        return 1
    else:
        return 0


def do_deleteprofile(**kwargs):
    """
    Worker to delete profile
    profobj_list: profile list object
    profobj: profile object
    return 0 if profile deleted
    """
    profobj = kwargs.get('profobj')
    profilesetlist = kwargs.get('profilesetlist')

    if profilesetlist.delete(profobj.profile_set_id):
        return 1
    else:
        return 0


def do_profileexport(**kwargs):
    """
    Worker to export profile to dataobject using the follwing format
    profile_name, profile_expression_name
    profobj: profile object
    proexpobj: expression object
    data: dataoutput object
    """
    profobj = kwargs.get('profobj')
    proexpobj = kwargs.get('proexpobj')
    data = kwargs.get('data')
    data.data_insert(
                      profobj.profile_set_name,
                      proexpobj.expression_name
                    )


def do_profilelist(**kwargs):
    """
    Worker to add profile to dataobject
    profobj: profile object
    proexpobj: expression object
    data: dataoutput object
    mapping: if true add expression list to output
    engine_obj: engine object
    """
    mapping = kwargs.get('mapping')
    data = kwargs.get('data')
    profobj = kwargs.get('profobj')
    proexpobj = kwargs.get('proexpobj')
    engine_obj = kwargs.get('engine_obj')

    if not mapping:
        data.data_insert(
                          engine_obj.get_name(),
                          profobj.profile_set_name,
                          len(profobj.profile_expression_ids),
                          profobj.created_by,
                          str(profobj.created_time),
                          profobj.description
                        )
    else:
        if proexpobj.data_level_profiling:
            dcswitch = "Data"
        else:
            dcswitch = "Column"
        data.data_insert(
                          engine_obj.get_name(),
                          profobj.profile_set_name,
                          proexpobj.expression_name,
                          proexpobj.domain_name,
                          proexpobj.created_by,
                          dcswitch,
                          proexpobj.regular_expression
                        )

def profile_worker(**kwargs):
    """
    Profile worker - run a dynamic action on profile object
    p_engine: engine name from configuration
    profilename: profile name to list
    expname: expression name to list
    mapping: print expression name with profile
    function_to_call: function name to call for every profile object
    kwargs: passed to dynamic action
    return sum of return codes of dynamic action run on all selected
    expressions
    """
    p_engine = kwargs.get('p_engine')
    profilename = kwargs.get('profilename')
    expname = kwargs.get('expname')
    function_to_call = kwargs.get('function_to_call')
    mapping = kwargs.get('mapping')

    ret = 0
    enginelist = get_list_of_engines(p_engine)

    if enginelist is None:
        return 1

    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)
        if engine_obj.get_session():
            continue

        # load all objects
        profilesetlist = DxProfilesList()
        profileexplist = DxProfileExpList()
        profiles = []

        if profilename is None:
            profiles = profilesetlist.get_allref()
        else:
            profile = profilesetlist.get_profileSetId_by_name(profilename)
            profiles.append(profile)
            if profile is None:
                ret = ret + 1
                continue

        for profileref in profiles:
            profobj = profilesetlist.get_by_ref(profileref)

            if not mapping:
                dynfunc = globals()[function_to_call]
                dynfunc(profobj=profobj,
                        engine_obj=engine_obj,
                        profilesetlist=profilesetlist,
                        **kwargs)

            else:
                expression_list = []
                if expname:
                    exp = profileexplist.get_profileExpId_by_name(expname)
                    if exp is None:
                        ret = ret + 1
                        continue
                    else:
                        if exp in profobj.profile_expression_ids:
                            expression_list.append(exp)
                else:
                    expression_list = profobj.profile_expression_ids

                for pe in expression_list:
                    proexpobj = profileexplist.get_by_ref(pe)
                    dynfunc = globals()[function_to_call]
                    dynfunc(
                        profobj=profobj,
                        proexpobj=proexpobj,
                        engine_obj=engine_obj,
                        **kwargs)

        return ret
