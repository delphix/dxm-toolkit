import pprint

class ProfileSet_mixin:
    swagger_types = { 
     'profile_set_id' : 'integer',  
     'profile_set_name' : 'string',  
     'profile_expression_ids' : 'array',  
     'profile_type_expression_ids' : 'array',  
     'classifier_ids' : 'array',  
     'created_by' : 'string',  
     'created_time' : 'string',  
     'description' : 'string' 
     }

    swagger_map = { 
     'profile_set_id' : 'profileSetId',  
     'profile_set_name' : 'profileSetName',  
     'profile_expression_ids' : 'profileExpressionIds',  
     'profile_type_expression_ids' : 'profileTypeExpressionIds',  
     'classifier_ids' : 'classifierIds',  
     'created_by' : 'createdBy',  
     'created_time' : 'createdTime',  
     'description' : 'description' 
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
    def profile_set_id(self):
        if self.obj is not None and hasattr(self.obj,'profile_set_id'):
            return self.obj.profile_set_id
        else:
            return None

    @profile_set_id.setter
    def profile_set_id(self, profile_set_id):
        if self.obj is not None:
            self.obj.profile_set_id = profile_set_id
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def profile_set_name(self):
        if self.obj is not None and hasattr(self.obj,'profile_set_name'):
            return self.obj.profile_set_name
        else:
            return None

    @profile_set_name.setter
    def profile_set_name(self, profile_set_name):
        if self.obj is not None:
            self.obj.profile_set_name = profile_set_name
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def profile_expression_ids(self):
        if self.obj is not None and hasattr(self.obj,'profile_expression_ids'):
            return self.obj.profile_expression_ids
        else:
            return None

    @profile_expression_ids.setter
    def profile_expression_ids(self, profile_expression_ids):
        if self.obj is not None:
            self.obj.profile_expression_ids = profile_expression_ids
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def profile_type_expression_ids(self):
        if self.obj is not None and hasattr(self.obj,'profile_type_expression_ids'):
            return self.obj.profile_type_expression_ids
        else:
            return None

    @profile_type_expression_ids.setter
    def profile_type_expression_ids(self, profile_type_expression_ids):
        if self.obj is not None:
            self.obj.profile_type_expression_ids = profile_type_expression_ids
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def classifier_ids(self):
        if self.obj is not None and hasattr(self.obj,'classifier_ids'):
            return self.obj.classifier_ids
        else:
            return None

    @classifier_ids.setter
    def classifier_ids(self, classifier_ids):
        if self.obj is not None:
            self.obj.classifier_ids = classifier_ids
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
    def created_time(self):
        if self.obj is not None and hasattr(self.obj,'created_time'):
            return self.obj.created_time
        else:
            return None

    @created_time.setter
    def created_time(self, created_time):
        if self.obj is not None:
            self.obj.created_time = created_time
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
          