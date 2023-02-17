import pprint

class FileRuleset_mixin:
    swagger_types = { 
     'file_ruleset_id' : 'integer',  
     'ruleset_name' : 'string',  
     'file_connector_id' : 'integer' 
     }

    swagger_map = { 
     'file_ruleset_id' : 'fileRulesetId',  
     'ruleset_name' : 'rulesetName',  
     'file_connector_id' : 'fileConnectorId' 
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
    def file_ruleset_id(self):
        if self.obj is not None and hasattr(self.obj,'file_ruleset_id'):
            return self.obj.file_ruleset_id
        else:
            return None

    @file_ruleset_id.setter
    def file_ruleset_id(self, file_ruleset_id):
        if self.obj is not None:
            self.obj.file_ruleset_id = file_ruleset_id
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
    def file_connector_id(self):
        if self.obj is not None and hasattr(self.obj,'file_connector_id'):
            return self.obj.file_connector_id
        else:
            return None

    @file_connector_id.setter
    def file_connector_id(self, file_connector_id):
        if self.obj is not None:
            self.obj.file_connector_id = file_connector_id
        else:
            raise ValueError("Object needs to be initialized first")
          