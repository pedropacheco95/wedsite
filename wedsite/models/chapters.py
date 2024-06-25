from wedsite import model 
from wedsite.sql_db import db
from sqlalchemy import Column, Integer , String
from sqlalchemy.orm import relationship

from wedsite.tools.input_tools import Field, Block , Form

class Chapter(db.Model ,model.Model,model.Base):
    __tablename__ = 'chapter'
    __table_args__ = {'extend_existing': True}
    page_title = 'Capítulos'
    model_name = 'Chapter'

    id = Column(Integer, primary_key=True)
    name = Column(String(80))

    products = relationship('Product', back_populates="chapter", cascade="all, delete-orphan")

    def display_all_info(self):
        searchable_column = {'field': 'name','label':'Nome'}
        table_columns = [
            {'field': 'id','label':'Numero'},
            searchable_column,
            {'field': 'products','label':'Products'},
            
        ]
        return searchable_column , table_columns

    def get_create_form(self):
        def get_field(name,label,type,required=False,related_model=None):
            return Field(instance_id=self.id,model=self.model_name,name=name,label=label,type=type,required=required,related_model=related_model)
        form = Form()
        # Create Info block

        fields = [
            get_field(name='name',label='Nome',type='Text',required=True),
        ]
        info_block = Block('info_block',fields)
        form.add_block(info_block)

        return form
    
    def products_paid(self):
        return [product for product in self.products if product.is_paid()]
    
    def products_not_paid(self):
        return [product for product in self.products if not product.is_paid()]
    