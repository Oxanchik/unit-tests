import pytest


# --- Логика приложения ---

def discriminant(a, b, c):
    """Функция для нахождения дискриминанта"""
    return b ** 2 - 4 * a * c


def solution(a, b, c):
    """Функция для нахождения корней уравнения"""
    d = discriminant(a, b, c)

    if d == 0:
        return -b / (2 * a)
    elif d > 0:
        root1 = (-b + d ** 0.5) / (2 * a)
        root2 = (-b - d ** 0.5) / (2 * a)
        return (root1, root2)
    else:
        return None


# --- Тесты ---

class TestQuadraticEquation:
    def setup_method(self):
        """Выполняется перед каждым тестом"""
        print("\n-> Запуск теста (setup)")

    def teardown_method(self):
        """Выполняется после каждого теста"""
        print("-> Завершение теста (teardown)")

    @pytest.mark.parametrize("a, b, c, expected", [
        (1, 5, 6, 1),  # D = 1
        (1, 2, 1, 0),  # D = 0
        (1, 0, 1, -4),  # D = -4
        (2, 4, 2, 0),  # D = 0 (a != 1)
        (1, -3, 2, 1),  # Отрицательный b
    ])
    def test_discriminant_values(self, a, b, c, expected):
        """Проверка вычисления дискриминанта"""
        assert discriminant(a, b, c) == expected

    @pytest.mark.parametrize("a, b, c, expected", [
        # Два корня: ожидаем кортеж (root1, root2)
        (1, -3, 2, (2.0, 1.0)),
        (1, 0, -1, (1.0, -1.0)),

        # Один корень: ожидаем float
        (1, 2, 1, -1.0),
        (2, 4, 2, -1.0),

        # Нет корней: ожидаем None
        (1, 0, 1, None),
        (1, 2, 5, None),
    ])
    def test_solution_roots(self, a, b, c, expected):
        """Проверка нахождения корней"""
        result = solution(a, b, c)

        if expected is None:
            assert result is None
        elif isinstance(expected, tuple):
            # Проверка двух корней с допустимой погрешностью
            assert result[0] == pytest.approx(expected[0], rel=1e-5)
            assert result[1] == pytest.approx(expected[1], rel=1e-5)
        else:
            # Проверка одного корня
            assert result == pytest.approx(expected, rel=1e-5)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
