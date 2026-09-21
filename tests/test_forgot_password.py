import allure
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.forgot_password_page import ForgotPasswordPage
from tests.conftest import TEST_EMAIL

@allure.feature("Восстановление пароля")
class TestForgotPassword:

    @allure.title("Переход на страницу восстановления пароля "
                  "по кнопке «Восстановить пароль»")
    def test_go_to_forgot_password_page(self, driver):
        main_page = MainPage(driver)
        login_page = LoginPage(driver)
        forgot_page = ForgotPasswordPage(driver)

        main_page.go_to_profile()
        login_page.click_forgot_password()

        assert forgot_page.is_loaded(), \
            "Страница восстановления пароля не открылась"

    @allure.title("Ввод почты и клик по кнопке «Восстановить»")
    def test_enter_email_and_restore(self, driver):
        main_page = MainPage(driver)
        login_page = LoginPage(driver)
        forgot_page = ForgotPasswordPage(driver)

        main_page.go_to_profile()
        login_page.click_forgot_password()
        forgot_page.submit_email(TEST_EMAIL)

        assert forgot_page.is_password_step_opened(), \
            "Не выполнен переход на страницу сброса пароля"

    @allure.title("Клик по кнопке показать/скрыть пароль "
                  "делает поле активным — подсвечивает его")
    def test_password_toggle_makes_field_active(self, driver):
        main_page = MainPage(driver)
        login_page = LoginPage(driver)

        main_page.go_to_profile()
        login_page.enter_password("Qwerty123!")
        login_page.toggle_password_visibility()

        assert login_page.is_password_field_active(), \
            "Поле пароля не стало активным после клика по глазу"