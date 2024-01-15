import pprint

class Application_mixin:
    swagger_types = { 
     'application_id' : 'integer',  
     'application_name' : 'string' 
     }

    swagger_map = { 
     'application_id' : 'applicationId',  
     'application_name' : 'applicationName' 
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
    def application_id(self):
        if self.obj is not None and hasattr(self.obj,'application_id'):
            return self.obj.application_id
        else:
            return None

    @application_id.setter
    def application_id(self, application_id):
        if self.obj is not None:
            self.obj.application_id = application_id
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def application_name(self):
        if self.obj is not None and hasattr(self.obj,'application_name'):
            return self.obj.application_name
        else:
            return None

    @application_name.setter
    def application_name(self, application_name):
        if self.obj is not None:
            self.obj.application_name = application_name
        else:
            raise ValueError("Object needs to be initialized first")
          