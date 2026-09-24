import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import BASE_URL, TEST_EMAIL, TEST_PASSWORD
from locators import MainPageLocators
from pages.main_page import MainPage
from pages.login_page import LoginPage


@pytest.fixture(params=["chrome", "firefox"], scope="function")
def driver(request):
    if request.param == "chrome":
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        driver = webdriver.Chrome(options=options)
    else:
        options = FirefoxOptions()
        options.set_preference("signon.rememberSignons", False)
        options.set_preference("dom.webnotifications.enabled", False)
        driver = webdriver.Firefox(options=options)
        driver.maximize_window()

    driver.get(BASE_URL)
    yield driver
    driver.quit()


@pytest.fixture
def authorized_driver(driver):
    main_page = MainPage(driver)
    login_page = LoginPage(driver)

    main_page.go_to_profile()
    login_page.login(TEST_EMAIL, TEST_PASSWORD)

    WebDriverWait(driver, 10).until(
        EC.url_changes(driver.current_url)
    )

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(MainPageLocators.ORDER_BUTTON)
    )

    return driver


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(autouse=True)
def screenshot_on_failure(driver, request):
    yield
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"failure_{request.node.name}",
            attachment_type=allure.attachment_type.PNG
        )