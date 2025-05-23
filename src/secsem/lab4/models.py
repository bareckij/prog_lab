from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import date

# Базовый класс для моделей
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    
    # Связь один-ко-многим с бронированиями
    bookings = relationship("Booking", back_populates="user")

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    copies_available = Column(Integer)
    
    # Связь один-ко-многим с бронированиями
    bookings = relationship("Booking", back_populates="book")

class Booking(Base):
    __tablename__ = 'bookings'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    booking_date = Column(Date, default=date.today())
    
    # Связи многие-к-одному
    user = relationship("User", back_populates="bookings")
    book = relationship("Book", back_populates="bookings")