from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from base import BasePage, BaseConfig
import time


class CareerPage(BasePage):
    TEAMS_BLOCK = (By.ID, "career-find-our-calling")
    LOCATION_BLOCK = (By.ID, "location-slider")
    LIFE_AT_INSIDER = (By.XPATH, "/html/body/div[1]/section[4]")
    GET_ALL_QA_JOBS_BUTTON = (By.LINK_TEXT, 'See all QA jobs')
    LOCATION_FILTER = (By.ID, "filter-by-location")
    DEPARTMENT_FILTER = (By.ID, "filter-by-department")
    JOBS_CONTAINER = (By.CSS_SELECTOR, "#jobs-list > div")
    JOB_TITLE = (By.CLASS_NAME, "position-title")
    JOB_DEPARTMENT = (By.CLASS_NAME, "position-department")
    JOB_LOCATION = (By.CLASS_NAME, "position-location")
    VIEW_ROLE_BUTTON = (By.LINK_TEXT, "View Role")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def get_teams_block(self):
        """Gets the teams block element.

        Returns:
            WebElement or None: The teams block WebElement if found, otherwise None.
        """
        _block = self.find_elements(self.TEAMS_BLOCK)
        if _block:
            self.scroll_element(_block[0])
            time.sleep(1)
            return _block[0]
        return None

    def get_location_block(self):
        """Gets the location block element.

        Returns:
            WebElement or None: The location block WebElement if found, otherwise None.
        """
        _block = self.find_elements(self.LOCATION_BLOCK)
        if _block:
            self.scroll_element(_block[0])
            time.sleep(1)
            return _block[0]
        return None

    def get_life_at_insider_block(self):
        """Gets the life at Insider block element.

        Returns:
            WebElement or None: The life at Insider block WebElement if found, otherwise None.
        """
        _block = self.find_elements(self.LIFE_AT_INSIDER)
        if _block:
            self.scroll_element(_block[0])
            time.sleep(1)
            return _block[0]
        return None

    def navigate_to_qa_career(self):
        """Navigates to the QA career page.

        This method navigates to the QA career page by appending the QA career page route to the base URL.

        """
        self.navigate_to_url(BaseConfig.BASE_URL + BaseConfig.QA_CAREER_PAGE_ROUTE)

    def get_filtered_qa_jobs(self):
        """Gets filtered QA jobs.

        This method filters QA jobs by clicking the "Get All QA Jobs" button, selecting location as "Istanbul, Turkey",
        selecting department as "Quality Assurance", and returns the job containers found.

        Returns:
            list[WebElement]: List of WebElement objects representing the filtered QA job containers.
        """
        self.click(self.GET_ALL_QA_JOBS_BUTTON)
        self.select(
            mark=self.LOCATION_FILTER,
            selector="Istanbul, Turkey",
            selector_type="text"
        )
        self.select(
            mark=self.DEPARTMENT_FILTER,
            selector="Quality Assurance",
            selector_type="text"
        )
        time.sleep(3)
        return self.find_elements(self.JOBS_CONTAINER)

    def get_job_info(self, job: WebElement):
        """Gets information about a job.

        Args:
            job (WebElement): The job WebElement to extract information from.

        Returns:
            tuple: A tuple containing job title (WebElement), job department (WebElement), and job location (WebElement).
        """
        self.scroll_element(job)
        job_title = job.find_element(*self.JOB_TITLE)
        job_department = job.find_element(*self.JOB_DEPARTMENT)
        job_location = job.find_element(*self.JOB_LOCATION)
        return job_title, job_department, job_location

    def click_view_role_and_switch_to_second_tab(self):
        """Clicks the View Role button and switches to the second tab.

        This method clicks the View Role button, waits for 2 seconds, and then switches to the second tab.

        """
        self.click(self.VIEW_ROLE_BUTTON)
        time.sleep(2)
        self.driver.switch_to.window(self.driver.window_handles[1])
