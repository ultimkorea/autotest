import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import allure
from reporter.report import Report
import os


@allure.title("init: webdriver init")
@pytest.fixture()
def browser():
    options = Options()
    options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)

    yield driver
    driver.quit()


@allure.title("init: allure-reporter")
@pytest.fixture()
def reporter():
    reporter = Report()
    return reporter



