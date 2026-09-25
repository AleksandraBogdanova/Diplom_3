from locators import ForgotPasswordPageLocators
from .base_page import BasePage
import allure


class ForgotPasswordPage(BasePage):

    @allure.step("Ввести email: {email}")
    def enter_email(self, email: str):
        self.type_text(ForgotPasswordPageLocators.EMAIL_INPUT, email)

    @allure.step("Клик по кнопке «Восстановить»")
    def click_restore(self):
        self.click(ForgotPasswordPageLocators.RESTORE_BUTTON)
        self.wait_url_contains("/reset-password", timeout=10)

    @allure.step("Отправить email для восстановления: {email}")
    def submit_email(self, email: str):
        self.enter_email(email)
        self.click_restore()

    @allure.step("Ввести новый пароль")
    def enter_new_password(self, password: str):
        self.type_text(ForgotPasswordPageLocators.PASSWORD_INPUT, password)

    @allure.step("Ввести код из письма")
    def enter_code(self, code: str):
        self.type_text(ForgotPasswordPageLocators.CODE_INPUT, code)

    @allure.step("Клик по кнопке «Сохранить»")
    def click_save(self):
        self.click(ForgotPasswordPageLocators.SAVE_BUTTON)

    @allure.step("Переключить видимость нового пароля")
    def toggle_password_visibility(self):
        self.click(ForgotPasswordPageLocators.PASSWORD_TOGGLE)

    @allure.step("Клик по ссылке «Войти»")
    def click_login_link(self):
        self.click(ForgotPasswordPageLocators.LOGIN_LINK)

    @allure.step("Проверить, что страница восстановления открыта")
    def is_loaded(self) -> bool:
        return self.is_visible(ForgotPasswordPageLocators.RESTORE_BUTTON)

    @allure.step("Проверить, что открылся шаг ввода нового пароля")
    def is_password_step_opened(self, timeout: int = 10) -> bool:
        if not self.wait_url_contains("/reset-password", timeout=timeout):
            return False
        return self.wait_element_visible(
            ForgotPasswordPageLocators.PASSWORD_INPUT, timeout=timeout
        )

    @allure.step("Проверить, что поле пароля активно")
    def is_password_field_active(self) -> bool:
        return self.is_element_active(ForgotPasswordPageLocators.PASSWORD_INPUT)

    @allure.step("Проверить, что URL — /reset-password")
    def is_on_reset_password_url(self) -> bool:
        return "/reset-password" in self.get_current_url()

    @allure.step("Получить name поля пароля")
    def get_password_field_name(self) -> str:
        return self.get_attribute(
            ForgotPasswordPageLocators.PASSWORD_INPUT, "name"
        )

    @allure.step("Получить value поля пароля")
    def get_password_field_value(self) -> str:
        return self.get_attribute(
            ForgotPasswordPageLocators.PASSWORD_INPUT, "value"
        )

    @allure.step("Полный сценарий восстановления пароля")
    def restore_password(self, email: str, new_password: str, code: str):
        self.submit_email(email)
        self.enter_new_password(new_password)
        self.enter_code(code)
        self.click_save()