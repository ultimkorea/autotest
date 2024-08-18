from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException

class BasePage:

    def __init__(self, driver, reporter, path=None):
        self.driver = driver
        self.base_url = 'https://sbis.ru/'
        self.reporter = reporter
        if path:
            self.default_path = path
            self.file_name = ''


    def page_load(self):
        return self.driver.execute_script("return document.readyState === 'complete'")

    def find_element(self, locator, time=5, count=1):
        """ Иногда падаем с ошибкой StaleElementReference и/и
         для этого обернул поиск элемента в try/except;
          update: в третьем сценарии еще стреляет ElementClickInterceptedException"""
        try:
            res = WebDriverWait(self.driver, time).until(EC.element_to_be_clickable(locator),
                                                      message=f"Не удалось найти элемент с локатором: {locator}")
            #self.reporter.log_step(f'Найден элемент по локатору: "{locator}"')
            return res
        except (StaleElementReferenceException, ElementClickInterceptedException):
            if count == 3:
                raise StaleElementReferenceException(f'Не удалось найти элемент по локатору {locator} ')
            count += 1
            self.find_element(locator, time, count)

    def find_elements(self, locator, time=5, count=0):
        res = WebDriverWait(self.driver, time).until(EC.presence_of_all_elements_located(locator),
                                                    message=f"Не удалось найти элементы по локатору: {locator}, осталось попыток: {count}")
        #self.reporter.log_step(f'Найдены элементы по локатору: "{locator}"')
        return res

    def find_element_in_element(self, locator, element, time=10):
        res = WebDriverWait(element, time).until(EC.element_to_be_clickable(locator),
                                                      message=f"Внутри {element} не удалось найти элементы с локатором: {locator}")
        #self.reporter.log_step(f'Найден элемент по локатору: {locator}')
        return res

    def waiting_element_be_invisible(self, locator, time=5):
        res = WebDriverWait(self.driver, time).until(EC.invisibility_of_element_located(locator),
                                                  message=f"Не удалось дождаться исчезновения элемента с локатором: {locator}")
        return res

    def waiting_element_be_visible(self, locator, time=5):
        return WebDriverWait(self.driver, time).until(EC.visibility_of_element_located(locator),
                                                      message=f"Не удалось дождаться появления элемента с локатором: {locator}")

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