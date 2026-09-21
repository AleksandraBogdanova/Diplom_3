from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from locators import OrderHistoryPageLocators
from .base_page import BasePage


class OrderHistoryPage(BasePage):

    def is_loaded(self, timeout: int = 10) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_contains("/account/order-history")
            )
            return True
        except TimeoutException:
            return False

    def wait_orders_loaded(self, timeout: int = 15) -> None:
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(
                OrderHistoryPageLocators.ORDER_LINKS
            )
        )

    def get_order_numbers(self) -> list:
        self.wait_orders_loaded()
        links = self.find_all(OrderHistoryPageLocators.ORDER_LINKS)
        numbers = []
        for link in links:
            text = (link.get_attribute("textContent") or "").strip()
            for line in text.split("\n"):
                line = line.strip()
                if line.startswith("#"):
                    digits = ""
                    for ch in line[1:]:
                        if ch.isdigit():
                            digits += ch
                        else:
                            break
                    if digits:
                        numbers.append(digits)
                    break
        return numbers

    def get_orders_count(self) -> int:
        return len(self.find_all(OrderHistoryPageLocators.ORDER_ITEMS))

    def is_empty(self) -> bool:
        return self.get_orders_count() == 0