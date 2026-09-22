from locators import ProfilePageLocators
from .base_page import BasePage
import allure


class ProfilePage(BasePage):

    @allure.step("Перейти в раздел «История заказов»")
    def go_to_order_history(self):
        self.click(ProfilePageLocators.ORDER_HISTORY_LINK)
        self.wait_url_contains("/account/order-history")

    @allure.step("Перейти в раздел «Профиль»")
    def go_to_profile(self):
        self.click(ProfilePageLocators.PROFILE_LINK)

    @allure.step("Выйти из аккаунта")
    def logout(self):
        self.click(ProfilePageLocators.LOGOUT_BUTTON)

    @allure.step("Проверить, что личный кабинет открыт")
    def is_loaded(self) -> bool:
        return self.is_visible(ProfilePageLocators.LOGOUT_BUTTON)