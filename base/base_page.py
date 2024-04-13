from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


class BasePage:
    ACCEPT_COOKIES = (By.ID, "wt-cli-accept-all-btn")

    def __init__(self, driver: WebDriver):
        self.driver: WebDriver = driver
        self.timeout = 10

    def navigate_to_url(self, url) -> None:
        """
        Navigates to the Url

        :param url: Url of the web page
        """
        self.driver.get(url)

    def find_element(self, locator) -> WebElement:
        """
        Find element for the given LOCATOR

        :param locator: Locator
        :return: WebElement
        """
        return WebDriverWait(self.driver, self.timeout).until(ec.presence_of_element_located(locator),
                                                              message=f"Element <{locator}> is not present")

    def find_elements(self, locator) -> list[WebElement]:
        """
        Find elements for the given LOCATOR

        :param locator: Locator
        :return: list
        """
        return WebDriverWait(self.driver, self.timeout).until(ec.presence_of_all_elements_located(locator))

    def click(self, mark) -> None:
        """
        Clicks to the given element

        :param mark: Locator or WebElement
        """
        if isinstance(mark, WebElement):
            element = mark
        else:
            element = self.find_element(mark)
        element.click()

    def scroll_element(self, mark) -> None:
        """
        Scrolls to the given element on the page

        :param mark: Locator or Web Element
        """
        if isinstance(mark, WebElement):
            element = mark
        else:
            element = self.find_element(mark)
        self.driver.execute_script("arguments[0].scrollIntoView(false)", element)

    def get_title(self) -> str:
        """
        Returns Browser Tab Title

        :return: str
        """
        return self.driver.title

    def get_current_url(self) -> str:
        """
        Returns current URL

        :return: str
        """
        return self.driver.current_url

    def select(self, mark, selector, selector_type="value") -> None:
        """
        Selects the selected element

        :param mark: Locator or Select element
        :param selector: Selector which includes different types of value/index/text
        :param selector_type: Selector_type can be given as value/index/text
        """
        if isinstance(mark, WebElement):
            element = mark
        else:
            if selector_type == "text":
                WebDriverWait(driver=self.driver, timeout=self.timeout).until(
                    ec.text_to_be_present_in_element(mark, selector)
                )
            element = self.find_element(mark)

        self.scroll_element(element)
        select = Select(element)
        if selector_type == "value":
            select.select_by_value(selector)
        elif selector_type == "index":
            select.select_by_index(selector)
        elif selector_type == "text":
            select.select_by_visible_text(selector)

    def hover(self, mark) -> None:
        """
        Hovers to the given element on the page

        :param mark: Locator or Web Element
        """
        if isinstance(mark, WebElement):
            element = mark
        else:
            element = self.find_element(mark)
        hover = ActionChains(self.driver).move_to_element(element)
        hover.perform()
