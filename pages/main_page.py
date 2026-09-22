from selenium.webdriver.common.by import By
from locators import HeaderLocators, MainPageLocators
from .base_page import BasePage
import allure


class MainPage(BasePage):

    @allure.step("Клик по кнопке «Конструктор»")
    def go_to_constructor(self):
        self.click(HeaderLocators.CONSTRUCTOR_LINK)

    @allure.step("Клик по кнопке «Лента заказов»")
    def go_to_orders_feed(self):
        self.click(HeaderLocators.ORDERS_FEED_LINK)

    @allure.step("Клик по кнопке «Личный кабинет»")
    def go_to_profile(self):
        self.click(HeaderLocators.PROFILE_LINK)

    @allure.step("Открыть таб «Булки»")
    def open_buns_tab(self):
        self.click(MainPageLocators.BUNS_TAB)

    @allure.step("Открыть таб «Соусы»")
    def open_sauces_tab(self):
        self.click(MainPageLocators.SAUCES_TAB)

    @allure.step("Открыть таб «Начинки»")
    def open_fillings_tab(self):
        self.click(MainPageLocators.FILLINGS_TAB)

    @allure.step("Клик по ингредиенту с индексом {index}")
    def click_ingredient(self, index: int = 0):
        self.wait_element_visible(
            MainPageLocators.INGREDIENT_CARD, timeout=10
        )
        self.wait_element_invisible(
            (By.CSS_SELECTOR, "[class*='Modal_modal_overlay']"), timeout=5
        )
        cards = self.find_all(MainPageLocators.INGREDIENT_CARD)
        if not cards:
            raise AssertionError("На странице нет ни одного ингредиента")
        if index >= len(cards):
            raise AssertionError(
                f"Индекс {index} вне диапазона: ингредиентов {len(cards)}"
            )
        cards[index].click()

    @allure.step("Закрыть модальное окно ингредиента")
    def close_ingredient_modal(self):
        self.click(MainPageLocators.INGREDIENT_MODAL_CLOSE)

    @allure.step("Получить счётчик ингредиента {index}")
    def get_ingredient_counter(self, index: int = 0) -> int:
        counters = self.find_all(MainPageLocators.INGREDIENT_COUNTER)
        if not counters:
            return 0
        text = counters[index].text.strip()
        return int(text) if text.isdigit() else 0

    @allure.step("Перетащить ингредиент {index} в корзину")
    def drag_ingredient_to_basket(self, index: int = 0):
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
        self.execute_script(js, cards[index], basket)

    @allure.step("Клик по кнопке «Оформить заказ»")
    def place_order(self):
        self.click(MainPageLocators.ORDER_BUTTON)

    @allure.step("Получить номер оформленного заказа")
    def get_order_number(self, timeout: int = 10) -> str:
        self.wait_until(
            lambda d: self.get_text(MainPageLocators.ORDER_NUMBER).strip()
                      not in ("", "9999"),
            timeout=timeout
        )
        raw = self.get_text(MainPageLocators.ORDER_NUMBER).strip()
        if raw.isdigit():
            raw = raw.zfill(6)
        return raw

    @allure.step("Проверить, что конструктор открыт")
    def is_loaded(self) -> bool:
        return self.is_visible(MainPageLocators.TITLE)

    @allure.step("Проверить, что кнопка «Оформить заказ» видна")
    def is_order_button_visible(self) -> bool:
        return self.is_visible(MainPageLocators.ORDER_BUTTON)

    @allure.step("Ждать появления кнопки «Оформить заказ»")
    def wait_order_button_visible(self, timeout: int = 10) -> bool:
        return self.wait_element_visible(
            MainPageLocators.ORDER_BUTTON, timeout=timeout
        )

    @allure.step("Проверить, что кнопка «Войти в аккаунт» видна")
    def is_login_button_visible(self) -> bool:
        return self.is_visible(MainPageLocators.LOGIN_BUTTON)

    @allure.step("Проверить, что модалка ингредиента открыта")
    def is_ingredient_modal_opened(self) -> bool:
        return self.is_visible(MainPageLocators.INGREDIENT_MODAL)

    @allure.step("Проверить, что модалка ингредиента закрыта")
    def is_ingredient_modal_closed(self, timeout: int = 5) -> bool:
        return self.is_invisible(
            MainPageLocators.INGREDIENT_MODAL, timeout=timeout
        )