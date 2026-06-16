import unittest
import requests
from dotenv import load_dotenv

import os
import time

# Загружаем переменные из .env
load_dotenv()

# КОНФИГУРАЦИЯ
YANDEX_TOKEN = os.getenv("YANDEX_TOKEN")
BASE_URL = 'https://cloud-api.yandex.net/v1/disk/resources'


class TestYandexDiskAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Настройка перед запуском всех тестов"""
        cls.headers = {
            'Authorization': f'OAuth {YANDEX_TOKEN}',
            'Content-Type': 'application/json'
        }
        # Генерируем уникальное имя папки для теста, чтобы избежать конфликтов с предыдущими запусками
        cls.test_folder_name = f"TestFolder_{int(time.time())}"
        cls.test_folder_path = f"disk:/{cls.test_folder_name}"

        # # Словарь для хранения результатов запросов, чтобы проверять их в разных тестах
        # cls.responses = {}

    def test_01_create_folder_success(self):
        """
        Положительный тест: Создание новой папки.
        Ожидается: Код ответа 201 (Created).
        """
        params = {'path': self.test_folder_path}

        response = requests.put(BASE_URL, headers=self.headers, params=params)

        # Выводим отладочную информацию при ошибке
        if response.status_code != 201:
            print(f"\n[DEBUG] Ответ сервера: {response.status_code}")
            print(f"[DEBUG] Тело ответа: {response.text}")
            print(f"[DEBUG] Заголовок Authorization: {self.headers['Authorization'][:15]}...")  # Первые 15 символов

        # Проверка кода ответа
        self.assertEqual(response.status_code, 201,
                         f"Ожидался код 201, но получен {response.status_code}. Текст: {response.text}")

        created_response = response.status_code

        # Дополнительная проверка: убедимся, что папка действительно создана через GET запрос
        get_response = requests.get(BASE_URL, headers=self.headers, params={'path': 'disk:/'})
        self.assertEqual(get_response.status_code, 200)

        # Проверяем наличие папки в списке ресурсов
        data = get_response.json()
        items = data.get('_embedded', {}).get('items', [])
        folder_names = [item['name'] for item in items if item['type'] == 'dir']

        self.assertIn(self.test_folder_name, folder_names,
                      "Папка не найдена в списке файлов на диске после создания.")
        print(f"\n[OK] Папка '{self.test_folder_name}' успешно создана и обнаружена на диске. Код ответа сервера: {created_response}")

    def test_02_create_folder_conflict(self):
        """
        Отрицательный тест: Попытка создать папку, которая уже существует.
        Ожидается: Код ответа 409 (Conflict).
        """
        # Используем путь той же папки, что была создана в предыдущем тесте
        params = {'path': self.test_folder_path}

        response = requests.put(BASE_URL, headers=self.headers, params=params)

        # API Яндекс.Диска возвращает 409, если ресурс уже существует
        self.assertEqual(response.status_code, 409,
                         f"Ожидался код ошибки 409 (Conflict), но получен {response.status_code}.")

        # Проверяем наличие сообщения об ошибке в теле ответа
        error_data = response.json()
        self.assertIn('error', error_data, "В ответе отсутствует поле 'error'")
        print(f"\n[OK] Корректно получена ошибка 409 при повторном создании папки: {error_data.get('error')}")

    def test_03_create_folder_unauthorized(self):
        """
        Отрицательный тест: Попытка создания папки с невалидным токеном.
        Ожидается: Код ответа 401 (Unauthorized).
        """
        bad_headers = {
            'Authorization': 'OAuth invalid_token_12345',
            'Content-Type': 'application/json'
        }
        unique_path = f"disk:/TestFolder_Unauthorized_{int(time.time())}"
        params = {'path': unique_path}

        response = requests.put(BASE_URL, headers=bad_headers, params=params)

        self.assertEqual(response.status_code, 401,
                         f"Ожидался код ошибки 401 (Unauthorized), но получен {response.status_code}.")
        print(f"\n[OK] Корректно получена ошибка 401 при использовании неверного токена.")

    @classmethod
    def tearDownClass(cls):
        """Очистка: удаление тестовой папки после завершения тестов"""
        # Пытаемся удалить папку, созданную в первом тесте
        if hasattr(cls, 'test_folder_path'):
            delete_url = f"{BASE_URL}?path={cls.test_folder_path}"
            # Для удаления используется метод DELETE
            response = requests.delete(delete_url, headers=cls.headers)
            if response.status_code in [204, 200]:
                print(f"\n[Cleanup] Тестовая папка '{cls.test_folder_name}' удалена.")
            else:
                print(f"\n[Warning] Не удалось удалить тестовую папку. Код: {response.status_code}")


if __name__ == '__main__':
    # Запуск тестов с подробным выводом
    unittest.main(verbosity=2)
