import time
from selenium.webdriver.common.by import By
from locators import OrdersFeedPageLocators
from .base_page import BasePage
import allure


class OrdersFeedPage(BasePage):

    @allure.step("Ждать загрузки карточек заказов")
    def wait_orders_loaded(self, timeout: int = 10):
        self.wait_element_visible(
            OrdersFeedPageLocators.ORDER_CARD, timeout=timeout
        )

    @allure.step("Клик по карточке заказа с индексом {index}")
    def click_order_card(self, index: int = 0):
        self.wait_orders_loaded()
        cards = self.find_all(OrdersFeedPageLocators.ORDER_CARD)
        if not cards:
            raise AssertionError("В ленте заказов нет ни одной карточки")
        if index >= len(cards):
            raise AssertionError(
                f"Индекс {index} вне диапазона: карточек {len(cards)}"
            )
        cards[index].click()

    @allure.step("Закрыть модальное окно заказа")
    def close_order_modal(self):
        self.click(OrdersFeedPageLocators.ORDER_MODAL_CLOSE)

    @allure.step("Получить счётчик «Выполнено за всё время»")
    def get_total_completed(self, timeout: int = 10) -> int:
        self.wait_element_visible(
            OrdersFeedPageLocators.TITLE, timeout=timeout
        )
        self.wait_element_visible(
            OrdersFeedPageLocators.TOTAL_COMPLETED_COUNTER, timeout=timeout
        )
        text = self.get_text(OrdersFeedPageLocators.TOTAL_COMPLETED_COUNTER)
        return self._parse_counter(text)

    @allure.step("Получить счётчик «Выполнено за сегодня»")
    def get_today_completed(self, timeout: int = 10) -> int:
        self.wait_element_visible(
            OrdersFeedPageLocators.TITLE, timeout=timeout
        )
        self.wait_element_visible(
            OrdersFeedPageLocators.TODAY_COMPLETED_COUNTER, timeout=timeout
        )
        text = self.get_text(OrdersFeedPageLocators.TODAY_COMPLETED_COUNTER)
        return self._parse_counter(text)

    @allure.step("Ждать, что счётчик увеличится")
    def wait_counter_increases(
        self, getter, before: int, timeout: int = 15
    ) -> int:
        deadline = time.time() + timeout
        while time.time() < deadline:
            current = getter()
            if current > before:
                return current
            time.sleep(0.5)
        return getter()

    @allure.step("Ждать появления номера заказа в списках")
    def wait_order_in_list(
        self, order_number: str, timeout: int = 15
    ) -> bool:
        deadline = time.time() + timeout
        while time.time() < deadline:
            in_progress = self.get_in_progress_orders()
            ready = self.get_ready_orders()
            if order_number in in_progress or order_number in ready:
                return True
            time.sleep(0.5)
        return False

    @staticmethod
    def _parse_counter(text: str) -> int:
        cleaned = text.replace(" ", "").replace("\u00a0", "")
        return int(cleaned)

    @allure.step("Получить список готовых заказов")
    def get_ready_orders(self) -> list:
        lists = self.find_all(OrdersFeedPageLocators.ORDER_LISTS)
        if not lists:
            return []
        items = lists[0].find_elements(By.TAG_NAME, "li")
        return [el.text.strip() for el in items]

    @allure.step("Получить список заказов в работе")
    def get_in_progress_orders(self) -> list:
        lists = self.find_all(OrdersFeedPageLocators.ORDER_LISTS)
        if len(lists) < 2:
            return []
        items = lists[1].find_elements(By.TAG_NAME, "li")
        return [el.text.strip() for el in items]

    @allure.step("Проверить, что в ленте есть заказы")
    def has_orders(self, timeout: int = 10) -> bool:
        return self.wait_element_visible(
            OrdersFeedPageLocators.ORDER_CARD, timeout=timeout
        )

    @allure.step("Проверить, что лента заказов открыта")
    def is_loaded(self) -> bool:
        return self.is_visible(OrdersFeedPageLocators.TITLE)

    @allure.step("Проверить, что модалка заказа открыта")
    def is_order_modal_opened(self) -> bool:
        return self.is_visible(OrdersFeedPageLocators.ORDER_MODAL)

    @allure.step("Проверить, что модалка заказа закрыта")
    def is_order_modal_closed(self, timeout: int = 5) -> bool:
        return self.is_invisible(
            OrdersFeedPageLocators.ORDER_MODAL, timeout=timeout
        )