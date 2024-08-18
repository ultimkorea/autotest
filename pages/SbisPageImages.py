from pages.BaseApplication import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import allure

class SbisImagesLocators:
    LOCATOR_CONTACTS_BUTTON = (By.XPATH, "//a[contains(@class,'sbisru-Header__menu-link') and text()='Контакты']")
    LOCATOR_LOGO_IMAGE = (By.XPATH, "//div[contains(@class,'sbisru-Contacts__border-left--border-xm')]/a/img")
    LOCATOR_COOKIES_MSG =(By.CLASS_NAME,'tensor_ru-CookieAgreement__close')
    # сомнительно, наверное, лучше использовать класс на уровень выше
    # и проверять наличие <p> с текстом Сила в людях (внутри div'a)
    LOCATOR_PEOPLEPOWER_DIV = (By.XPATH, "//div[contains(@class,'tensor_ru-Index__block4-content')]")
    LOCATOR_PEOPLEPOWER_P = (By.TAG_NAME, "a")
    LOCATOR_ABOUT_IMAGES = (By.XPATH,"//div[contains(@class, 'tensor_ru-About__block3-image-wrapper')]/img")


class SbisPageImages(BasePage):

    def findclick_contacts_button(self):
        field = self.find_element(SbisImagesLocators.LOCATOR_CONTACTS_BUTTON).click()
        self.page_load()
        self.reporter.log_step(f'Выполнено: нажатие на ссылку Контакты')
        return field

    def findclick_logo_image(self):
        field = self.find_element(SbisImagesLocators.LOCATOR_LOGO_IMAGE).click()
        self.change_active_window(1)
        self.page_load()
        self.findclick_close_cookies_icon()
        self.reporter.log_step(f'Выполнено: нажатие на логотип тензора')
        return field

    def findclick_close_cookies_icon(self):
        field = self.find_element(SbisImagesLocators.LOCATOR_COOKIES_MSG).click()
        self.reporter.log_step(f'Выполнено: закрытие предупреждения о куках')
        return field

    def findclick_readmore_button(self):
        field_div = self.find_element(SbisImagesLocators.LOCATOR_PEOPLEPOWER_DIV)
        field_p = self.find_element_in_element(SbisImagesLocators.LOCATOR_PEOPLEPOWER_P, field_div).click()
        self.page_load()
        self.reporter.log_step(f'Выполнено: нажатие на ссылку: Подробнее')
        return field_p

    @property
    def check_peoplepower_is_displayed(self):
        field_div = self.find_element(SbisImagesLocators.LOCATOR_PEOPLEPOWER_DIV)
        return field_div.is_displayed()

    @property
    def check_current_url(self):
        return self.current_url == 'https://tensor.ru/about'

    @property
    def images(self):
        field = self.find_elements(SbisImagesLocators.LOCATOR_ABOUT_IMAGES)
        self.reporter.log_step(f'Выполнено: получены искомые изображения')
        return field

    def check_width_height_of_images(self, images):
        res = [f"{image.size['height']}:{image.size['width']}" for image in images]
        if set(res).__len__() == 1:
            return True
        else:
            res = f'Размеры некоторых изображений отличаются: {res}'
            return res
