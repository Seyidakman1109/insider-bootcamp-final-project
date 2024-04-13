from selenium.webdriver.common.by import By
from base import BasePage, BaseConfig
from .career_page import CareerPage


class HomePage(BasePage):
    COMPANY_NAVIGATOR = (By.PARTIAL_LINK_TEXT, "Company")
    CAREERS_NAVIGATOR = (By.PARTIAL_LINK_TEXT, "Careers")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.navigate_to_url(BaseConfig.BASE_URL)

    def accept_cookies(self):
        """Accepts cookies by clicking the accept button."""
        self.click(self.ACCEPT_COOKIES)

    def open_careers_page(self) -> CareerPage:
        """Opens the careers page.

        Returns:
            CareerPage: An instance of CareerPage representing the opened careers page.
        """
        self.click(self.COMPANY_NAVIGATOR)
        self.click(self.CAREERS_NAVIGATOR)
        return CareerPage(self.driver)
