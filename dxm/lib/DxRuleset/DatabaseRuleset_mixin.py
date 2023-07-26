import pprint

class DatabaseRuleset_mixin:
    swagger_types = { 
     'database_ruleset_id' : 'integer',  
     'ruleset_name' : 'string',  
     'database_connector_id' : 'integer',  
     'refresh_drops_tables' : 'boolean' 
     }

    swagger_map = { 
     'database_ruleset_id' : 'databaseRulesetId',  
     'ruleset_name' : 'rulesetName',  
     'database_connector_id' : 'databaseConnectorId',  
     'refresh_drops_tables' : 'refreshDropsTables' 
     }

    @property
    def obj(self):
        if self._obj is not None:
            return self._obj
        else:
            return None

    @obj.setter
    def obj(self, value):
        self._obj = value

    def to_dict_all(self):
        return { k:getattr(self, k) for k,v in self.swagger_map.items() if hasattr(self, k) }

    def to_str(self):
        return pprint.pformat(self.to_dict_all())

    def __repr__(self):
        return self.to_str()

     
    @property
    def database_ruleset_id(self):
        if self.obj is not None and hasattr(self.obj,'database_ruleset_id'):
            return self.obj.database_ruleset_id
        else:
            return None

    @database_ruleset_id.setter
    def database_ruleset_id(self, database_ruleset_id):
        if self.obj is not None:
            self.obj.database_ruleset_id = database_ruleset_id
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def ruleset_name(self):
        if self.obj is not None and hasattr(self.obj,'ruleset_name'):
            return self.obj.ruleset_name
        else:
            return None

    @ruleset_name.setter
    def ruleset_name(self, ruleset_name):
        if self.obj is not None:
            self.obj.ruleset_name = ruleset_name
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def database_connector_id(self):
        if self.obj is not None and hasattr(self.obj,'database_connector_id'):
            return self.obj.database_connector_id
        else:
            return None

    @database_connector_id.setter
    def database_connector_id(self, database_connector_id):
        if self.obj is not None:
            self.obj.database_connector_id = database_connector_id
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def refresh_drops_tables(self):
        if self.obj is not None and hasattr(self.obj,'refresh_drops_tables'):
            return self.obj.refresh_drops_tables
        else:
            return None

    @refresh_drops_tables.setter
    def refresh_drops_tables(self, refresh_drops_tables):
        if self.obj is not None:
            self.obj.refresh_drops_tables = refresh_drops_tables
        else:
            raise ValueError("Object needs to be initialized first")
          