from wedsite import model 
from wedsite.sql_db import db
from sqlalchemy import Column, Integer , String , Text , ForeignKey , Boolean
from sqlalchemy.orm import relationship

from wedsite.tools.input_tools import Field, Block, Tab , Form

class User(db.Model ,model.Model,model.Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    page_title = 'Utilizadores'
    model_name = 'User'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(Text, nullable=False)
    generated_code = Column(Integer)

    def display_all_info(self):
        searchable_column = {'field': 'name','label':'Nome'}
        table_columns = [
            {'field': 'id','label':'Numero'},
            searchable_column,
            {'field': 'username','label':'Username'},
            {'field': 'email','label':'Email'},
        ]
        return searchable_column , table_columns

    def get_create_form(self):
        def get_field(name,label,type,required=False,related_model=None):
            return Field(instance_id=self.id,model=self.model_name,name=name,label=label,type=type,required=required,related_model=related_model)
        form = Form()
        # Create Info block

        fields = [
            get_field(name='name',label='Nome',type='Text',required=True),
            get_field(name='username',label='Username',type='Text',required=True),
            get_field(name='email',label='Email',type='Text',required=True),
        ]
        info_block = Block('info_block',fields)
        form.add_block(info_block)

        return form