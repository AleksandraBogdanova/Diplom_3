from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
)
import allure


class BasePage:
    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    @allure.step("Открыть страницу: {url}")
    def open(self, url: str):
        self.driver.get(url)

    @allure.step("Получить текущий URL")
    def get_current_url(self) -> str:
        return self.driver.current_url

    @allure.step("Ждать, что URL содержит: {substring}")
    def wait_url_contains(self, substring: str, timeout: int = 10) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_contains(substring)
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Найти элемент: {locator}")
    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    @allure.step("Найти все элементы: {locator}")
    def find_all(self, locator):
        return self.driver.find_elements(*locator)

    @allure.step("Клик по элементу: {locator}")
    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Ввести текст '{text}' в {locator}")
    def type_text(self, locator, text: str):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    @allure.step("Выполнить JavaScript")
    def execute_script(self, script, *args):
        return self.driver.execute_script(script, *args)

    @allure.step("Получить текст элемента: {locator}")
    def get_text(self, locator) -> str:
        return self.find(locator).text

    @allure.step("Получить атрибут '{attribute}' элемента: {locator}")
    def get_attribute(self, locator, attribute: str) -> str:
        return self.find(locator).get_attribute(attribute)

    @allure.step("Проверить, что элемент виден: {locator}")
    def is_visible(self, locator, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Проверить, что элемент невидим: {locator}")
    def is_invisible(self, locator, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Проверить, что элемент есть в DOM: {locator}")
    def is_present(self, locator, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Ждать появления элемента: {locator}")
    def wait_element_visible(self, locator, timeout: int = 10) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Ждать исчезновения элемента: {locator}")
    def wait_element_invisible(self, locator, timeout: int = 10) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Проверить, что элемент в фокусе: {locator}")
    def is_element_active(self, locator) -> bool:
        element = self.find(locator)
        return element == self.driver.switch_to.active_element

    @allure.step("Ждать выполнения условия")
    def wait_until(self, condition, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(condition)
            return True
        except TimeoutException:
            return False

    @allure.step("Сделать скриншот: {name}")
    def take_screenshot(self, name: str = "screenshot"):
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )