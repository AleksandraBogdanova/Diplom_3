from selenium.webdriver.common.by import By


class CommonLocators:
    MODAL_OVERLAY = (By.CSS_SELECTOR, "[class*='Modal_modal_overlay']")
    MODAL_CONTENT = (By.CSS_SELECTOR, "[class*='Modal_modal__contentBox']")
    MODAL_CLOSE = (By.CSS_SELECTOR, "[class*='Modal_modal__close']")


class HeaderLocators:
    CONSTRUCTOR_LINK = (By.CSS_SELECTOR, "a[href='/']")
    ORDERS_FEED_LINK = (By.CSS_SELECTOR, "a[href='/feed']")
    PROFILE_LINK = (By.CSS_SELECTOR, "a[href='/account']")


class MainPageLocators:
    TITLE = (By.XPATH, "//h1[text()='Соберите бургер']")
    BUNS_TAB = (By.XPATH, "//span[text()='Булки']")
    SAUCES_TAB = (By.XPATH, "//span[text()='Соусы']")
    FILLINGS_TAB = (By.XPATH, "//span[text()='Начинки']")
    INGREDIENT_CARD = (By.CSS_SELECTOR, "[class*='BurgerIngredient_ingredient']")
    INGREDIENT_COUNTER = (By.CSS_SELECTOR, "[class*='counter_counter__num']")
    BASKET = (By.CSS_SELECTOR, "section[class*='BurgerConstructor_basket']")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти в аккаунт']")
    INGREDIENT_MODAL = (By.CSS_SELECTOR, "[class*='Modal_modal__contentBox']")
    INGREDIENT_MODAL_CLOSE = (By.CSS_SELECTOR, "[class*='Modal_modal__close']")
    ORDER_NUMBER = (
        By.CSS_SELECTOR,
        "[class*='Modal_orderBox'] p.text_type_digits-default"
    )
    ORDER_BUTTON = (By.XPATH, "//button[text()='Оформить заказ']")


class LoginPageLocators:
    TITLE = (By.XPATH, "//h2[text()='Вход']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='name']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='Пароль']")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти']")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a[href='/forgot-password']")
    REGISTER_LINK = (By.CSS_SELECTOR, "a[href='/register']")
    PASSWORD_TOGGLE = (By.CSS_SELECTOR, "div[class*='input__icon-action']")


class ForgotPasswordPageLocators:
    TITLE = (By.XPATH, "//h2[text()='Восстановление пароля']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='name']")
    RESTORE_BUTTON = (By.XPATH, "//button[text()='Восстановить']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='Введите новый пароль']")
    CODE_INPUT = (By.CSS_SELECTOR, "input[name='Введите код из письма']")
    SAVE_BUTTON = (By.XPATH, "//button[text()='Сохранить']")
    LOGIN_LINK = (By.CSS_SELECTOR, "a[href='/login']")
    PASSWORD_TOGGLE = (By.CSS_SELECTOR, "div[class*='input__icon-action']")


class ProfilePageLocators:
    PROFILE_LINK = (By.CSS_SELECTOR, "a[href='/account/profile']")
    ORDER_HISTORY_LINK = (By.CSS_SELECTOR, "a[href='/account/order-history']")
    LOGOUT_BUTTON = (By.XPATH, "//button[text()='Выход']")
    TITLE = (By.XPATH, "//h2[contains(text(), 'Личный')]")


class OrderHistoryPageLocators:
    ORDER_ITEMS = (By.CSS_SELECTOR, "[class*='OrderHistory_listItem']")
    ORDER_LINKS = (By.CSS_SELECTOR, "[class*='OrderHistory_link']")
    ORDER_NUMBER = (By.CSS_SELECTOR, "p[class*='text_type_digits-default']")
    ORDER_LIST_ITEMS = (By.CSS_SELECTOR, "p[class*='text_type_digits-default']")


class OrdersFeedPageLocators:
    TITLE = (By.XPATH, "//h1[text()='Лента заказов']")
    ORDER_CARD = (By.CSS_SELECTOR, "[class*='OrderFeed_list'] > li")
    ORDER_LINK = (By.CSS_SELECTOR, "[class*='OrderFeed_list'] > li a")
    ORDER_LISTS = (By.CSS_SELECTOR, "[class*='OrderFeed_orderList']")
    ORDER_LIST_ITEMS = (By.TAG_NAME, "li")

    TOTAL_COMPLETED_COUNTER = (
        By.XPATH,
        "(//p[contains(@class, 'OrderFeed_number')])[1]"
    )
    TODAY_COMPLETED_COUNTER = (
        By.XPATH,
        "(//p[contains(@class, 'OrderFeed_number')])[2]"
    )

    ORDER_MODAL = (By.CSS_SELECTOR, "[class*='Modal_orderBox']")
    ORDER_MODAL_CLOSE = (By.CSS_SELECTOR, "[class*='Modal_modal__close']")