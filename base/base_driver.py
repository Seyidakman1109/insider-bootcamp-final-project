from selenium.webdriver import Chrome
import pytest


@pytest.mark.usefixtures("init_driver")
class BaseTest:
    driver: Chrome
