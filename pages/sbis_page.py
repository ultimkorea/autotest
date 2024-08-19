from pages.base_app import BasePage
from selenium.webdriver.common.by import By
from pages.tensor_page import TensorHome
from reporter.report import Report
from selenium.webdriver.support import expected_conditions as EC
import requests

reporter = Report()


class SbisHome(BasePage):
    LOCATOR_CONTACTS_BUTTON = (By.XPATH, "//a[contains(@class,'sbisru-Header__menu-link') and text()='Контакты']")
    LOCATOR_LOCAL_VERSION_BUTTON = (
        By.XPATH, "//a[contains(@class,'sbisru-Footer__link') and text()='Скачать локальные версии']")

    def findclick_download_page(self):
        self.find_element(SbisHome.LOCATOR_LOCAL_VERSION_BUTTON).click()
        self.page_load()
        self.reporter.log_step(f'Выполнено: нажатие на ссылку "Скачать локальные версии"')
        return SbisPluginSize(self.driver)

    def findclick_contacts_button(self):
        self.find_element(SbisHome.LOCATOR_CONTACTS_BUTTON).click()
        self.page_load()
        self.reporter.log_step(f'Выполнено: нажатие на ссылку Контакты')
        return SbisContacts(self.driver)


class SbisContacts(BasePage):
    LOCATOR_LOGO_IMAGE = (By.XPATH, "//div[contains(@class,'sbisru-Contacts__border-left--border-xm')]/a/img")
    LOCATOR_REGION_CHOOSER = (By.XPATH, "//span[contains(@class,'sbis_ru-Region-Chooser__text sbis_ru-link')]")
    LOCATOR_REGION_CHOOSEN_KAMCHATKA = (By.XPATH, "//span[contains(@class,'sbis_ru-Region-Chooser__text sbis_ru-link') and text()='Камчатский край']")
    LOCATOR_NEW_REGION = (By.XPATH,"//span[@title = 'Камчатский край']/span")
    LOCATOR_PARTNER = (By.CLASS_NAME, "sbisru-Contacts-List__name")
    LOCATOR_REGION_CHOOSE_INPUT = (By.XPATH, "//input[contains(@class,'controls-Field')]")

    def findclick_logo_image(self):
        self.find_element(SbisContacts.LOCATOR_LOGO_IMAGE).click()
        self.change_active_window(1)
        self.page_load()
        self.reporter.log_step(f'Выполнено: нажатие на логотип тензора')
        return TensorHome(self.driver)

    def get_partner_list(self, old=False):
        partners = self.find_elements(SbisContacts.LOCATOR_PARTNER)
        self.reporter.log_step(f'Выполнено: получен список партнеров')
        if old:
            return [partner.text for partner in partners]
        return partners

    @property
    def check_kamchatka_region(self):
        if self.find_element(SbisContacts.LOCATOR_REGION_CHOOSEN_KAMCHATKA):
            return True
        return False

    @property
    def check_kamchatka_url(self):
        return '41-kamchatskij-kraj' in self.current_url

    @property
    def check_kamchatka_title(self):
        return 'камчатский край' in self.current_title

    def find_region(self):
        return self.find_element(SbisContacts.LOCATOR_REGION_CHOOSER)

    @property
    def region(self):
        return self.find_region().text.lower()

    def region_click(self):
        res = self.find_region().click()
        self.wait_until(EC.visibility_of_element_located(SbisContacts.LOCATOR_REGION_CHOOSE_INPUT))
        return res

    def chooseclick_new_region(self):
        old_first_partner = self.get_partner_list()[0]
        self.region_click()
        field = self.find_element(SbisContacts.LOCATOR_NEW_REGION).click()
        self.wait_until(EC.visibility_of_element_located(SbisContacts.LOCATOR_REGION_CHOOSER))
        self.reporter.log_step(f'Выполнено: выбор нового региона')
        # здесь же дождемся пока пропадет старый блок с партнерами
        # т.к. иногда не успевает пропасть перед получением нового списка
        self.wait_until(EC.staleness_of(old_first_partner))
        return field

    @property
    def check_moscow_region(self):
        return 'москва' in self.region

    def matches_partners(self, old):
        new = [partner.text for partner in self.get_partner_list()]
        return not (set(old) == set(new))


class SbisPluginSize(BasePage):
    LOCATOR_DOWNLOAD_LINK = (By.XPATH, "//a[contains(@href,'sbisplugin-setup-web')]")

    @property
    def download_link(self):
        field = self.find_element(SbisPluginSize.LOCATOR_DOWNLOAD_LINK)
        link = field.get_attribute('href')
        self.reporter.log_step(f'Выполнено: получена ссылка на скачивание web-версии плагина"')
        return link

    @property
    def plugin_plan_size(self):
        field = self.find_element(SbisPluginSize.LOCATOR_DOWNLOAD_LINK)
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
