import allure
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage
from pages.order_history_page import OrderHistoryPage


@allure.feature("Личный кабинет")
class TestPersonalAccount:

    @allure.title("Переход по клику на «Личный кабинет»")
    def test_go_to_profile_from_main(self, authorized_driver):
        main = MainPage(authorized_driver)
        profile = ProfilePage(authorized_driver)

        main.go_to_profile()

        assert profile.is_loaded(), \
            "Личный кабинет не открылся"

    @allure.title("Переход в раздел «История заказов»")
    def test_go_to_order_history(self, authorized_driver):
        main = MainPage(authorized_driver)
        profile = ProfilePage(authorized_driver)
        history = OrderHistoryPage(authorized_driver)

        main.go_to_profile()
        profile.go_to_order_history()

        assert history.is_loaded(), \
            "Не выполнен переход в раздел «История заказов»"

    @allure.title("Выход из аккаунта")
    def test_logout(self, authorized_driver):
        main = MainPage(authorized_driver)
        profile = ProfilePage(authorized_driver)
        login = LoginPage(authorized_driver)

        main.go_to_profile()
        profile.logout()

        assert login.is_loaded(), \
            "После выхода форма входа не отображается"