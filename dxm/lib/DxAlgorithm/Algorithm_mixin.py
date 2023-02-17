import pprint

class Algorithm_mixin:
    swagger_types = { 
     'algorithm_name' : 'string',  
     'algorithm_type' : 'string',  
     'created_by' : 'string',  
     'description' : 'string',  
     'is_tokenization_supported' : 'boolean',  
     'framework_id' : 'integer',  
     'plugin_id' : 'integer',  
     'fields' : 'array',  
     'algorithm_extension' : 'object' 
     }

    swagger_map = { 
     'algorithm_name' : 'algorithmName',  
     'algorithm_type' : 'algorithmType',  
     'created_by' : 'createdBy',  
     'description' : 'description',  
     'is_tokenization_supported' : 'isTokenizationSupported',  
     'framework_id' : 'frameworkId',  
     'plugin_id' : 'pluginId',  
     'fields' : 'fields',  
     'algorithm_extension' : 'algorithmExtension' 
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
    def algorithm_name(self):
        if self.obj is not None and hasattr(self.obj,'algorithm_name'):
            return self.obj.algorithm_name
        else:
            return None

    @algorithm_name.setter
    def algorithm_name(self, algorithm_name):
        if self.obj is not None:
            self.obj.algorithm_name = algorithm_name
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def algorithm_type(self):
        if self.obj is not None and hasattr(self.obj,'algorithm_type'):
            return self.obj.algorithm_type
        else:
            return None

    @algorithm_type.setter
    def algorithm_type(self, algorithm_type):
        if self.obj is not None:
            self.obj.algorithm_type = algorithm_type
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def created_by(self):
        if self.obj is not None and hasattr(self.obj,'created_by'):
            return self.obj.created_by
        else:
            return None

    @created_by.setter
    def created_by(self, created_by):
        if self.obj is not None:
            self.obj.created_by = created_by
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def description(self):
        if self.obj is not None and hasattr(self.obj,'description'):
            return self.obj.description
        else:
            return None

    @description.setter
    def description(self, description):
        if self.obj is not None:
            self.obj.description = description
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def is_tokenization_supported(self):
        if self.obj is not None and hasattr(self.obj,'is_tokenization_supported'):
            return self.obj.is_tokenization_supported
        else:
            return None

    @is_tokenization_supported.setter
    def is_tokenization_supported(self, is_tokenization_supported):
        if self.obj is not None:
            self.obj.is_tokenization_supported = is_tokenization_supported
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def framework_id(self):
        if self.obj is not None and hasattr(self.obj,'framework_id'):
            return self.obj.framework_id
        else:
            return None

    @framework_id.setter
    def framework_id(self, framework_id):
        if self.obj is not None:
            self.obj.framework_id = framework_id
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def plugin_id(self):
        if self.obj is not None and hasattr(self.obj,'plugin_id'):
            return self.obj.plugin_id
        else:
            return None

    @plugin_id.setter
    def plugin_id(self, plugin_id):
        if self.obj is not None:
            self.obj.plugin_id = plugin_id
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def fields(self):
        if self.obj is not None and hasattr(self.obj,'fields'):
            return self.obj.fields
        else:
            return None

    @fields.setter
    def fields(self, fields):
        if self.obj is not None:
            self.obj.fields = fields
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def algorithm_extension(self):
        if self.obj is not None and hasattr(self.obj,'algorithm_extension'):
            return self.obj.algorithm_extension
        else:
            return None

    @algorithm_extension.setter
    def algorithm_extension(self, algorithm_extension):
        if self.obj is not None:
            self.obj.algorithm_extension = algorithm_extension
        else:
            raise ValueError("Object needs to be initialized first")
          