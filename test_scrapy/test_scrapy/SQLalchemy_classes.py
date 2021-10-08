from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func, UniqueConstraint, Date, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Keywords_and_quotes(Base):
    __tablename__ = 'keywords_and_quotes'
    keyword_id = Column(ForeignKey('keyword.keyword_id'), primary_key=True)
    quote_id = Column(ForeignKey('quote.quote_id'), primary_key=True)
    quote = relationship("Quote")


class Author(Base):
    __tablename__ = 'author'
    author_id = Column(Integer, primary_key=True, )
    name = Column(String(100), nullable=False)
    birthday = Column(String(50), nullable=True)
    link = Column(String(100), nullable=False)
    author_info = Column(Text, nullable=True)


class Keyword(Base):
    __tablename__ = 'keyword'
    keyword_id = Column(Integer, primary_key=True, )
    keyword = Column(String(50), nullable=False)
    quote = relationship("Keywords_and_quotes")


class Quote(Base):
    __tablename__ = 'quote'
    quote_id = Column(Integer, primary_key=True, )
    author_id = Column(Integer, ForeignKey('author.author_id', onupdate="CASCADE", ondelete="CASCADE"))
    quote = Column(Text, nullable=False)


