import os
import unittest

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Загрузка переменных
load_dotenv()
TEST_LOGIN = os.getenv("TEST_LOGIN", "")
TEST_PASSWORD = os.getenv("TEST_PASSWORD", "")


class TestYandexAuth(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()

        # 1. Указываем путь к исполняемому файлу Brave
        # Для Windows (стандартный путь):
        brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

        if not os.path.exists(brave_path):
            raise FileNotFoundError(f"Brave browser не найден по пути: {brave_path}")

        options.binary_location = brave_path

        # 2. Стандартные настройки для обхода детекции
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # 3. Инициализируем именно Chrome Driver, но с браузером Brave
        self.driver = webdriver.Chrome(options=options)

        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 15)  # Увеличили время до 15 сек
        self.base_url = "https://passport.yandex.ru/auth/"

    def test_login_success(self):
        driver = self.driver
        wait = self.wait

        driver.get(self.base_url)

        try:
            # --- ШАГ 1: ЛОГИН ---
            # Поле логина (autocomplete='username')
            login_field = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "input[data-testid='text-field-input'][autocomplete='username']")
            ))
            login_field.send_keys(TEST_LOGIN)

            # Кнопка "Next" для логина
            next_btn_login = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[data-testid='add-user-next']")
            ))
            next_btn_login.click()

            # --- ШАГ 2: ПАРОЛЬ ---
            # Ждем исчезновения поля логина (гарантия смены экрана)
            wait.until(EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, "input[data-testid='text-field-input'][autocomplete='username']")))

            # Поле пароля (autocomplete='current-password')
            password_field = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "input[data-testid='text-field-input'][autocomplete='current-password']")
            ))
            password_field.send_keys(TEST_PASSWORD)

            # Кнопка "Next" для пароля (используем найденный data-testid)
            next_btn_pass = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[data-testid='password-next']")
            ))
            next_btn_pass.click()

            # --- ПРОВЕРКА ---
            # Ждем редирект со страницы авторизации
            wait.until(lambda d: "passport.yandex.ru/auth" not in d.current_url)

            self.assertNotIn("passport.yandex.ru/auth", driver.current_url,
                             "Авторизация не удалась: редирект не произошел")
            print("✅ Успешная авторизация!")

        except TimeoutException:
            driver.save_screenshot("debug_final.png")
            self.fail("Таймаут. Проверьте скриншот debug_final.png. Возможно, сайт требует ввода капчи или код 2FA.")
        except Exception as e:
            self.fail(f"Произошла ошибка: {e}")
        finally:
            if self.driver:
                self.driver.quit()

if __name__ == "__main__":
    unittest.main()
