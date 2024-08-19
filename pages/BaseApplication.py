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
        """ Иногда падаем с ошибкой StaleElementReference и/и ElementClickInterceptedException
         для этого обернул поиск элемента в try/except;
          update: в третьем сценарии еще стреляет ElementClickInterceptedException"""
        try:
            res = WebDriverWait(self.driver, time).until(EC.element_to_be_clickable(locator),
                                                      message=f"Не удалось найти элемент с локатором: {locator}")
            #self.reporter.log_step(f'Найден элемент по локатору: "{locator}"')
            # иногда нужные элементы скрываются за предупреждением о куках в футере страницы
            # поэтому скролим до появления
            self.driver.execute_script("arguments[0].scrollIntoView(true);", res)
            return res
        except (StaleElementReferenceException, ElementClickInterceptedException):
            if count == 3:
                raise StaleElementReferenceException(f'Не удалось найти элемент по локатору {locator} после 3 попыток ')
            count += 1
            return self.find_element(locator, time, count)

    def find_elements(self, locator, time=5, count=0):
        res = WebDriverWait(self.driver, time).until(EC.presence_of_all_elements_located(locator),
                                                    message=f"Не удалось найти элементы по локатору: {locator}")
        #self.reporter.log_step(f'Найдены элементы по локатору: "{locator}"')
        return res

    def find_element_in_element(self, locator, element, time=10):
        res = WebDriverWait(element, time).until(EC.element_to_be_clickable(locator),
                                                      message=f"Внутри {element} не удалось найти элементы с локатором: {locator}")
        #self.reporter.log_step(f'Найден элемент по локатору: {locator}')
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