# Insider Selenium Automation Task

## Technologies Used

- Python 3.11
- Selenium
- Pytest

## Installation

After downloading the project, install the required libraries by running the following command in your terminal or command prompt:

```bash
pip install -r requirements.txt
```

## Running Tests

To run the test cases, execute the following command in your terminal or command prompt:

```bash
pytest --browser <browser> --pg-username <username> --pg-password <password> --pg-host <host> --pg-port <port> --pg-database <database>
```

By default, test cases run in headless mode. However, you can run them in headed mode.

Options:
- `--headed`: Runs the browser visibly.
-  `--browser`: Specifies the browser to be used by Selenium driver (e.g., chrome, firefox).
-  `--pg-username`: Specifies the PostgreSQL username for database connection.
-  `--pg-password`: Specifies the PostgreSQL password for database connection.
-  `--pg-host`: Specifies the PostgreSQL host address.
-  `--pg-port`: Specifies the PostgreSQL port number.
-  `--pg-database`: Specifies the name of the PostgreSQL database.

Example usage:

```bash
pytest --headed --browser chrome
```

This command will run the tests in headed mode and Chrome webdriver.

---

This README file provides essential information for Insider Selenium Automation Task. If you have any questions regarding the project, feel free to reach out.