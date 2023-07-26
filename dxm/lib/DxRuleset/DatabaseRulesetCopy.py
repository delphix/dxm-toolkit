import pprint

class DatabaseRulesetCopy_mixin:
    swagger_types = { 
     'new_ruleset_name' : 'string' 
     }

    swagger_map = { 
     'new_ruleset_name' : 'newRulesetName' 
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
    def new_ruleset_name(self):
        if self.obj is not None and hasattr(self.obj,'new_ruleset_name'):
            return self.obj.new_ruleset_name
        else:
            return None

    @new_ruleset_name.setter
    def new_ruleset_name(self, new_ruleset_name):
        if self.obj is not None:
            self.obj.new_ruleset_name = new_ruleset_name
        else:
            raise ValueError("Object needs to be initialized first")
          