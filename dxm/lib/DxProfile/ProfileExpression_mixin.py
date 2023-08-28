import pprint

class ProfileExpression_mixin:
    swagger_types = { 
     'profile_expression_id' : 'integer',  
     'domain_name' : 'string',  
     'expression_name' : 'string',  
     'regular_expression' : 'string',  
     'created_by' : 'string',  
     'data_level_profiling' : 'boolean' 
     }

    swagger_map = { 
     'profile_expression_id' : 'profileExpressionId',  
     'domain_name' : 'domainName',  
     'expression_name' : 'expressionName',  
     'regular_expression' : 'regularExpression',  
     'created_by' : 'createdBy',  
     'data_level_profiling' : 'dataLevelProfiling' 
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
    def profile_expression_id(self):
        if self.obj is not None and hasattr(self.obj,'profile_expression_id'):
            return self.obj.profile_expression_id
        else:
            return None

    @profile_expression_id.setter
    def profile_expression_id(self, profile_expression_id):
        if self.obj is not None:
            self.obj.profile_expression_id = profile_expression_id
        else:
            raise ValueError("Object needs to be initialized first")
     
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
    def expression_name(self):
        if self.obj is not None and hasattr(self.obj,'expression_name'):
            return self.obj.expression_name
        else:
            return None

    @expression_name.setter
    def expression_name(self, expression_name):
        if self.obj is not None:
            self.obj.expression_name = expression_name
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def regular_expression(self):
        if self.obj is not None and hasattr(self.obj,'regular_expression'):
            return self.obj.regular_expression
        else:
            return None

    @regular_expression.setter
    def regular_expression(self, regular_expression):
        if self.obj is not None:
            self.obj.regular_expression = regular_expression
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
    def data_level_profiling(self):
        if self.obj is not None and hasattr(self.obj,'data_level_profiling'):
            return self.obj.data_level_profiling
        else:
            return None

    @data_level_profiling.setter
    def data_level_profiling(self, data_level_profiling):
        if self.obj is not None:
            self.obj.data_level_profiling = data_level_profiling
        else:
            raise ValueError("Object needs to be initialized first")
          