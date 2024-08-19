from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from reporter.report import Report
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException

reporter = Report()


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.base_url = 'https://sbis.ru/'
        self.reporter = reporter

    def page_load(self):
        return self.driver.execute_script("return document.readyState === 'complete'")

    def find_element(self, locator, time=10, count=1):
        """ Иногда падаем с ошибкой StaleElementReference и/и ElementClickInterceptedException
         для этого обернул поиск элемента в try/except;
          update: в третьем сценарии еще стреляет ElementClickInterceptedException"""
        try:
            res = WebDriverWait(self.driver, time).until(EC.visibility_of_element_located(locator),
                                                      message=f"Не удалось найти элемент с локатором: {locator}")
            if not res.is_displayed():
                self.driver.execute_script("arguments[0].scrollIntoView(true);", res)
            return res
        except StaleElementReferenceException:
            if count == 3:
                raise StaleElementReferenceException(f'Не удалось найти элемент по локатору {locator} после 3 попыток ')
            count += 1
            return self.find_element(locator, time, count)

    def find_elements(self, locator, time=10, count=0):
        res = WebDriverWait(self.driver, time).until(EC.presence_of_all_elements_located(locator),
                                                    message=f"Не удалось найти элементы по локатору: {locator}")
        #self.reporter.log_step(f'Найдены элементы по локатору: "{locator}"')
        return res


    def wait_until(self, condition, time=5):
        WebDriverWait(self.driver, time).until(condition)

    @property
    def current_url(self):
        res = self.driver.current_url
        return res

    @property
    def current_title(self):
        res = self.driver.title.lower()
        return res

    def open_start_url(self):
        res = self.driver.get(self.base_url)
        self.page_load()
        self.reporter.log_step(f'Выполнен переход на стартовую страницу {self.base_url}')
        return res

    def change_active_window(self, window_index):
        res = self.driver.switch_to.window(self.driver.window_handles[window_index])
        self.reporter.log_step(f'Изменено акативное окна драйвера')
        return res