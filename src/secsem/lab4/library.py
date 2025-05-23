from db import init_db, SessionLocal
from crud import (
    add_user, 
    add_book, 
    create_booking, 
    delete_booking,
    get_user_bookings,
    get_book_bookings
)
from models import *
def reset_db(db):
    db.query(Booking).delete()
    db.query(Book).delete()
    db.query(User).delete()
    db.commit()


def main():

    # Инициализация базы данных
    init_db()
    
    # Создание сессии
    db = SessionLocal()
    reset_db(db)

    try:
        # Добавляем пользователей
        user1 = add_user(db, name="Иван Иванов", email="ivan@example.com")
        user2 = add_user(db, name="Петр Петров", email="petr@example.com")
        
        # Добавляем книги
        book1 = add_book(db, title="Python для начинающих", author="А. Б. Смит", copies_available=3)
        book2 = add_book(db, title="Продвинутый SQL", author="М. Н. Ковалев", copies_available=1)
        
        
        # Создаем бронирования
        booking1 = create_booking(db, user_id=user1.id, book_id=book1.id)
        booking2 = create_booking(db, user_id=user1.id, book_id=book2.id)
        booking3 = create_booking(db, user_id=user2.id, book_id=book1.id)
        
        print(f"Книга '{book1.title}' теперь имеет {book1.copies_available} доступных экземпляров")
        
        # Получаем бронирования пользователя
        print("\nБронирования Ивана:")
        for booking in get_user_bookings(db, user_id=user1.id):
            print(f"- {booking.book.title} (дата: {booking.booking_date})")
        
        # Удаляем бронирование
        delete_booking(db, booking_id=booking2.id)
        print(f"\nПосле удаления бронирования книга '{book2.title}' имеет {book2.copies_available} доступных экземпляров")
        
    finally:
        db.close()

if __name__ == "__main__":
    main()