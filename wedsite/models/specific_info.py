from wedsite import model 
from wedsite.sql_db import db
from sqlalchemy import Column, Integer , Text , JSON

class WebsiteCostumization(db.Model ,model.Model,model.Base):
    __tablename__ = 'website_costumization'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    
    name = Column(Text)
    information = Column(JSON, nullable=True)
