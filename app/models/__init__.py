from sqlalchemy import Column, String, Boolean, ForeignKey, Integer, Float
from ..db import Base


class Attribute(Base):
    __tablename__ = "attribute"
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True, nullable=False)
    type = Column(String(length=256), nullable=False)
    remote_reference = Column(String(256), nullable=False)
    key = Column(String(length=256), unique=True)

    __mapper_args__ = {
        'polymorphic_identity': 'attribute',
        'polymorphic_on': type
    }


class BooleanAttribute(Attribute):
    __tablename__ = "boolean_attribute"
    id = Column(Integer, ForeignKey('attribute.id'), primary_key=True)
    value = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity': bool.__name__
    }


class IntegerAttribute(Attribute):
    __tablename__ = "integer_attribute"
    id = Column(Integer, ForeignKey('attribute.id'), primary_key=True)
    value = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': int.__name__
    }


class FloatAttribute(Attribute):
    __tablename__ = "float_attribute"
    id = Column(Integer, ForeignKey('attribute.id'), primary_key=True)
    value = Column(Float)

    __mapper_args__ = {
        'polymorphic_identity': float.__name__
    }


class StringAttribute(Attribute):
    __tablename__ = "string_attribute"
    id = Column(Integer, ForeignKey('attribute.id'), primary_key=True)
    value = Column(String(length=4096))

    __mapper_args__ = {
        'polymorphic_identity': str.__name__
    }