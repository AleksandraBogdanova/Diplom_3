from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from locators import ForgotPasswordPageLocators
from .base_page import BasePage
import allure


class ForgotPasswordPage(BasePage):
    @allure.step("Ввести email: {email}")
    def enter_email(self, email: str) -> "ForgotPasswordPage":
        self.type_text(ForgotPasswordPageLocators.EMAIL_INPUT, email)
        return self

    @allure.step("Клик по кнопке «Восстановить»")
    def click_restore(self) -> "ForgotPasswordPage":
        self.click(ForgotPasswordPageLocators.RESTORE_BUTTON)
        try:
            WebDriverWait(self.driver, 10).until(
                lambda d: "/reset-password" in d.current_url
            )
        except TimeoutException:
            pass
        return self

    @allure.step("Отправить email для восстановления: {email}")
    def submit_email(self, email: str) -> "ForgotPasswordPage":
        self.enter_email(email)
        self.click_restore()
        return self


    @allure.step("Ввести новый пароль")
    def enter_new_password(self, password: str) -> "ForgotPasswordPage":
        self.type_text(ForgotPasswordPageLocators.PASSWORD_INPUT, password)
        return self

    @allure.step("Ввести код из письма")
    def enter_code(self, code: str) -> "ForgotPasswordPage":
        self.type_text(ForgotPasswordPageLocators.CODE_INPUT, code)
        return self

    @allure.step("Клик по кнопке «Сохранить»")
    def click_save(self) -> "ForgotPasswordPage":
        self.click(ForgotPasswordPageLocators.SAVE_BUTTON)
        return self

    @allure.step("Переключить видимость нового пароля")
    def toggle_password_visibility(self) -> "ForgotPasswordPage":
        self.click(ForgotPasswordPageLocators.PASSWORD_TOGGLE)
        return self

    @allure.step("Клик по ссылке «Войти»")
    def click_login_link(self) -> "ForgotPasswordPage":
        self.click(ForgotPasswordPageLocators.LOGIN_LINK)
        return self


    def is_loaded(self) -> bool:
        return self.is_visible(ForgotPasswordPageLocators.RESTORE_BUTTON)

    def is_password_step_opened(self, timeout: int = 10) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: "/reset-password" in d.current_url
            )
        except TimeoutException:
            return False

        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(
                    ForgotPasswordPageLocators.PASSWORD_INPUT
                )
            )
            return True
        except TimeoutException:
            return False

    def is_password_field_active(self) -> bool:
        password_input = self.find(ForgotPasswordPageLocators.PASSWORD_INPUT)
        return password_input == self.driver.switch_to.active_element

    def is_on_reset_password_url(self) -> bool:
        return "/reset-password" in self.driver.current_url

    def get_password_field_name(self) -> str:
        return self.get_attribute(
            ForgotPasswordPageLocators.PASSWORD_INPUT, "name"
        )

    def get_password_field_value(self) -> str:
        return self.get_attribute(
            ForgotPasswordPageLocators.PASSWORD_INPUT, "value"
        )


    @allure.step("Полный сценарий восстановления пароля")
    def restore_password(
        self,
        email: str,
        new_password: str,
        code: str
    ) -> "ForgotPasswordPage":
        self.submit_email(email)
        self.enter_new_password(new_password)
        self.enter_code(code)
        self.click_save()
        return self