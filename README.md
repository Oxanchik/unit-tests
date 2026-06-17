# Домашнее задание к лекции 4.«Tests»

## Задача №1 unit-tests
Напишите тесты на любые 3 задания из модуля «Основы языка программирования Python». Используйте своё решение домашнего задания.
При написании тестов не забывайте использовать параметризацию.
Рекомендации по тестам: если у вас в функциях информация выводилась (print), то теперь её лучше возвращать (return), чтобы можно было протестировать.

## Задача №2 Автотест API Яндекса
Проверим правильность работы Яндекс.Диск REST API. Написать тесты, проверяющий создание папки на Диске.
Используя библиотеку requests напишите unit-test на верный ответ и возможные отрицательные тесты на ответы с ошибкой

Пример положительных тестов:
- Код ответа соответствует 201. В отличие от многих других API, Яндекс.Диск возвращает именно 201, а не 200, при создании. 
- Результат создания папки - папка появилась в списке файлов.

## Задача №3. Дополнительная (не обязательная)
Применив selenium, напишите unit-test для авторизации на Яндексе по url: https://passport.yandex.ru/auth/


## Инструкция по запуску проекта

**1. Установите Python**

Убедитесь, что у вас установлен Python 3.8+

```bash
python --version
```
Если Python не установлен: https://www.python.org/downloads/

**2. Клонируйте репозиторий:**
```bash
git clone git@github.com:Oxanchik/unit_tests.git
cd unit_tests
```

**3. Создайте и активируйте виртуальное окружение (по желанию):**

Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**4. Установите зависимости:**
```bash
pip install -r requirements.txt
```

**5. Настройте токен, логин и пароль Яндекс.Диска**
- **Скопируйте файл-пример**

```bash
cp .env.example .env        # macOS/Linux
copy .env.example .env      # Windows
```

- **Получите токен Яндекс Диска на [Полигоне](https://yandex.ru/dev/disk/poligon/)**

- **Вставьте данные в файл `.env`**
Откройте файл .env в любом текстовом редакторе и замените your_token_here на ваш токен, "your_test_login@yandex.ru" на ваш логин, "your_test_password" на ваш пароль:
```bash
YANDEX_TOKEN=y0_AgAAAAABXk3QA...
TEST_LOGIN="your_test_login@yandex.ru"
TEST_PASSWORD="your_test_password"
```
## Пример работы

Пример работы `02_test_ydisk.py`

```
============================= test session starts =============================
collecting ... collected 3 items

02_test_ydisk.py::TestYandexDiskAPI::test_01_create_folder_success 
02_test_ydisk.py::TestYandexDiskAPI::test_02_create_folder_conflict 
02_test_ydisk.py::TestYandexDiskAPI::test_03_create_folder_unauthorized 

============================== 3 passed in 4.91s ==============================
PASSED [ 33%]
[OK] Папка 'TestFolder_1781723024' успешно создана и обнаружена на диске. Код ответа сервера: 201
PASSED [ 66%]
[OK] Корректно получена ошибка 409 при повторном создании папки: DiskPathPointsToExistentDirectoryError
PASSED [100%]
[OK] Корректно получена ошибка 401 при использовании неверного токена.

[Cleanup] Тестовая папка 'TestFolder_1781723024' удалена.
```

Пример работы `03_test_yauth.py`

```
============================= test session starts =============================
collecting ... collected 1 item

03_test_yauth.py::TestYandexAuth::test_login_success 

============================= 1 passed in 22.78s ==============================
PASSED              [100%]✅ Успешная авторизация!
```