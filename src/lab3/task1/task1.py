class Movie:
    def __init__(self, movie_id, movie_name):
        self.film_id = int(movie_id)  # id фильма
        self.film_name = movie_name   # название фильма


class Person:
    def __init__(self, person_id, person_history):
        self.person_id = person_id  # id пользователя
        self.person_history = set(map(int, person_history))  # просмотренные фильмы (в виде множества)


class Recommender:
    def __init__(self, movies_file, history_file):
        self.movies = {}  # Словарь для хранения фильмов
        self.users = {}   # Словарь для хранения пользователей
        self.loadMovies(movies_file)
        self.loadHistory(history_file)

    def loadMovies(self, file_path):
        # Загрузка данных о фильмах
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                movie_id, movie_name = line.strip().split(',', 1)
                self.movies[int(movie_id)] = Movie(movie_id, movie_name)

    def loadHistory(self, file_path):
        # Загрузка истории пользователей
        with open(file_path, 'r', encoding='utf-8') as f:
            for person_id, line in enumerate(f, 1):  # Нумерация с 1
                person_history = line.strip().split(',')
                self.users[person_id] = Person(person_id, person_history)

    def recommend(self, person_id, target_user_movies):
        target_user_movies = set(map(int, target_user_movies))  # преобразуем фильмы пользователя в множество
        similar_users = self.find_similar_users(target_user_movies)
        recommendation = self.get_recommendation(person_id, similar_users, target_user_movies)
        return self.get_good_movie(recommendation)

    def find_similar_users(self, target_user_movies):
        # Поиск схожих пользователей
        similar_users = []
        for user in self.users.values():
            common_movies = target_user_movies.intersection(user.person_history)
            if len(common_movies) >= len(target_user_movies) / 2:
                similar_users.append((user, common_movies))
        return similar_users

    def get_recommendation(self, person_id, similar_users, target_user_movies):
        # Генерация рекомендаций на основе схожих пользователей
        movie_scores = {}  # Словарь для подсчета "схожести" фильмов
        for user, common_movies in similar_users:
            similarity_score = len(common_movies) / len(target_user_movies)
            if user.person_id != person_id:  # Не учитывать самого себя
                for movie_id in user.person_history:
                    if movie_id not in target_user_movies:  # Исключаем просмотренные фильмы
                        if movie_id not in movie_scores:
                            movie_scores[movie_id] = 0
                        movie_scores[movie_id] += similarity_score
        return movie_scores

    def get_good_movie(self, movie_scores):
        # Выбор фильма с наибольшим "оценочным" баллом
        if not movie_scores:
            return None  # Нет рекомендаций
        recommended_movie_id = max(movie_scores, key=movie_scores.get)
        return self.movies[recommended_movie_id].film_name


# Пример использования:
if __name__ == "__main__":
    recommender = Recommender('textf/Movies.txt', 'textf/History.txt')
    person_id = int(input("Введите ID пользователя, для которого нужно получить рекомендацию: "))  # ID пользователя
    target_user_movies_input = input("Введите ID фильмов, которые вы посмотрели (через запятую): ")  # Ввод ID фильмов
    target_user_movies = list(map(int, target_user_movies_input.split(',')))  # Разделение и преобразование в список чисел
    recommendation = recommender.recommend(person_id, target_user_movies)
    
    if recommendation:
        print(f"Рекомендуемый фильм: {recommendation}")
    else:
        print("Рекомендации не найдены.")
