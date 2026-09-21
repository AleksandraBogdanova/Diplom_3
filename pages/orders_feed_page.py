import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from locators import OrdersFeedPageLocators
from .base_page import BasePage
import allure


class OrdersFeedPage(BasePage):

    def wait_orders_loaded(self, timeout: int = 10) -> None:
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(
                OrdersFeedPageLocators.ORDER_CARD
            )
        )

    @allure.step("Клик по карточке заказа с индексом {index}")
    def click_order_card(self, index: int = 0) -> "OrdersFeedPage":
        self.wait_orders_loaded()
        cards = self.find_all(OrdersFeedPageLocators.ORDER_CARD)
        if not cards:
            raise AssertionError("В ленте заказов нет ни одной карточки")
        if index >= len(cards):
            raise AssertionError(
                f"Индекс {index} вне диапазона: карточек {len(cards)}"
            )
        cards[index].click()
        return self

    @allure.step("Закрыть модальное окно заказа")
    def close_order_modal(self) -> "OrdersFeedPage":
        self.click(OrdersFeedPageLocators.ORDER_MODAL_CLOSE)
        return self

    def get_total_completed(self, timeout: int = 10) -> int:
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(OrdersFeedPageLocators.TITLE)
        )
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(
                OrdersFeedPageLocators.TOTAL_COMPLETED_COUNTER
            )
        )
        text = self.get_text(OrdersFeedPageLocators.TOTAL_COMPLETED_COUNTER)
        return self._parse_counter(text)

    def get_today_completed(self, timeout: int = 10) -> int:
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(OrdersFeedPageLocators.TITLE)
        )
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(
                OrdersFeedPageLocators.TODAY_COMPLETED_COUNTER
            )
        )
        text = self.get_text(OrdersFeedPageLocators.TODAY_COMPLETED_COUNTER)
        return self._parse_counter(text)

    def wait_counter_increases(self, getter, before: int, timeout: int = 15) -> int:
        deadline = time.time() + timeout
        while time.time() < deadline:
            current = getter()
            if current > before:
                return current
            time.sleep(0.5)
        return getter()

    def wait_order_in_list(self, order_number: str, timeout: int = 15) -> bool:
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

    def get_ready_orders(self) -> list:
        lists = self.find_all(OrdersFeedPageLocators.ORDER_LISTS)
        if not lists:
            return []
        items = lists[0].find_elements(By.TAG_NAME, "li")
        return [el.text.strip() for el in items]

    def get_in_progress_orders(self) -> list:
        lists = self.find_all(OrdersFeedPageLocators.ORDER_LISTS)
        if len(lists) < 2:
            return []
        items = lists[1].find_elements(By.TAG_NAME, "li")
        return [el.text.strip() for el in items]

    def has_orders(self, timeout: int = 10) -> bool:
        try:
            self.wait_orders_loaded(timeout=timeout)
            return True
        except TimeoutException:
            return False

    def is_loaded(self) -> bool:
        return self.is_visible(OrdersFeedPageLocators.TITLE)

    def is_order_modal_opened(self) -> bool:
        return self.is_visible(OrdersFeedPageLocators.ORDER_MODAL)

    def is_order_modal_closed(self, timeout: int = 5) -> bool:
        return self.is_invisible(
            OrdersFeedPageLocators.ORDER_MODAL, timeout=timeout
        )