from pages.BaseApplication import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from pages.SbisPageImages import SbisImagesLocators, SbisPageImages
from selenium.webdriver.support import expected_conditions as EC

class SbisRegionLocators:
    LOCATOR_REGION_CHOOSER = (By.XPATH, "//span[contains(@class,'sbis_ru-Region-Chooser__text sbis_ru-link')]")
    LOCATOR_REGION_CHOOSEN_KAMCHATKA = (By.XPATH, "//span[contains(@class,'sbis_ru-Region-Chooser__text sbis_ru-link') and text()='Камчатский край']")
    LOCATOR_PARTNERS = (By.XPATH, "//div[contains(@class,'sbisru-Contacts-City__flex sbisru-Contacts-Shot')]")
    LOCATOR_NEW_REGION = (By.XPATH,"//span[@title = 'Камчатский край']/span")
    LOCATOR_PARTNER = (By.CLASS_NAME, "sbisru-Contacts-List__name")
    LOCATOR_REGION_CHOOSE_OVERLAY = (By.XPATH, "//div[contains(@class,'sbis_ru-Region-Panel__overlay')]")
    LOCATOR_REGION_CHOOSE_INPUT = (By.XPATH, "//input[contains(@class,'controls-Field')]")
class SbisPageRegion(SbisPageImages):

    def find_region(self):
        return self.find_element(SbisRegionLocators.LOCATOR_REGION_CHOOSER)

    @property
    def region(self):
        return self.find_region().text.lower()

    def region_click(self):
        res = self.find_region().click()
        self.wait_until(EC.visibility_of_element_located(SbisRegionLocators.LOCATOR_REGION_CHOOSE_INPUT))
        return res
    def chooseclick_new_region(self):
        old_first_partner = self.get_partner_list()[0]
        self.region_click()
        field = self.find_element(SbisRegionLocators.LOCATOR_NEW_REGION).click()
        self.wait_until(EC.visibility_of_element_located(SbisRegionLocators.LOCATOR_REGION_CHOOSER))
        self.reporter.log_step(f'Выполнено: выбор нового региона')
        # здесь же дождемся пока пропадет старый блок с партнерами
        self.wait_until(EC.staleness_of(old_first_partner))

        return field

    @property
    def check_moscow_region(self):
        return 'москва' in self.region

    @property
    def check_kamchatka_region(self):
        if self.find_element(SbisRegionLocators.LOCATOR_REGION_CHOOSEN_KAMCHATKA):
            return True
        return False

    @property
    def check_kamchatka_url(self):
        return '41-kamchatskij-kraj' in self.current_url

    @property
    def check_kamchatka_title(self):
        return 'камчатский край' in self.current_title

    def get_partner_list(self, old=False):
        partners = self.find_elements(SbisRegionLocators.LOCATOR_PARTNER)
        self.reporter.log_step(f'Выполнено: получен список партнеров')
        if old:
            return [partner.text for partner in partners]
        return partners

    def matches_partners(self, old):
        new = [partner.text for partner in self.get_partner_list()]
        return not (set(old) == set(new))
