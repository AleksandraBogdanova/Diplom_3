import allure
from pages.main_page import MainPage
from pages.profile_page import ProfilePage
from pages.order_history_page import OrderHistoryPage
from pages.orders_feed_page import OrdersFeedPage


@allure.feature("Лента заказов")
class TestOrdersFeed:

    @allure.title("Клик по заказу открывает всплывающее окно с деталями")
    def test_click_order_opens_modal(self, driver):
        main = MainPage(driver)
        feed = OrdersFeedPage(driver)

        main.go_to_orders_feed()
        assert feed.is_loaded(), "Лента заказов не открылась"
        assert feed.has_orders(), "В ленте заказов нет ни одного заказа"

        feed.click_order_card(index=0)

        assert feed.is_order_modal_opened(), \
            "Всплывающее окно с деталями заказа не открылось"

    @allure.title("Заказы из «Истории заказов» отображаются в «Ленте заказов»")
    def test_user_orders_appear_in_feed(self, authorized_driver):
        main = MainPage(authorized_driver)
        profile = ProfilePage(authorized_driver)
        history = OrderHistoryPage(authorized_driver)
        feed = OrdersFeedPage(authorized_driver)

        main.drag_ingredient_to_basket(index=0)
        main.place_order()
        main.close_ingredient_modal()

        main.go_to_profile()
        profile.go_to_order_history()
        assert history.is_loaded(), "История заказов не открылась"

        user_orders = history.get_order_numbers()
        assert user_orders, "История заказов пуста"

        fresh_order = user_orders[-1]

        main.go_to_orders_feed()
        assert feed.is_loaded(), "Лента заказов не открылась"
        assert feed.has_orders(), "В ленте нет ни одного заказа"

        found = feed.wait_order_in_list(fresh_order, timeout=15)
        assert found, \
            f"Заказ {fresh_order} не появился в ленте за 15 секунд"

    @allure.title("При создании нового заказа счётчик "
                  "«Выполнено за всё время» увеличивается")
    def test_total_completed_counter_increases(self, authorized_driver):
        main = MainPage(authorized_driver)
        feed = OrdersFeedPage(authorized_driver)

        main.go_to_orders_feed()
        total_before = feed.get_total_completed()

        main.go_to_constructor()
        main.drag_ingredient_to_basket(index=0)
        main.place_order()
        main.close_ingredient_modal()

        main.go_to_orders_feed()
        total_after = feed.wait_counter_increases(
            feed.get_total_completed, total_before
        )

        assert total_after > total_before, \
            f"Счётчик не увеличился: {total_before} -> {total_after}"

    @allure.title("При создании нового заказа счётчик "
                  "«Выполнено за сегодня» увеличивается")
    def test_today_completed_counter_increases(self, authorized_driver):
        main = MainPage(authorized_driver)
        feed = OrdersFeedPage(authorized_driver)

        main.go_to_orders_feed()
        today_before = feed.get_today_completed()

        main.go_to_constructor()
        main.drag_ingredient_to_basket(index=0)
        main.place_order()
        main.close_ingredient_modal()

        main.go_to_orders_feed()
        today_after = feed.wait_counter_increases(
            feed.get_today_completed, today_before
        )

        assert today_after > today_before, \
            f"Счётчик не увеличился: {today_before} -> {today_after}"

    @allure.title("После оформления заказа его номер "
                  "появляется в разделе «В работе»")
    def test_order_number_appears_in_progress(self, authorized_driver):
        main = MainPage(authorized_driver)
        profile = ProfilePage(authorized_driver)
        history = OrderHistoryPage(authorized_driver)
        feed = OrdersFeedPage(authorized_driver)

        main.drag_ingredient_to_basket(index=0)
        main.place_order()
        main.close_ingredient_modal()

        main.go_to_profile()
        profile.go_to_order_history()
        assert history.is_loaded(), "История заказов не открылась"

        user_orders = history.get_order_numbers()
        assert user_orders, "История заказов пуста"

        order_number = user_orders[-1]

        main.go_to_orders_feed()
        assert feed.is_loaded(), "Лента заказов не открылась"

        found = feed.wait_order_in_list(order_number, timeout=15)
        assert found, \
            f"Номер {order_number} не появился ни в «В работе», ни в «Готовы»"