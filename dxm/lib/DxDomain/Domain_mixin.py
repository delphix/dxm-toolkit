import pprint

class Domain_mixin:
    swagger_types = { 
     'domain_name' : 'string',  
     'created_by' : 'string',  
     'default_algorithm_code' : 'string',  
     'default_tokenization_code' : 'string' 
     }

    swagger_map = { 
     'domain_name' : 'domainName',  
     'created_by' : 'createdBy',  
     'default_algorithm_code' : 'defaultAlgorithmCode',  
     'default_tokenization_code' : 'defaultTokenizationCode' 
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
    def domain_name(self):
        if self.obj is not None and hasattr(self.obj,'domain_name'):
            return self.obj.domain_name
        else:
            return None

    @domain_name.setter
    def domain_name(self, domain_name):
        if self.obj is not None:
            self.obj.domain_name = domain_name
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
    def default_algorithm_code(self):
        if self.obj is not None and hasattr(self.obj,'default_algorithm_code'):
            return self.obj.default_algorithm_code
        else:
            return None

    @default_algorithm_code.setter
    def default_algorithm_code(self, default_algorithm_code):
        if self.obj is not None:
            self.obj.default_algorithm_code = default_algorithm_code
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def default_tokenization_code(self):
        if self.obj is not None and hasattr(self.obj,'default_tokenization_code'):
            return self.obj.default_tokenization_code
        else:
            return None

    @default_tokenization_code.setter
    def default_tokenization_code(self, default_tokenization_code):
        if self.obj is not None:
            self.obj.default_tokenization_code = default_tokenization_code
        else:
            raise ValueError("Object needs to be initialized first")
          