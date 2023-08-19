from wedsite import model 
from wedsite.sql_db import db
from sqlalchemy import Column, Integer , Text , Boolean , DateTime

from wedsite.tools.input_tools import Field, Block, Tab , Form

class Client(db.Model ,model.Model,model.Base):
    __tablename__ = 'client'
    __table_args__ = {'extend_existing': True}
    page_title = 'Clientes'
    model_name = 'Client'

    id = Column(Integer, primary_key=True)
    name = Column(Text)

    main_title = Column(Text)
    datetime = Column(DateTime)

    party_location_name = Column(Text)
    party_location_url = Column(Text)
    party_image_path = Column(Text)

    church_location_name = Column(Text)
    church_location_url = Column(Text)
    church_image_path = Column(Text)

    use_mbway = Column(Boolean)
    mbway_numbers = Column(Text)
    use_nib = Column(Boolean)
    nibs = Column(Text)

    index_backgroud_image_path = Column(Text)
    index_backgroud_image_phone_path = Column(Text)

    products_all_background_image_path = Column(Text)
    confirmation_background_image_path = Column(Text)
    faqs_background_image_path = Column(Text)

    def get_mbway_numbers(self):
        return self.mbway_numbers.split(';')
    
    def get_nibs(self):
        return self.nibs.split(';')
    
    def get_formatted_datetime(self):
        months = {
            1: "Janeiro",
            2: "Fevereiro",
            3: "Março",
            4: "Abril",
            5: "Maio",
            6: "Junho",
            7: "Julho",
            8: "Agosto",
            9: "Setembro",
            10: "Outubro",
            11: "Novembro",
            12: "Dezembro"
        }
        
        day = self.datetime.day
        month = months[self.datetime.month]
        time = self.datetime.strftime("%H:%M")
        
        formatted_datetime = f"{day} de {month}"
        return [formatted_datetime,time]
    
    def get_formatted_mbways(self):
        mbways = self.get_mbway_numbers()
        formatted = ''
        for mbway in mbways:
            formatted += mbway + ' | '
        return formatted[:-3]
    
    def get_formatted_nibs(self):
        nibs = self.get_nibs()
        formatted = ''
        for nib in nibs:
            formatted += nib + ' | '
        return formatted[:-3]
    
    def display_all_info(self):
        searchable_column = {'field': 'name','label':'Nome'}
        table_columns = [
            {'field': 'id','label':'Numero'},
            searchable_column
        ]
        return searchable_column , table_columns
    
    def get_create_form(self):
        def get_field(name,label,type,required=False,related_model=None,mandatory_path=None):
            return Field(instance_id=self.id,model=self.model_name,name=name,label=label,type=type,required=required,related_model=related_model,mandatory_path=mandatory_path)
        form = Form()

        # Create Info block
        fields = [
            get_field(name='name',label='Nome',type='Text',required=True),
            get_field(name='main_title',label='Título',type='Text',required=True),
            get_field(name='datetime',label='Data e dia',type='DateTime',required=True),
        ]
        info_block = Block('info_block',fields)
        form.add_block(info_block)

        # Create Caracteristicas Físicas tab
        fields = [
            get_field(name='use_mbway',label='Mostrar Mbway',type='Boolean'),
            get_field(name='mbway_numbers',label='Numeros de mbway',type='Text'),
            get_field(name='use_nib',label='Mostrar NIB',type='Boolean'),
            get_field(name='nibs',label='NIBs',type='Text'),
        ]
        form.add_tab(Tab(title='Informação de pagamento',fields=fields,orientation='vertical'))

        # Create Index tab
        fields = [
            get_field(name='index_backgroud_image_path',label='Imagem de fundo computador',type='Picture',mandatory_path='index_background.jpg'),
            get_field(name='index_backgroud_image_phone_path',label='Imagem de fundo telemovel',type='Picture',mandatory_path='index_background_phone.jpg'),
        ]
        form.add_tab(Tab(title='Homepage',fields=fields,orientation='horizontal'))

        # Create Faqs tab
        fields = [
            get_field(name='faqs_background_image_path',label='Imagem de fundo computador',type='Picture',mandatory_path='faqs_background.jpg'),
        ]
        form.add_tab(Tab(title='Perguntas Frequentes',fields=fields,orientation='horizontal'))

        # Create Products tab
        fields = [
            get_field(name='products_all_background_image_path',label='Imagem de fundo computador',type='Picture',mandatory_path='products_all_background.jpg'),
        ]
        form.add_tab(Tab(title='Lista de casamento',fields=fields,orientation='horizontal'))

        # Create Confirmation tab
        fields = [
            get_field(name='confirmation_background_image_path',label='Imagem de fundo computador',type='Picture',mandatory_path='confirmation_background.jpg'),
        ]
        form.add_tab(Tab(title='Confirmação',fields=fields,orientation='horizontal'))

        # Create Informations tab
        fields = [
            get_field(name='party_location_name',label='Festa',type='Text'),
            get_field(name='party_location_url',label='Local da festa (url)',type='Text'),
            get_field(name='church_location_name',label='Igreja',type='Text'),
            get_field(name='church_location_url',label='Local da igreja (url)',type='Text'),
            get_field(name='party_image_path',label='Imagem da festa',type='Picture'),
            get_field(name='church_image_path',label='Imagem da igreja',type='Picture'),
        ]
        form.add_tab(Tab(title='Informações',fields=fields,orientation='vertical'))


        return form
