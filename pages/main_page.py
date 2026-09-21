from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
)

from locators import HeaderLocators, MainPageLocators
from .base_page import BasePage
import allure


class MainPage(BasePage):

    @allure.step("Клик по кнопке «Конструктор»")
    def go_to_constructor(self) -> "MainPage":
        self.click(HeaderLocators.CONSTRUCTOR_LINK)
        return self

    @allure.step("Клик по кнопке «Лента заказов»")
    def go_to_orders_feed(self) -> "MainPage":
        self.click(HeaderLocators.ORDERS_FEED_LINK)
        return self

    @allure.step("Клик по кнопке «Личный кабинет»")
    def go_to_profile(self) -> "MainPage":
        self.click(HeaderLocators.PROFILE_LINK)
        return self

    @allure.step("Открыть таб «Булки»")
    def open_buns_tab(self) -> "MainPage":
        self.click(MainPageLocators.BUNS_TAB)
        return self

    @allure.step("Открыть таб «Соусы»")
    def open_sauces_tab(self) -> "MainPage":
        self.click(MainPageLocators.SAUCES_TAB)
        return self

    @allure.step("Открыть таб «Начинки»")
    def open_fillings_tab(self) -> "MainPage":
        self.click(MainPageLocators.FILLINGS_TAB)
        return self

    @allure.step("Клик по ингредиенту с индексом {index}")
    def click_ingredient(self, index: int = 0) -> "MainPage":
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    MainPageLocators.INGREDIENT_CARD
                )
            )
        except TimeoutException:
            raise AssertionError("Ингредиенты не загрузились на странице")

        try:
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, "[class*='Modal_modal_overlay']")
                )
            )
        except TimeoutException:
            pass

        cards = self.find_all(MainPageLocators.INGREDIENT_CARD)
        if not cards:
            raise AssertionError("На странице нет ни одного ингредиента")
        if index >= len(cards):
            raise AssertionError(
                f"Индекс {index} вне диапазона: ингредиентов {len(cards)}"
            )

        try:
            cards[index].click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", cards[index])
        return self

    @allure.step("Закрыть модальное окно ингредиента")
    def close_ingredient_modal(self) -> "MainPage":
        self.click(MainPageLocators.INGREDIENT_MODAL_CLOSE)
        return self

    def get_ingredient_counter(self, index: int = 0) -> int:
        counters = self.find_all(MainPageLocators.INGREDIENT_COUNTER)
        if not counters:
            return 0
        text = counters[index].text.strip()
        return int(text) if text.isdigit() else 0

    @allure.step("Перетащить ингредиент {index} в корзину")
    def drag_ingredient_to_basket(self, index: int = 0) -> "MainPage":
        cards = self.find_all(MainPageLocators.INGREDIENT_CARD)
        basket = self.find(MainPageLocators.BASKET)

        js = """
        const source = arguments[0];
        const target = arguments[1];

        function fire(el, type) {
            const e = document.createEvent('CustomEvent');
            e.initCustomEvent(type, true, true, null);
            e.dataTransfer = {
                data: {},
                setData(k, v) { this.data[k] = v; },
                getData(k) { return this.data[k]; }
            };
            el.dispatchEvent(e);
        }

        fire(source, 'dragstart');
        fire(target, 'dragover');
        fire(target, 'drop');
        """
        self.driver.execute_script(js, cards[index], basket)
        return self

    @allure.step("Клик по кнопке «Оформить заказ»")
    def place_order(self) -> "MainPage":
        self.click(MainPageLocators.ORDER_BUTTON)
        return self

    def get_order_number(self, timeout: int = 10) -> str:
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: self.get_text(MainPageLocators.ORDER_NUMBER).strip()
                          not in ("", "9999")
            )
        except TimeoutException:
            pass
        raw = self.get_text(MainPageLocators.ORDER_NUMBER).strip()
        # Номер из модалки — "20896", в ленте — "020896". Приводим к 6 знакам.
        if raw.isdigit():
            raw = raw.zfill(6)
        return raw

    def is_loaded(self) -> bool:
        return self.is_visible(MainPageLocators.TITLE)

    def is_order_button_visible(self) -> bool:
        return self.is_visible(MainPageLocators.ORDER_BUTTON)

    def is_login_button_visible(self) -> bool:
        return self.is_visible(MainPageLocators.LOGIN_BUTTON)

    def is_ingredient_modal_opened(self) -> bool:
        return self.is_visible(MainPageLocators.INGREDIENT_MODAL)

    def is_ingredient_modal_closed(self, timeout: int = 5) -> bool:
        return self.is_invisible(
            MainPageLocators.INGREDIENT_MODAL,
            timeout=timeout
        )