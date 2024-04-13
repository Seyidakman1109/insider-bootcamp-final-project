import uuid
from datetime import datetime, timezone
import pytest
from base import insert_test_result_to_postgres


@pytest.fixture
def init_driver(request: pytest.FixtureRequest):
    """Fixture to initialize the WebDriver instance.

    Args:
        request (pytest.FixtureRequest): The request object from pytest.

    Yields:
        WebDriver: The initialized WebDriver instance.
    """
    # SETUP
    match request.config.getoption("browser"):
        case "chrome":
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver import Chrome

            opts = Options()
            opts.add_argument('--no-sandbox')
            opts.add_argument('--disable-gpu')
            opts.add_argument("--start-maximized")
            opts.add_argument("--disable-extensions")
            opts.add_argument("--proxy-bypass-list=*")
            opts.add_argument('--disable-dev-shm-usage')
            opts.add_argument("--window-size=1920,1080")
            opts.add_argument("--proxy-server='direct://'")
            opts.add_argument('--ignore-certificate-errors')
            opts.ignore_local_proxy_environment_variables()

            if not request.config.getoption("headed"):
                opts.add_argument("--headless")

            driver = Chrome(options=opts)

        case "firefox":
            from selenium.webdriver import Firefox, FirefoxOptions

            opts = FirefoxOptions()
            opts.add_argument("--width=1920")
            opts.add_argument("--height=1080")

            if not request.config.getoption("headed"):
                opts.add_argument("--headless")

            driver = Firefox(options=opts)

        case _:
            raise RuntimeError("Unsupported browser")

    request.cls.driver = driver

    yield

    # TEARDOWN
    if request.node.result_call.failed:
        driver.save_screenshot("failed_page.png")

    driver.close()
    driver.quit()


def pytest_addoption(parser: pytest.Parser):
    """Adds custom command-line options for pytest.

    Args:
        parser (pytest.Parser): The pytest parser object.
    """
    parser.addoption(
        '--browser', action='store', default="chrome", choices=["chrome", "firefox"],
        help='Browser engine which should be used. Default: "chrome"'
    )
    parser.addoption(
        '--headed', action='store_true', default=False,
        help='Headless mode option. Default: False'
    )

    parser.addoption(
        '--pg-username', action='store', default=None,
        help='Database username'
    )
    parser.addoption(
        '--pg-password', action='store', default=None,
        help='Database password'
    )
    parser.addoption(
        '--pg-host', action='store', default=None,
        help='Database host'
    )
    parser.addoption(
        '--pg-port', action='store', default=None,
        help='Database port'
    )
    parser.addoption(
        '--pg-database', action='store', default=None,
        help='Database name'
    )


def pytest_sessionstart(session: pytest.Session):
    """Initializes a dictionary to store test results in the session.

    Args:
        session (pytest.Session): The pytest session object.
    """
    session.id = uuid.uuid4().__str__()
    session.results = dict()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item):
    """Stores the test result in the session's results dictionary.

    Args:
        item (pytest.Item): The pytest item object.
    """
    outcome = yield
    result = outcome.get_result()
    setattr(item, "result_" + result.when, result)

    if result.when == "call" or result.outcome == "failed":
        item.session.results[item] = result

        session_id = item.session.id
        test_name = item.nodeid
        res = result.outcome
        duration = result.duration
        start_time = datetime.fromtimestamp(result.start,tz=timezone.utc)
        status = "pass" if res == "passed" else "fail"

        conn_cred = {
            "user": item.config.getoption("pg_username"),
            "password": item.config.getoption("pg_password"),
            "host": item.config.getoption("pg_host"),
            "port": item.config.getoption("pg_port"),
            "database": item.config.getoption("pg_database"),
        }

        insert_test_result_to_postgres(conn_cred, session_id, test_name, res, duration, start_time, status)
