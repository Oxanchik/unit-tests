import pytest
from collections import Counter


# --- Логика приложения ---

def mentors_names(courses: list, mentors: list, durations: list):
    """Возвращает список строк с информацией о тёзках для каждого курса."""

    result = []

    # Объединяем данные
    for course, mentor_list, duration in zip(courses, mentors, durations):
        # Извлекаем имена (первые слова)
        names = [full_name.split()[0] for full_name in mentor_list]

        # Находим дубликаты через Counter
        counts = Counter(names)
        duplicates = {name for name, count in counts.items() if count > 1}

        if duplicates:
            # Собираем полные имена тех, у кого имя есть в списке дубликатов
            same_name_list = [
                full_name for full_name in mentor_list
                if full_name.split()[0] in duplicates
            ]
            # Сортируем для консистентности вывода
            same_name_list.sort()

            result.append(f"На курсе {course} есть тёзки: {', '.join(same_name_list)}")

    return result


# --- Тесты ---

class TestMentorsNames:
    def setup_method(self, method):
        print(f"\n-> Запуск теста: {method.__name__}")
        self.courses = ["Python", "Java", "C++"]
        self.durations = [6, 9, 12]

    def teardown_method(self, method):
        print(f"-> Завершение теста: {method.__name__}")

    @pytest.mark.parametrize("courses, mentors, durations, expected", [
        # Тёзки есть (стандартный случай)
        (
                ["Python"],
                [["Иван Петров", "Мария Иванова", "Иван Сидоров"]],
                [6],
                ["На курсе Python есть тёзки: Иван Петров, Иван Сидоров"]
        ),
        # Тёзок нет (все имена уникальны)
        (
                ["Java"],
                [["Алексей Смирнов", "Борис Иванов", "Виктор Петров"]],
                [9],
                []
        ),
        # Несколько курсов, тёзки только на одном
        (
                ["Python", "Java"],
                [
                    ["Иван Петров", "Мария Иванова", "Иван Сидоров"],
                    ["Алексей Смирнов", "Борис Иванов"]
                ],
                [6, 9],
                ["На курсе Python есть тёзки: Иван Петров, Иван Сидоров"]
        ),
        # Несколько курсов, тёзки на всех
        (
                ["Python", "Java"],
                [
                    ["Иван Петров", "Иван Сидоров"],
                    ["Анна Каренина", "Анна Павлова"]
                ],
                [6, 9],
                [
                    "На курсе Python есть тёзки: Иван Петров, Иван Сидоров",
                    "На курсе Java есть тёзки: Анна Каренина, Анна Павлова"
                ]
        ),
        # Пустые списки
        (
                [],
                [],
                [],
                []
        ),
        # Курс без преподавателей
        (
                ["Empty"],
                [[]],
                [3],
                []
        ),
        # Тёзки более 2 человек
        (
                ["C++"],
                [["Олег Тиньков", "Олег Веретенников", "Олег Газманов", "Дмитрий Менделеев"]],
                [12],
                ["На курсе C++ есть тёзки: Олег Веретенников, Олег Газманов, Олег Тиньков"]
        )
    ])
    def test_mentors_names_output(self, courses, mentors, durations, expected):
        """Проверка корректности поиска тёзок и форматирования"""
        result = mentors_names(courses, mentors, durations)
        assert result == expected

    @pytest.mark.parametrize("courses, mentors, durations, expected_type", [
        (["Course"], [["Name Surname"]], [1], list),
        ([], [], [], list),
    ])
    def test_mentors_names_return_type(self, courses, mentors, durations, expected_type):
        """Явная проверка типа возвращаемого значения"""
        result = mentors_names(courses, mentors, durations)
        assert isinstance(result, expected_type)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
