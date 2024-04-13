from pages import HomePage
from base import BaseTest


class TestInsider(BaseTest):

    def test_insider(self):
        home_page = HomePage(driver=self.driver)
        home_page.accept_cookies()
        careers_page = home_page.open_careers_page()

        assert "Career" in careers_page.get_title(), "Page title is incorrect"
        assert "/careers" in careers_page.get_current_url(), "Page URL route is incorrect"

        assert careers_page.get_teams_block(), "Teams block not found"
        assert careers_page.get_location_block(), "Locations block not found"
        assert careers_page.get_life_at_insider_block(), "Life at Insider block not found"

        careers_page.navigate_to_qa_career()
        assert "Insider quality assurance job opportunities" == careers_page.get_title(), "Page title is incorrect"

        jobs = careers_page.get_filtered_qa_jobs()
        assert jobs, "No jobs found for Quality Assurance"

        job = None
        for job in jobs:
            job_title, job_department, job_location = careers_page.get_job_info(job)
            assert "Quality Assurance" in job_title.text or "QA" in job_title.text
            assert "Quality Assurance" in job_department.text
            assert "Istanbul, Turkey" in job_location.text

        careers_page.hover(job)
        careers_page.click_view_role_and_switch_to_second_tab()
        assert "jobs.lever.co" in careers_page.get_current_url()
