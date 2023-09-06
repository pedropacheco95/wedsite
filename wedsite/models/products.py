from email.policy import default
from wedsite import model 
from wedsite.sql_db import db
from sqlalchemy import Column, Integer , String , Text ,Float , Boolean , ForeignKey
from sqlalchemy.orm import relationship

from wedsite.tools.input_tools import Field, Block, Tab , Form

class Product(model.Imageable ,model.Model):
    __tablename__ = 'products'
    __table_args__ = {'extend_existing': True}
    page_title = 'Produtos'
    model_name = 'Product'

    id = Column(Integer, primary_key=True)

    imageable_id = Column(Integer, ForeignKey('imageables.imageable_id'))
    imageable = relationship('Imageable', backref=db.backref('products', uselist=False, cascade='all,delete-orphan'),post_update=True)

    name = Column(String(80), unique=True, nullable=False)
    description = Column(Text)
    price = Column(Float)
    price_paid = Column(Float, default= 0.0)
    store = Column(Text)
    show_price = Column(Boolean, default=True)
    priority = Column(Integer, default=10)

    contributions = relationship('Contribution', back_populates="product", cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': model_name,
    }

    def calculate_percentage(self):
        if self.price:
            ratio = (self.price_paid/self.price)
            return ratio * 100 if ratio <=1 else 100
        else:
            return 0.0

    def missing_value(self):
        return self.price - self.price_paid if self.price >= self.price_paid else 0

    def is_paid(self):
        return False if self.missing_value()>0 else True

    def update_price_paid(self):
        price_paid = sum([contribution.value_contributed for contribution in self.contributions])
        self.price_paid = price_paid
        self.save()

    def display_all_info(self):
        searchable_column = {'field': 'name','label':'Nome'}
        table_columns = [
            {'field': 'id','label':'Numero'},
            searchable_column,
            {'field': 'price','label':'Preço'},
            {'field': 'price_paid','label':'Valor Pago'},
        ]
        return searchable_column , table_columns

    def get_create_form(self):
        def get_field(name,label,type,required=False,related_model=None):
            return Field(instance_id=self.id,model=self.model_name,name=name,label=label,type=type,required=required,related_model=related_model)
        form = Form()
        # Create Picture block

        fields = [get_field(name='imageable',label='Fotografia',type='MultiplePictures')]
        picture_block = Block('picture_block',fields)
        form.add_block(picture_block)

        # Create Info block

        fields = [
            get_field(name='name',label='Nome',type='Text',required=True),
            get_field(name='description',label='Descrição',type='Text'),
            get_field(name='price',label='Preço',type='Float',required=True),
            get_field(name='store',label='Loja',type='Text'),
            get_field(name='show_price',label='Mostrar Preço',type='Boolean'),
            get_field(name='priority',label='Prioridade',type='Integer'),
        ]
        info_block = Block('info_block',fields)
        form.add_block(info_block)

        return form