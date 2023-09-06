from wedsite import model 
from wedsite.sql_db import db
from sqlalchemy import Column, Integer , Text , Boolean

from wedsite.tools.input_tools import Field, Block, Tab , Form

class FAQ(db.Model ,model.Model,model.Base):
    __tablename__ = 'faq'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    page_title = 'FAQs'
    model_name = 'FAQ'

    name = Column(Text)
    question = Column(Text)
    answer = Column(Text)

    def display_all_info(self):
        searchable_column = {'field': 'question','label':'Pergunta'}
        table_columns = [
            {'field': 'id','label':'Numero'},
            searchable_column,
            {'field': 'answer','label':'Resposta'},
            
        ]
        return searchable_column , table_columns

    def get_create_form(self):
        def get_field(name,label,type,required=False,related_model=None):
            return Field(instance_id=self.id,model=self.model_name,name=name,label=label,type=type,required=required,related_model=related_model)
        form = Form()
        # Create Info block

        fields = [
            get_field(name='question',label='Pergunta',type='Text',required=True),
            get_field(name='answer',label='Resposta',type='Text',required=True),
        ]
        info_block = Block('info_block',fields)
        form.add_block(info_block)

        return form
