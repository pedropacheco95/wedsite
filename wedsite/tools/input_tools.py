
from wedsite.tools import image_tools
from datetime import datetime

from wedsite.model import Image, Imageable

class Field:

    valid_types = ['Text','Integer',
                'Float','Password',
                'Select','Picture',
                'EditablePicture', 'MultiplePictures',
                'ManyToMany','Color',
                'OneToMany','ManyToOne',
                'Boolean','Date',
                'DateTime']

    def __init__(self, instance_id, model, label, name, type, value = None, options = None, required = False, related_model = None,mandatory_path = None):
        if label is None:
            raise ValueError('label is required')
        if name is None:
            raise ValueError('name is required')
        if type is None:
            raise ValueError('type is required')
        if type not in self.valid_types:
            raise ValueError('type is not valid')
        self.instance_id = instance_id
        self.model = model
        self.label = label
        self.name = name
        self.type = type
        self.value = value
        self.options = options
        self.required = required
        self.related_model = related_model
        self.mandatory_path = mandatory_path

        self.set_special_fields = {
            'Picture': self.set_picture_value,
            'EditablePicture': self.set_picture_value,
            'MultiplePictures': self.set_multiple_picture_value,
            'ManyToMany': self.set_relationship_value,
            'OneToMany': self.set_relationship_value,
            'ManyToOne': self.set_relationship_value,
            'Date': self.set_date_value,
            'DateTime': self.set_date_value,
            'Boolean': self.set_boolean_value,
        }


    def get_field_dict(self):
        return {
            "type": self.type,
            "label": self.label,
            "name": self.name,
            "options": self.options if self.options else None,
            "required": self.required if self.required else False,
            "related_model": self.related_model if self.related_model else None,
        }
    
    def set_picture_value(self, request):
        now = datetime.now()
        formatted = now.strftime("%Y%m%d%H%M%S")
        file , name = image_tools.file_handler(request.files.getlist(self.name)[0]) if request.files.getlist(self.name) else None 
        name = '{folder}/{added}_{name}'.format(folder=self.model,name=name,added=formatted)
        if self.mandatory_path:
            name = self.mandatory_path
        saved = image_tools.save_file(file,name)
        if saved:
            self.value = name
        return True
    
    def set_multiple_picture_value(self, request):
        now = datetime.now()
        formatted = now.strftime("%Y%m%d%H%M%S")
        files = request.files.getlist(self.name) if request.files.getlist(self.name) else None
        self.value = []
        if files:
            for i, file in enumerate(files):
                image = Image()
                file , name = image_tools.file_handler(file)
                name = '{folder}/{added}_{index}_{name}'.format(folder=self.model,name=name,added=formatted,index=i)
                if self.mandatory_path:
                    name = self.mandatory_path
                saved = image_tools.save_file(file,name)
                if saved:
                    image.filename = name
                    image.create()
                    self.value.append(image)
        return True
    
    def set_relationship_value(self, request):
        self.value = [int(ele) for ele in request.form.getlist(self.name) if request.form.getlist(self.name)]
        return True
    
    def set_date_value(self, request):
        string_format = {
            'Date': '%d/%m/%Y',
            'DateTime': '%d/%m/%Y, %H:%M',
        }
        date_obj = datetime.strptime(request.form[self.name], string_format[self.type]) if self.name in request.form else None
        self.value = date_obj
        return True
    
    def set_date_value(self, request):
        string_formats = {
            'Date': ['%d/%m/%Y'],
            'DateTime': ['%d/%m/%Y, %H:%M', '%Y-%m-%dT%H:%M'],
        }

        if self.name in request.form:
            input_value = request.form[self.name]
            for format in string_formats[self.type]:
                try:
                    date_obj = datetime.strptime(input_value, format)
                    self.value = date_obj
                    return True
                except ValueError:
                    pass

        self.value = None
        return False
    
    def set_boolean_value(self, request):
        self.value = True if request.form[self.name] == 'true' else False
        return True

    def set_value(self, request):
        if self.type in self.set_special_fields.keys():
            return self.set_special_fields[self.type](request)
        self.value = request.form[self.name] if self.name in request.form else None
        return True

class Block:
    def __init__(self,name,fields):
        if name is None:
            raise ValueError('name is required')
        if fields is None:
            raise ValueError('fields is required')
        if not all(isinstance(item, Field) for item in fields):
            raise ValueError('fields is not a list of Field objects')
        self.fields = fields
        self.name = name

    def get_block_dict(self):
        return {
            "name": self.name,
            "fields": self.fields,
        }

class Tab:
    def __init__(self, title, fields,orientation = 'vertical'):
        if title is None:
            raise ValueError('tab_name is required')
        if fields is None:
            raise ValueError('fields is required')
        if not all(isinstance(item, Field) for item in fields):
            raise ValueError('fields is not a list of Field objects')
        self.title = title
        self.fields = fields
        self.orientation = orientation

    def get_tab_dict(self):
        return {
            "title": self.title,
            "fields": self.fields,
            "orientation": self.orientation,
        }

class Form:

    def __init__(self):
        self.blocks = []
        self.tabs = []
        self.fields = []

    def add_block(self,block):
        if not isinstance(block, Block):
            raise ValueError('block is not a Block object')
        if block.name in [block.name for block in self.blocks]:
            raise ValueError('name already exists')
        if block.name not in ['picture_block','info_block']:
            raise ValueError('name is not valid')
        self.blocks.append(block)
        for field in block.fields:
            self.fields.append(field)
        
    def add_tab(self,tab):
        if not isinstance(tab, Tab):
            raise ValueError('tab is not a Tab object')
        self.tabs.append(tab)
        for field in tab.fields:
            self.fields.append(field)

    def get_form_dict(self):
        return {
            "main": self.blocks,
            "tabs": self.tabs,
        }

    def set_values(self,request):
        for field in self.fields:
            field.set_value(request)
        return {field.name: field.value for field in self.fields}
