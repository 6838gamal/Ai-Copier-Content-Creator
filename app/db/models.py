from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DigitalProduct(Base):
    __tablename__ = "digital_products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    product_type = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    file_url = Column(String(500), nullable=False)

    def __repr__(self):
        return f"<DigitalProduct(title={self.title}, price={self.price})>"
