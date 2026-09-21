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

    def open(self, url: str) -> "BasePage":
        with allure.step(f"Открыть страницу: {url}"):
            self.driver.get(url)
        return self


    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator):
        return self.driver.find_elements(*locator)



    def click(self, locator):
        with allure.step(f"Клик по элементу: {locator}"):
            element = self.wait.until(EC.element_to_be_clickable(locator))
            try:
                element.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", element)

    def type_text(self, locator, text: str):
        with allure.step(f"Ввод текста '{text}' в {locator}"):
            element = self.find(locator)
            element.clear()
            element.send_keys(text)



    def get_text(self, locator) -> str:
        return self.find(locator).text

    def get_attribute(self, locator, attribute: str) -> str:
        return self.find(locator).get_attribute(attribute)


    def is_visible(self, locator, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def is_invisible(self, locator, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def is_present(self, locator, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False


    def wait_until(self, condition, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(condition)
            return True
        except TimeoutException:
            return False

    def wait_url_contains(self, substring: str, timeout: int = 10) -> bool:
        return self.wait_until(
            lambda d: substring in d.current_url,
            timeout=timeout
        )

    def wait_url_equals(self, url: str, timeout: int = 10) -> bool:
        return self.wait_until(
            lambda d: d.current_url == url,
            timeout=timeout
        )

    def wait_element_visible(self, locator, timeout: int = 10) -> bool:
        return self.is_visible(locator, timeout=timeout)

    def wait_element_invisible(self, locator, timeout: int = 10) -> bool:
        return self.is_invisible(locator, timeout=timeout)

    def wait_text_in_element(self, locator, text: str, timeout: int = 10) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element(locator, text)
            )
            return True
        except TimeoutException:
            return False



    def take_screenshot(self, name: str = "screenshot"):
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )