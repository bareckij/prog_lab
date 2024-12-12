import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from lab3.task1.task1 import Recommender, Person, Movie  # Импорт классов

class TestMovieRecommendationSystem(unittest.TestCase):
    def setUp(self):
        """Этот метод вызывается перед каждым тестом для подготовки данных"""
        self.movies_data = """1,Movie A
2,Movie B
3,Movie C
4,Movie D
5,Movie E"""
        
        self.history_data = """1,1,2,3
2,2,3,4
3,1,3,5"""
        
        with open('test_movies.txt', 'w', encoding='utf-8') as f:
            f.write(self.movies_data)
        
        with open('test_history.txt', 'w', encoding='utf-8') as f:
            f.write(self.history_data)

        self.recommender = Recommender('test_movies.txt', 'test_history.txt')

    def tearDown(self):
        """Этот метод вызывается после каждого теста для очистки данных"""
        import os
        os.remove('test_movies.txt')
        os.remove('test_history.txt')

    def test_load_movies(self):
        """Тестирует загрузку фильмов"""
        self.assertEqual(len(self.recommender.movies), 5)  # должно быть 5 фильмов
        self.assertEqual(self.recommender.movies[1].film_name, 'Movie A')
        self.assertEqual(self.recommender.movies[5].film_name, 'Movie E')

    def test_load_history(self):
        """Тестирует загрузку истории пользователей"""
        self.assertEqual(len(self.recommender.users), 3)  # должно быть 3 пользователя
        self.assertEqual(self.recommender.users[1].person_history, {1, 2, 3})
        self.assertEqual(self.recommender.users[2].person_history, {2, 3, 4})

    def test_find_similar_users(self):
        """Тестирует поиск схожих пользователей"""
        target_user_movies = {1, 2, 3}
        similar_users = self.recommender.find_similar_users(target_user_movies)
        self.assertEqual(len(similar_users), 3)  # должно быть 3 похожих пользователя
        self.assertEqual(similar_users[0][0].person_id, 1)  # Первый пользователь
        self.assertEqual(similar_users[1][0].person_id, 2)  # Второй пользователь

    def test_get_recommendation(self):
        """Тестирует генерацию рекомендаций"""
        target_user_movies = {1, 2, 3}
        similar_users = self.recommender.find_similar_users(target_user_movies)
        movie_scores = self.recommender.get_recommendation(1, similar_users, target_user_movies)
        self.assertIn(4, movie_scores)  # Movie D должен быть рекомендован (пользователи 2 и 3 его видели)

    def test_get_good_movie(self):
        """Тестирует выбор лучшего фильма по оценке"""
        movie_scores = {4: 0.5, 5: 0.7}  # Movie D и Movie E
        good_movie = self.recommender.get_good_movie(movie_scores)
        self.assertEqual(good_movie, 'Movie E')  # Movie E должен быть выбран

    def test_recommend(self):
        """Тестирует полный процесс рекомендации"""
        person_id = 1
        target_user_movies = [1, 2, 3]
        recommendation = self.recommender.recommend(person_id, target_user_movies)
        self.assertEqual(recommendation, 'Movie D')  # Ожидаем, что будет рекомендован 'Movie D'

    def test_no_recommendations(self):
        """Тестирует случай, когда нет рекомендаций"""
        person_id = 3
        target_user_movies = [5]
        recommendation = self.recommender.recommend(person_id, target_user_movies)
        self.assertIsNone(recommendation)  # Нет рекомендаций, так как нет схожих пользователей


if __name__ == '__main__':
    unittest.main()
