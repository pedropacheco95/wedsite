from wedsite import model 
from wedsite.sql_db import db
from sqlalchemy import Column, Integer , String , Text ,Float , ForeignKey
from sqlalchemy.orm import relationship

from wedsite.tools import messages
from wedsite.tools.input_tools import Field, Block, Tab , Form

class Contribution(db.Model ,model.Model,model.Base):
    __tablename__ = 'contribution'
    __table_args__ = {'extend_existing': True}
    page_title = 'Contribuições'
    model_name = 'Contribution'

    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    value_contributed = Column(Float)
    message = Column(Text)
    product_id = Column(Integer, ForeignKey('products.id'))

    product = relationship('Product', back_populates="contributions")

    def thank_you_message(self):
        return messages.generate_ty_contribution_message(self.name)

    def display_all_info(self):
        searchable_column = {'field': 'name','label':'Nome'}
        table_columns = [
            {'field': 'id','label':'Numero'},
            searchable_column,
            {'field': 'value_contributed','label':'Valor'},
            {'field': 'product','label':'Product'},
            
        ]
        return searchable_column , table_columns

    def get_create_form(self):
        def get_field(name,label,type,required=False,related_model=None):
            return Field(instance_id=self.id,model=self.model_name,name=name,label=label,type=type,required=required,related_model=related_model)
        form = Form()
        # Create Info block

        fields = [
            get_field(name='name',label='Nome',type='Text',required=True),
            get_field(name='value_contributed',label='Valor',type='Float',required=True),
            get_field(name='message',label='Mensagem',type='Text'),
        ]
        info_block = Block('info_block',fields)
        form.add_block(info_block)

        return form
    