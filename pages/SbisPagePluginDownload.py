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


    def plugin_fact_size(self, filesize):
        """ Переводим байты в мегабайты, округляем до 2 точек после запятой """
        file_size = round(filesize / (1024 * 1024), 2)
        return file_size

    def get_filesize_from_head_request(self):
        url = self.download_link
        pre_response = requests.head(url)
        st_code = pre_response.status_code
        if st_code == 302:
            response = requests.head(pre_response.headers['Location'])
            if response.status_code == 200:
                file_size = int(response.headers['Content-Length'])
        elif st_code == 200:
            # если вдруг нет редиректа
            file_size = int(pre_response.headers['Content-Length'])
        else:
            raise Exception(f'Status code == {st_code}, ошибка выполнения запроса')

        return file_size






