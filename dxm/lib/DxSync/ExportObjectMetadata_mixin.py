import pprint

class ExportObjectMetadata_mixin:
    swagger_types = { 
     'object_identifier' : 'object',  
     'object_type' : 'string',  
     'revision_hash' : 'string' 
     }

    swagger_map = { 
     'object_identifier' : 'objectIdentifier',  
     'object_type' : 'objectType',  
     'revision_hash' : 'revisionHash' 
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
    def object_identifier(self):
        if self.obj is not None and hasattr(self.obj,'object_identifier'):
            return self.obj.object_identifier
        else:
            return None

    @object_identifier.setter
    def object_identifier(self, object_identifier):
        if self.obj is not None:
            self.obj.object_identifier = object_identifier
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def object_type(self):
        if self.obj is not None and hasattr(self.obj,'object_type'):
            return self.obj.object_type
        else:
            return None

    @object_type.setter
    def object_type(self, object_type):
        if self.obj is not None:
            self.obj.object_type = object_type
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def revision_hash(self):
        if self.obj is not None and hasattr(self.obj,'revision_hash'):
            return self.obj.revision_hash
        else:
            return None

    @revision_hash.setter
    def revision_hash(self, revision_hash):
        if self.obj is not None:
            self.obj.revision_hash = revision_hash
        else:
            raise ValueError("Object needs to be initialized first")
          