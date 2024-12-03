class Survey:
    def __init__(self, age_groups):
        """Инициализация с границами возрастных групп и списком респондентов."""
        self.age_groups = age_groups
        self.respondents = []

    def add_respondent(self, full_name, age):
        """Добавление респондента в список."""
        self.respondents.append((full_name, age))

    def categorize_respondents(self):
        """Категоризация респондентов по возрастным группам и вывод результата."""
        self.respondents.sort(key=lambda x: (-x[1], x[0]))
        groups = {f'{self.age_groups[i]}-{self.age_groups[i + 1]}': [] for i in range(len(self.age_groups) - 1)}
        groups['101-inf'] = []
        for full_name, age in self.respondents:
            categorized = False
            for i in range(len(self.age_groups) - 1):
                if self.age_groups[i] <= age <= self.age_groups[i + 1]:
                    groups[f'{self.age_groups[i]}-{self.age_groups[i + 1]}'].append((full_name, age))
                    categorized = True
                    break
            if not categorized and age >= 101:
                groups['101-inf'].append((full_name, age))
        sorted_groups = sorted(groups.items(), key=lambda item: self.get_group_order(item[0]), reverse=True)
        for group, members in sorted_groups:
            if members:
                members_str = ', '.join([f"{name} ({age})" for name, age in members])
                print(f'{group}: {members_str}')

    def get_group_order(self, group_name):
        """Получение числового значения для группы, чтобы корректно сортировать по возрасту."""
        if group_name == '101-inf':
            return 101
        age_range = group_name.split('-')
        return int(age_range[1])

def main():
    """Основная функция для обработки ввода и вывода данных."""
    age_groups = [0, 18, 25, 35, 45, 60, 80, 100, 101]
    survey = Survey(age_groups)
    while True:
        data = input()
        if data == "END":
            break
        else:
            try:
                full_name, age = data.split(',')
                age = int(age)
                if (full_name, age) not in survey.respondents:
                    survey.add_respondent(full_name.strip(), age)
            except ValueError:
                print("Некорректный ввод, попробуйте еще раз.")
    survey.categorize_respondents()

if __name__ == "__main__":
    main()
