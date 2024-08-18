from pages.BaseApplication import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from pages.SbisPageImages import SbisImagesLocators, SbisPageImages

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
        return self.find_region().click()

    def chooseclick_new_region(self):
        self.waiting_element_be_visible(SbisRegionLocators.LOCATOR_REGION_CHOOSE_OVERLAY)
        self.waiting_element_be_visible(SbisRegionLocators.LOCATOR_REGION_CHOOSE_INPUT)
        field = self.find_element(SbisRegionLocators.LOCATOR_NEW_REGION).click()
        try:
            self.waiting_element_be_invisible(SbisRegionLocators.LOCATOR_REGION_CHOOSE_INPUT)
        except TimeoutException:
            field = self.find_element(SbisRegionLocators.LOCATOR_NEW_REGION).click()

        self.reporter.log_step(f'Выполнено: выбор нового региона')
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

    def get_partner_list(self):
        partners = self.find_elements(SbisRegionLocators.LOCATOR_PARTNER)
        self.reporter.log_step(f'Выполнено: получен список партнеров')
        return [partner.text for partner in partners]

    def matches_partners(self, partners_first, partners_last):
        return not (set(partners_first) == set(partners_last))
