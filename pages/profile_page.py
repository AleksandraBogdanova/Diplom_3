from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import ProfilePageLocators
from .base_page import BasePage
import allure


class ProfilePage(BasePage):

    @allure.step("Перейти в раздел «История заказов»")
    def go_to_order_history(self) -> "ProfilePage":
        self.click(ProfilePageLocators.ORDER_HISTORY_LINK)
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/account/order-history")
        )
        return self

    @allure.step("Перейти в раздел «Профиль»")
    def go_to_profile(self) -> "ProfilePage":
        self.click(ProfilePageLocators.PROFILE_LINK)
        return self

    @allure.step("Выйти из аккаунта")
    def logout(self) -> "ProfilePage":
        self.click(ProfilePageLocators.LOGOUT_BUTTON)
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(ProfilePageLocators.LOGOUT_BUTTON)