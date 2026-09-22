from locators import LoginPageLocators
from .base_page import BasePage
import allure


class LoginPage(BasePage):

    @allure.step("Ввести email: {email}")
    def enter_email(self, email: str):
        self.type_text(LoginPageLocators.EMAIL_INPUT, email)

    @allure.step("Ввести пароль")
    def enter_password(self, password: str):
        self.type_text(LoginPageLocators.PASSWORD_INPUT, password)

    @allure.step("Клик по кнопке «Войти»")
    def click_login(self):
        self.click(LoginPageLocators.LOGIN_BUTTON)

    @allure.step("Клик по ссылке «Восстановить пароль»")
    def click_forgot_password(self):
        self.click(LoginPageLocators.FORGOT_PASSWORD_LINK)

    @allure.step("Клик по ссылке «Зарегистрироваться»")
    def click_register(self):
        self.click(LoginPageLocators.REGISTER_LINK)

    @allure.step("Переключить видимость пароля")
    def toggle_password_visibility(self):
        self.click(LoginPageLocators.PASSWORD_TOGGLE)

    @allure.step("Авторизоваться: {email}")
    def login(self, email: str, password: str):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    @allure.step("Проверить, что форма входа открыта")
    def is_loaded(self) -> bool:
        return self.is_visible(LoginPageLocators.LOGIN_BUTTON)

    @allure.step("Проверить, что поле пароля активно")
    def is_password_field_active(self, timeout: int = 5) -> bool:
        return self.wait_until(
            lambda d: self.find(LoginPageLocators.PASSWORD_INPUT)
                      == d.switch_to.active_element,
            timeout=timeout
        )

    @allure.step("Получить name поля пароля")
    def get_password_field_name(self) -> str:
        return self.get_attribute(LoginPageLocators.PASSWORD_INPUT, "name")

    @allure.step("Получить type поля пароля")
    def get_password_field_type(self) -> str:
        return self.get_attribute(LoginPageLocators.PASSWORD_INPUT, "type")

    @allure.step("Получить value поля пароля")
    def get_password_field_value(self) -> str:
        return self.get_attribute(LoginPageLocators.PASSWORD_INPUT, "value")