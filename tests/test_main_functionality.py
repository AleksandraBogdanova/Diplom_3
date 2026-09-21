import allure
from pages.main_page import MainPage
from pages.orders_feed_page import OrdersFeedPage


@allure.feature("Основной функционал")
class TestMainFunctionality:

    @allure.title("Переход по клику на «Конструктор»")
    def test_go_to_constructor(self, authorized_driver):
        main_page = MainPage(authorized_driver)
        main_page.go_to_constructor()

        assert main_page.is_order_button_visible(), \
            "Не выполнен переход в конструктор"

    @allure.title("Переход по клику на «Лента заказов»")
    def test_go_to_orders_feed(self, driver):
        main_page = MainPage(driver)
        feed = OrdersFeedPage(driver)

        main_page.go_to_orders_feed()

        assert feed.is_loaded(), \
            "Не выполнен переход в ленту заказов"

    @allure.title("Клик по ингредиенту открывает всплывающее окно")
    def test_ingredient_modal_opens(self, driver):
        main_page = MainPage(driver)
        main_page.click_ingredient(index=0)

        assert main_page.is_ingredient_modal_opened(), \
            "Модальное окно ингредиента не открылось"

    @allure.title("Всплывающее окно закрывается кликом по крестику")
    def test_ingredient_modal_closes(self, driver):
        main_page = MainPage(driver)
        main_page.click_ingredient(index=0)
        assert main_page.is_ingredient_modal_opened(), \
            "Модальное окно не открылось"

        main_page.close_ingredient_modal()
        assert main_page.is_ingredient_modal_closed(), \
            "Модальное окно не закрылось"

    @allure.title("При добавлении ингредиента каунтер увеличивается")
    def test_ingredient_counter_increases(self, driver):
        main_page = MainPage(driver)
        before = main_page.get_ingredient_counter(index=0)

        main_page.drag_ingredient_to_basket(index=0)
        after = main_page.get_ingredient_counter(index=0)

        assert after > before, \
            f"Счётчик не увеличился: было {before}, стало {after}"

    @allure.title("Залогиненный пользователь может оформить заказ")
    def test_authorized_user_can_place_order(self, authorized_driver):
        main_page = MainPage(authorized_driver)

        main_page.drag_ingredient_to_basket(index=0)
        main_page.place_order()

        assert main_page.is_ingredient_modal_opened(), \
            "Заказ не оформлен — модальное окно с номером не появилось"