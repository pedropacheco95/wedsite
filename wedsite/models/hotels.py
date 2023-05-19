from wedsite import model 
from wedsite.sql_db import db
from sqlalchemy import Column, Integer , Text , Boolean

from wedsite.tools.input_tools import Field, Block, Tab , Form

class Hotel(db.Model ,model.Model,model.Base):
    __tablename__ = 'hotel'
    __table_args__ = {'extend_existing': True}
    page_title = 'Hotéis'
    model_name = 'Hotel'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    adress = Column(Text)
    phone = Column(Text)
    email = Column(Text)

    def display_all_info(self):
        searchable_column = {'field': 'name','label':'Nome'}
        table_columns = [
            {'field': 'id','label':'Numero'},
            searchable_column,
        ]
        return searchable_column , table_columns

    def get_create_form(self):
        def get_field(name,label,type,required=False,related_model=None):
            return Field(instance_id=self.id,model=self.model_name,name=name,label=label,type=type,required=required,related_model=related_model)
        form = Form()
        # Create Info block

        fields = [
            get_field(name='name',label='Nome',type='Text',required=True),
            get_field(name='adress',label='Endereço',type='Text'),
            get_field(name='phone',label='Telefone',type='Text'),
            get_field(name='email',label='Email',type='Text'),

        ]
        info_block = Block('info_block',fields)
        form.add_block(info_block)

        return form
