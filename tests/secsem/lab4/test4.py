import unittest
from sqlalchemy.exc import IntegrityError
from src.secsem.lab4.db import init_db, SessionLocal
from src.secsem.lab4.models import User, Book, Booking
from src.secsem.lab4.crud import (
    add_user,
    add_book,
    create_booking,
    delete_booking,
    get_user_bookings,
    get_book_bookings
)

class TestLibrarySystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()

    
    def setUp(self):
        # Создаем новую сессию для каждого теста
        self.db = SessionLocal()
        # Начинаем транзакцию
        self.trans = self.db.begin_nested()
        
    def tearDown(self):
        # Откатываем транзакцию и закрываем сессию
        self.db.rollback()
        self.db.close()
    
    def test_add_user(self):
        user = add_user(self.db, "Тест Юзер", "test1@example.com")
        self.assertIsNotNone(user.id)
    
    def test_add_book(self):
        book = add_book(self.db, "Тестовая книга", "Автор", 5)
        self.assertEqual(book.copies_available, 5)
    
    def test_create_booking(self):
        user = add_user(self.db, "Юзер", "user1@example.com")
        book = add_book(self.db, "Книга", "Автор", 2)
        booking = create_booking(self.db, user.id, book.id)
        self.assertEqual(book.copies_available, 1)
    
    def test_create_booking_for_unavailable_book(self):
        user = add_user(self.db, "Юзер", "user2@example.com")
        book = add_book(self.db, "Редкая книга", "Автор", 0)
        with self.assertRaises(ValueError):
            create_booking(self.db, user.id, book.id)
    
    def test_delete_booking(self):
        user = add_user(self.db, "Юзер", "user3@example.com")
        book = add_book(self.db, "Книга", "Автор", 1)
        booking = create_booking(self.db, user.id, book.id)
        result = delete_booking(self.db, booking.id)
        self.assertTrue(result)
        self.assertEqual(book.copies_available, 1)
    
    def test_delete_nonexistent_booking(self):
        with self.assertRaises(ValueError):
            delete_booking(self.db, 999)
    
    def test_get_user_bookings(self):
        user = add_user(self.db, "Юзер", "user4@example.com")
        book = add_book(self.db, "Книга", "Автор", 3)
        create_booking(self.db, user.id, book.id)
        bookings = get_user_bookings(self.db, user.id)
        self.assertEqual(len(bookings), 1)
    
    def test_get_book_bookings(self):
        user = add_user(self.db, "Юзер", "user5@example.com")
        book = add_book(self.db, "Книга", "Автор", 2)
        create_booking(self.db, user.id, book.id)
        bookings = get_book_bookings(self.db, book.id)
        self.assertEqual(len(bookings), 1)
    
    def test_user_book_relationships(self):
        user = add_user(self.db, "Юзер", "user6@example.com")
        book = add_book(self.db, "Книга", "Автор", 1)
        booking = create_booking(self.db, user.id, book.id)
        self.assertEqual(len(user.bookings), 1)
        self.assertEqual(len(book.bookings), 1)

if __name__ == '__main__':
    unittest.main()