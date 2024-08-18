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


@allure.title("init: create/delete temp directory")
@pytest.fixture()
def filesystem():
    dir_name = 'temp/'
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    yield dir_name
    for file in os.listdir(f'{dir_name}'):
        os.remove(f'{dir_name}{file}')
    os.rmdir(dir_name)



