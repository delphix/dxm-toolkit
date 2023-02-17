import pprint

class FileFormat_mixin:
    swagger_types = { 
     'file_format_id' : 'integer',  
     'file_format_name' : 'string',  
     'file_format_type' : 'string',  
     'header' : 'integer',  
     'footer' : 'integer' 
     }

    swagger_map = { 
     'file_format_id' : 'fileFormatId',  
     'file_format_name' : 'fileFormatName',  
     'file_format_type' : 'fileFormatType',  
     'header' : 'header',  
     'footer' : 'footer' 
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
    def file_format_id(self):
        if self.obj is not None and hasattr(self.obj,'file_format_id'):
            return self.obj.file_format_id
        else:
            return None

    @file_format_id.setter
    def file_format_id(self, file_format_id):
        if self.obj is not None:
            self.obj.file_format_id = file_format_id
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def file_format_name(self):
        if self.obj is not None and hasattr(self.obj,'file_format_name'):
            return self.obj.file_format_name
        else:
            return None

    @file_format_name.setter
    def file_format_name(self, file_format_name):
        if self.obj is not None:
            self.obj.file_format_name = file_format_name
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def file_format_type(self):
        if self.obj is not None and hasattr(self.obj,'file_format_type'):
            return self.obj.file_format_type
        else:
            return None

    @file_format_type.setter
    def file_format_type(self, file_format_type):
        if self.obj is not None:
            self.obj.file_format_type = file_format_type
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def header(self):
        if self.obj is not None and hasattr(self.obj,'header'):
            return self.obj.header
        else:
            return None

    @header.setter
    def header(self, header):
        if self.obj is not None:
            self.obj.header = header
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def footer(self):
        if self.obj is not None and hasattr(self.obj,'footer'):
            return self.obj.footer
        else:
            return None

    @footer.setter
    def footer(self, footer):
        if self.obj is not None:
            self.obj.footer = footer
        else:
            raise ValueError("Object needs to be initialized first")
          