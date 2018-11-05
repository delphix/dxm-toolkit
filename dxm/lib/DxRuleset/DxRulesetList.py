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


import logging
from dxm.lib.DxRuleset.DxDatabaseRuleset import DxDatabaseRuleset
from dxm.lib.DxRuleset.DxFileRuleset import DxFileRuleset
from dxm.lib.DxTools.DxTools import get_objref_by_val_and_attribute
from dxm.lib.DxTools.DxTools import paginator
from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from dxm.lib.DxEnvironment.DxEnvironmentList import DxEnvironmentList
from masking_apis.apis.database_ruleset_api import DatabaseRulesetApi
from masking_apis.apis.file_ruleset_api import FileRulesetApi
from masking_apis.rest import ApiException
from dxm.lib.DxLogging import print_error
from dxm.lib.DxConnector.DxConnectorsList import DxConnectorsList


class DxRulesetList(object):

    __rulesetList = {}
    __engine = None
    __logger = None

    @classmethod
    def __init__(self, environment_name=None):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        self.__engine = DxMaskingEngine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxRulesetList object")
        self.LoadRulesets(environment_name)

    @classmethod
    def LoadRulesets(self, environment_name):
        """
        Load list of rule sets
        Return None if OK
        """
        return self.LoadRulesets_worker(environment_name, None)

    @classmethod
    def LoadRulesetsbyId(self, env_id):
        """
        Load list of rule sets for env_id
        Return None if OK
        """
        return self.LoadRulesets_worker(None, env_id)

    @classmethod
    def LoadRulesets_worker(self, environment_name, env_id):
        """
        Load list of rule sets
        Return None if OK
        """

        DxConnectorsList(environment_name)
        self.__rulesetList = {}

        try:
            api_instance = DatabaseRulesetApi(self.__engine.api_client)

            if environment_name:
                environment_id = DxEnvironmentList.get_environmentId_by_name(
                                 environment_name)

                if environment_id:
                    database_rulesets = paginator(
                            api_instance,
                            "get_all_database_rulesets",
                            environment_id=environment_id,
                            _request_timeout=self.__engine.get_timeout())
                else:
                    return 1

            else:
                if env_id:
                    environment_id = env_id
                    database_rulesets = paginator(
                            api_instance,
                            "get_all_database_rulesets",
                            environment_id=environment_id,
                            _request_timeout=self.__engine.get_timeout())
                else:
                    environment_id = None
                    database_rulesets = paginator(
                                            api_instance,
                                            "get_all_database_rulesets")

            if database_rulesets.response_list:
                for c in database_rulesets.response_list:
                    ruleset = DxDatabaseRuleset(self.__engine)
                    ruleset.from_ruleset(c)
                    self.__rulesetList[c.database_ruleset_id] = ruleset
            else:
                if environment_id:
                    self.__logger.error("No database ruleset found for "
                                        "environment name %s"
                                        % environment_name)
                else:
                    self.__logger.error("No database ruleset found")

            api_instance = FileRulesetApi(self.__engine.api_client)

            if environment_id:
                file_rulesets = paginator(
                        api_instance,
                        "get_all_file_rulesets",
                        environment_id=environment_id)
            else:
                file_rulesets = paginator(
                        api_instance,
                        "get_all_file_rulesets")

            if file_rulesets.response_list:
                for c in file_rulesets.response_list:
                    ruleset = DxFileRuleset(self.__engine)
                    ruleset.from_ruleset(c)
                    self.__rulesetList[c.file_ruleset_id] = ruleset
            else:
                if environment_id:
                    self.__logger.error("No file ruleset found for "
                                        "environment name %s"
                                        % environment_name)
                else:
                    self.__logger.error("No file ruleset found")

        except ApiException as e:
            print_error("Can't load ruleset %s" % e.body)
            return 1

    @classmethod
    def get_by_ref(self, reference):
        """
        return a Ruleset object by refrerence
        return None if not found
        """
        try:
            self.__logger.debug("reference %s" % reference)
            return self.__rulesetList[reference]

        except KeyError as e:
            self.__logger.debug("can't find Ruleset object"
                                " for reference %s" % reference)
            self.__logger.debug(e)
            return None

    @classmethod
    def get_allref(self):
        """
        return a list of all references
        """
        return self.__rulesetList.keys()

    @classmethod
    def get_rulesetId_by_name(self, name):
        """
        Return ruleset id by name.
        :param1 name: name of ruleset
        return ref if OK
        return None if ruleset not found or not unique
        """
        reflist = self.get_rulesetId_by_name_worker(name)
        # convert list to single value
        # as there will be only one element in list
        if reflist:
            return reflist[0]
        else:
            return None

    @classmethod
    def get_all_rulesetId_by_name(self, name):
        """
        Return ruleset id by name.
        :param1 name: name of ruleset
        return list of references if OK
        return None if ruleset not found
        """
        return self.get_rulesetId_by_name_worker(name, None)

    @classmethod
    def get_rulesetId_by_name_worker(self, name, check_uniqueness=1):
        """
        :param1 name: name of ruleset
        :param2 check_uniqueness: check uniqueness put None if skip this check
        return list of rulesets
        """
        reflist = get_objref_by_val_and_attribute(name, self, 'ruleset_name')
        if len(reflist) == 0:
            self.__logger.error('Ruleset %s not found' % name)
            print_error('Ruleset %s not found' % name)
            return None

        if check_uniqueness:
            if len(reflist) > 1:
                self.__logger.error('Ruleset name %s is not unique' % name)
                print_error('Ruleset name %s is not unique' % name)
                return None

        return reflist

    @classmethod
    def get_all_database_rulesetIds(self):
        """
        Return list of database ruleset ids.
        return list of references if OK
        return None if ruleset not found
        """
        return get_objref_by_val_and_attribute('Database', self, 'type')

    @classmethod
    def get_all_file_rulesetIds(self):
        """
        Return list of database ruleset ids.
        return list of references if OK
        return None if ruleset not found
        """
        return get_objref_by_val_and_attribute('File', self, 'type')

    @classmethod
    def add(self, ruleset):
        """
        Add an Ruleset to a list and Engine
        :param ruleset: Ruleset object to add to Engine and list
        return None if OK
        """

        if (ruleset.add() is None):
            self.__logger.debug("Adding ruleset %s to list" % ruleset)
            self.__rulesetList[ruleset.ruleset_id] = ruleset
            return None
        else:
            return 1

    @classmethod
    def delete(self, RulesetId):
        """
        Delete a ruleset from a list and Engine
        :param RulesetId: Ruleset id to delete from Engine and list
        return None if OK
        """

        ruleset = self.get_by_ref(RulesetId)
        if ruleset is not None:
            if ruleset.delete() is None:
                return None
            else:
                return 1
        else:
            print "Ruleset with id %s not found" % RulesetId
            return 1

    @classmethod
    def copy(self, ruleset_id, newname):
        """
        Add an Ruleset to a list and Engine
        :param ruleset: Ruleset id of the existing ruleset
        :param newname: Name of the new ruleset
        return new ruleset_id if OK, None if failure
        """

        ruleset = self.get_by_ref(ruleset_id)

        if ruleset.type == 'Database':
            newruleset = DxDatabaseRuleset(self.__engine)
            newruleset.from_ruleset(ruleset)
            newruleset.ruleset_name = newname
        elif ruleset.type == 'File':
            newruleset = DxFileRuleset(self.__engine)
            newruleset.from_ruleset(ruleset)
            newruleset.ruleset_name = newname

        if (newruleset.add() is None):
            self.__logger.debug("Adding ruleset %s to list" % newruleset)
            self.__rulesetList[newruleset.ruleset_id] = newruleset
            return newruleset.ruleset_id
        else:
            return None
