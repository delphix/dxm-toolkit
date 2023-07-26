import pprint

class Environment_mixin:
    swagger_types = { 
     'environment_id' : 'integer',  
     'environment_name' : 'string',  
     'application_id' : 'integer',  
     'purpose' : 'string',  
     'is_workflow_enabled' : 'boolean' 
     }

    swagger_map = { 
     'environment_id' : 'environmentId',  
     'environment_name' : 'environmentName',  
     'application_id' : 'applicationId',  
     'purpose' : 'purpose',  
     'is_workflow_enabled' : 'isWorkflowEnabled' 
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
    def environment_id(self):
        if self.obj is not None and hasattr(self.obj,'environment_id'):
            return self.obj.environment_id
        else:
            return None

    @environment_id.setter
    def environment_id(self, environment_id):
        if self.obj is not None:
            self.obj.environment_id = environment_id
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def environment_name(self):
        if self.obj is not None and hasattr(self.obj,'environment_name'):
            return self.obj.environment_name
        else:
            return None

    @environment_name.setter
    def environment_name(self, environment_name):
        if self.obj is not None:
            self.obj.environment_name = environment_name
        else:
            raise ValueError("Object needs to be initialized first")
     
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
    def purpose(self):
        if self.obj is not None and hasattr(self.obj,'purpose'):
            return self.obj.purpose
        else:
            return None

    @purpose.setter
    def purpose(self, purpose):
        if self.obj is not None:
            self.obj.purpose = purpose
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def is_workflow_enabled(self):
        if self.obj is not None and hasattr(self.obj,'is_workflow_enabled'):
            return self.obj.is_workflow_enabled
        else:
            return None

    @is_workflow_enabled.setter
    def is_workflow_enabled(self, is_workflow_enabled):
        if self.obj is not None:
            self.obj.is_workflow_enabled = is_workflow_enabled
        else:
            raise ValueError("Object needs to be initialized first")
          