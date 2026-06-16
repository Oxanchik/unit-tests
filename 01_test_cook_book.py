import pytest

# --- Логика приложения ---

def solve(cook_book: list, person: int):
    """
    Формирует список покупок для заданного количества персон.
    Возвращает список строк.
    """
    result = []
    dish_buy = ''
    for dish_name, ingredients_list in cook_book:
        products = ''
        for ingredient, quantity, measure in ingredients_list:
            quantity_buy = quantity * person
            if len(products) > 0:
                products += ', '
            products += f'{ingredient} {quantity_buy} {measure}'
        dish_buy = f'{dish_name}: {products}'
        result.append(dish_buy)
    return result

# --- Тесты ---

class TestCookBookSolver:
    def setup_method(self, method):
        """Выполняется перед каждым тестом"""
        print(f"\n-> Запуск теста: {method.__name__}")
        # Базовые данные для тестов (можно переопределять в конкретных тестах)
        self.sample_cook_book = [
            ('Омлет', [('Яйцо', 2, 'шт'), ('Молоко', 50, 'мл')]),
            ('Бутерброд', [('Хлеб', 1, 'шт'), ('Сыр', 30, 'г')])
        ]

    def teardown_method(self, method):
        """Выполняется после каждого теста"""
        print(f"-> Завершение теста: {method.__name__}")
        self.sample_cook_book = None

    @pytest.mark.parametrize("cook_book, person, expected", [
        # Стандартный случай: 2 персоны
        (
            [('Омлет', [('Яйцо', 2, 'шт'), ('Молоко', 50, 'мл')])],
            2,
            ['Омлет: Яйцо 4 шт, Молоко 100 мл']
        ),
        # Несколько блюд: 1 персона
        (
            [
                ('Омлет', [('Яйцо', 2, 'шт'), ('Молоко', 50, 'мл')]),
                ('Бутерброд', [('Хлеб', 1, 'шт'), ('Сыр', 30, 'г')])
            ],
            1,
            [
                'Омлет: Яйцо 2 шт, Молоко 50 мл',
                'Бутерброд: Хлеб 1 шт, Сыр 30 г'
            ]
        ),
        # Нулевое количество персон (все количества становятся 0)
        (
            [('Суп', [('Вода', 500, 'мл')])],
            0,
            ['Суп: Вода 0 мл']
        ),
        # Блюдо без ингредиентов (пустой список)
        (
            [('Чай', [])],
            3,
            ['Чай: ']
        ),
        # Дробные количества (если входные данные float)
        (
            [('Коктейль', [('Сок', 0.5, 'л')])],
            4,
            ['Коктейль: Сок 2.0 л']
        )
    ])
    def test_solve_output(self, cook_book, person, expected):
        """Проверка корректности формирования списка покупок"""
        result = solve(cook_book, person)
        assert result == expected

    @pytest.mark.parametrize("cook_book, person, expected_type", [
        # Обычный случай -> список
        ([('Блюдо', [('Ингр', 1, 'шт')])], 1, list),
        # Пустая книга рецептов -> пустой список
        ([], 1, list),
    ])
    def test_solve_return_type(self, cook_book, person, expected_type):
        """Явная проверка типа возвращаемого значения"""
        result = solve(cook_book, person)
        assert isinstance(result, expected_type)

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
