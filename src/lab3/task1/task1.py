class Movie:
    """Класс, представляющий фильм."""
    def __init__(self, movie_id, movie_name):
        """Инициализирует объект фильма."""
        self.film_id = int(movie_id)  
        self.film_name = movie_name   


class Person:
    """Класс, представляющий пользователя и его историю просмотров."""
    def __init__(self, person_id, person_history):
        """Инициализирует объект пользователя и его историю просмотров."""
        self.person_id = person_id  
        self.person_history = set(map(int, person_history))  


class Recommender:
    """Класс, реализующий систему рекомендаций на основе истории просмотров пользователей."""
    def __init__(self, movies_file, history_file):
        """ Инициализирует систему рекомендаций, загружая данные о фильмах и истории просмотров."""
        self.movies = {}  
        self.users = {}   
        self.loadMovies(movies_file)
        self.loadHistory(history_file)

    def loadMovies(self, file_path):
        """Загружает данные о фильмах из файла."""
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                movie_id, movie_name = line.strip().split(',', 1)
                self.movies[int(movie_id)] = Movie(movie_id, movie_name)

    def loadHistory(self, file_path):
        """Загружает историю просмотров пользователей из файла."""
        with open(file_path, 'r', encoding='utf-8') as f:
            for person_id, line in enumerate(f, 1):  
                person_history = line.strip().split(',')
                self.users[person_id] = Person(person_id, person_history)

    def recommend(self, person_id, target_user_movies):
        """Генерирует рекомендацию для пользователя на основе его истории просмотров."""
        target_user_movies = set(map(int, target_user_movies))  
        similar_users = self.find_similar_users(target_user_movies)
        recommendation = self.get_recommendation(person_id, similar_users, target_user_movies)
        return self.get_good_movie(recommendation)

    def find_similar_users(self, target_user_movies):
        """Находит пользователей с похожими интересами, основываясь на совпадении просмотренных фильмов."""
        similar_users = []
        for user in self.users.values():
            common_movies = target_user_movies.intersection(user.person_history)
            if len(common_movies) >= len(target_user_movies) / 2:
                similar_users.append((user, common_movies))
        return similar_users

    def get_recommendation(self, person_id, similar_users, target_user_movies):
        """Генерирует список фильмов для рекомендации, основываясь на схожести с другими пользователями."""
        movie_scores = {}  
        for user, common_movies in similar_users:
            similarity_score = len(common_movies) / len(target_user_movies)
            if user.person_id != person_id:  
                for movie_id in user.person_history:
                    if movie_id not in target_user_movies:  
                        if movie_id not in movie_scores:
                            movie_scores[movie_id] = 0
                        movie_scores[movie_id] += similarity_score
        return movie_scores

    def get_good_movie(self, movie_scores):
        """Выбирает фильм с наибольшей оценкой из списка предложенных."""
        if not movie_scores:
            return None  
        recommended_movie_id = max(movie_scores, key=movie_scores.get)
        return self.movies[recommended_movie_id].film_name


if __name__ == "__main__":
    recommender = Recommender('textf/Movies.txt', 'textf/History.txt')
    person_id = int(input("Введите ID пользователя, для которого нужно получить рекомендацию: "))  
    target_user_movies_input = input("Введите ID фильмов, которые вы посмотрели (через запятую): ")  
    target_user_movies = list(map(int, target_user_movies_input.split(',')))  
    recommendation = recommender.recommend(person_id, target_user_movies)
    
    if recommendation:
        print(f"Рекомендуемый фильм: {recommendation}")
    else:
        print("Рекомендации не найдены.")
