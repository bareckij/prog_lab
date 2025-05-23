from sqlalchemy.orm import Session
from src.secsem.lab4.models import User, Book, Booking
from datetime import date
from src.secsem.lab4.db import SessionLocal

def add_user(db: Session, name: str, email: str):
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def add_book(db: Session, title: str, author: str, copies_available: int):
    book = Book(title=title, author=author, copies_available=copies_available)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

def create_booking(db: Session, user_id: int, book_id: int):
    # Проверяем доступность книги
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book or book.copies_available <= 0:
        raise ValueError("Книга недоступна для бронирования")
    
    # Создаем бронирование
    booking = Booking(user_id=user_id, book_id=book_id, booking_date=date.today())
    db.add(booking)
    
    # Уменьшаем количество доступных экземпляров
    book.copies_available -= 1
    
    db.commit()
    db.refresh(booking)
    return booking

def delete_booking(db: Session, booking_id: int):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise ValueError("Бронирование не найдено")
    
    # Увеличиваем количество доступных экземпляров
    book = db.query(Book).filter(Book.id == booking.book_id).first()
    if book:
        book.copies_available += 1
    
    db.delete(booking)
    db.commit()
    return True

def get_user_bookings(db: Session, user_id: int):
    return db.query(Booking).filter(Booking.user_id == user_id).all()

def get_book_bookings(db: Session, book_id: int):
    return db.query(Booking).filter(Booking.book_id == book_id).all()