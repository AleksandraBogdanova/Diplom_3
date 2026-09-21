from locators import LoginPageLocators
from .base_page import BasePage
import allure


class LoginPage(BasePage):

    @allure.step("Ввести email: {email}")
    def enter_email(self, email: str) -> "LoginPage":
        self.type_text(LoginPageLocators.EMAIL_INPUT, email)
        return self

    @allure.step("Ввести пароль")
    def enter_password(self, password: str) -> "LoginPage":
        self.type_text(LoginPageLocators.PASSWORD_INPUT, password)
        return self

    @allure.step("Клик по кнопке «Войти»")
    def click_login(self) -> "LoginPage":
        self.click(LoginPageLocators.LOGIN_BUTTON)
        return self

    @allure.step("Клик по ссылке «Восстановить пароль»")
    def click_forgot_password(self) -> "LoginPage":
        self.click(LoginPageLocators.FORGOT_PASSWORD_LINK)
        return self

    @allure.step("Клик по ссылке «Зарегистрироваться»")
    def click_register(self) -> "LoginPage":
        self.click(LoginPageLocators.REGISTER_LINK)
        return self

    @allure.step("Переключить видимость пароля")
    def toggle_password_visibility(self) -> "LoginPage":
        self.click(LoginPageLocators.PASSWORD_TOGGLE)
        return self


    def is_loaded(self) -> bool:
        return self.is_visible(LoginPageLocators.LOGIN_BUTTON)

    def is_password_field_active(self, timeout: int = 5) -> bool:
        password_input = self.find(LoginPageLocators.PASSWORD_INPUT)
        return self.wait_until(
            lambda d: password_input == d.switch_to.active_element,
            timeout=timeout
        )

    def get_password_field_name(self) -> str:
        return self.get_attribute(LoginPageLocators.PASSWORD_INPUT, "name")

    def get_password_field_type(self) -> str:
        return self.get_attribute(LoginPageLocators.PASSWORD_INPUT, "type")

    def get_password_field_value(self) -> str:
        return self.get_attribute(LoginPageLocators.PASSWORD_INPUT, "value")


    @allure.step("Авторизоваться: {email}")
    def login(self, email: str, password: str) -> "LoginPage":
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
        return self