from locators import OrderHistoryPageLocators
from .base_page import BasePage
import allure


class OrderHistoryPage(BasePage):

    @allure.step("Проверить, что страница истории заказов открыта")
    def is_loaded(self, timeout: int = 10) -> bool:
        return self.wait_url_contains(
            "/account/order-history", timeout=timeout
        )

    @allure.step("Ждать загрузки списка заказов")
    def wait_orders_loaded(self, timeout: int = 15):
        self.wait_element_visible(
            OrderHistoryPageLocators.ORDER_LINKS, timeout=timeout
        )

    @allure.step("Получить номера заказов из истории")
    def get_order_numbers(self) -> list:
        self.wait_orders_loaded()
        numbers = []
        for link in self.find_all(OrderHistoryPageLocators.ORDER_LINKS):
            elements = link.find_elements(
                *OrderHistoryPageLocators.ORDER_NUMBER
            )
            for el in elements:
                text = el.text.strip()
                if text.startswith("#"):
                    digits = text.lstrip("#")
                    if digits.isdigit():
                        numbers.append(digits)
                    break
        return numbers

    @allure.step("Получить количество заказов в истории")
    def get_orders_count(self, timeout: int = 10) -> int:
        self.wait_element_visible(
            OrderHistoryPageLocators.ORDER_ITEMS, timeout=timeout
        )
        return len(self.find_all(OrderHistoryPageLocators.ORDER_ITEMS))

    @allure.step("Проверить, что история заказов пуста")
    def is_empty(self) -> bool:
        return self.get_orders_count() == 0