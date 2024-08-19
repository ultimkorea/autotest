from pages.BaseApplication import BasePage
from selenium.webdriver.common.by import By
import allure
import requests
import os

class SbisPluginDownloaderLocators:
    LOCATOR_LOCAL_VERSION_BUTTON = (By.XPATH, "//a[contains(@class,'sbisru-Footer__link') and text()='Скачать локальные версии']")
    LOCATOR_DOWNLOAD_LINK = (By.XPATH, "//a[contains(@href,'sbisplugin-setup-web')]")

class SbisPluginDownloader(BasePage):

    def findclick_download_page(self):
        field = self.find_element(SbisPluginDownloaderLocators.LOCATOR_LOCAL_VERSION_BUTTON).click()
        self.page_load()
        self.reporter.log_step(f'Выполнено: нажатие на ссылку "Скачать локальные версии"')
        return field

    @property
    def download_link(self):
        field = self.find_element(SbisPluginDownloaderLocators.LOCATOR_DOWNLOAD_LINK)
        link = field.get_attribute('href')
        self.reporter.log_step(f'Выполнено: получена ссылка на скачивание web-версии плагина"')
        return link

    @property
    def plugin_plan_size(self):
        field = self.find_element(SbisPluginDownloaderLocators.LOCATOR_DOWNLOAD_LINK)
        text = field.text
        for item in text.split(' '):
            try:
                res = float(item)
                return res
            except ValueError:
                pass

        return False

    @property
    def plugin_fact_size(self):
        """ Переводим байты в мегабайты, округляем до 2 точек после запятой """
        file_size = round(os.path.getsize(self.file_name) / (1024 * 1024), 2)
        return file_size


    def download_file(self, repeat = False):
        url = self.download_link
        response = requests.get(url)

        if response.status_code != 200:
            # попробуем еще один раз скачать, если не получится - рейзим исключение
            if not repeat:
                self.download_file(repeat=True)
            raise Exception(f'status_code = {response.status_code}, запрос выполнен с ошибкой')

        self.file_name = self.default_path+'sbis-plugin.exe'
        self.save_file(self.file_name, response.content)

    def save_file(self, file_name, file):
        with open(file_name, 'wb') as f:
            f.write(file)
            self.file_name = file_name






