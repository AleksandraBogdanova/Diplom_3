from locators import OrderHistoryPageLocators
from .base_page import BasePage
import allure


class OrderHistoryPage(BasePage):

    @allure.step("Проверить, что страница истории заказов открыта")
    def is_loaded(self, timeout: int = 10) -> bool:
        return self.wait_url_contains("/account/order-history", timeout=timeout)

    @allure.step("Ждать загрузки списка заказов")
    def wait_orders_loaded(self, timeout: int = 15):
        self.wait_element_visible(
            OrderHistoryPageLocators.ORDER_LINKS, timeout=timeout
        )

    @allure.step("Получить номера заказов из истории")
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

    @allure.step("Получить количество заказов в истории")
    def get_orders_count(self) -> int:
        return len(self.find_all(OrderHistoryPageLocators.ORDER_ITEMS))

    @allure.step("Проверить, что история заказов пуста")
    def is_empty(self) -> bool:
        return self.get_orders_count() == 0