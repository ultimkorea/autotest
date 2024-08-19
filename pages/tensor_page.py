from pages.base_app import BasePage
from selenium.webdriver.common.by import By
from reporter.report import Report

reporter = Report()


class TensorHome(BasePage):
    LOCATOR_PEOPLEPOWER_DIV = (By.XPATH, "//div[contains(@class,'tensor_ru-Index__block4-content')]")
    LOCATOR_PEOPLEPOWER_LINK = (By.XPATH, "//div[contains(@class,'tensor_ru-Index__block4-content')]/p/a")
    LOCATOR_COOKIES_MSG = (By.CLASS_NAME, 'tensor_ru-CookieAgreement__close')

    def findclick_close_cookies_icon(self):
        field = self.find_element(TensorHome.LOCATOR_COOKIES_MSG).click()
        self.reporter.log_step(f'Выполнено: закрытие предупреждения о куках')
        return field

    def findclick_readmore_button(self):
        self.findclick_close_cookies_icon()
        self.find_element(TensorHome.LOCATOR_PEOPLEPOWER_LINK).click()
        self.page_load()
        self.reporter.log_step(f'Выполнено: нажатие на ссылку: Подробнее')
        return TensorAbout(self.driver)

    @property
    def check_peoplepower_is_displayed(self):
        field_div = self.find_element(TensorHome.LOCATOR_PEOPLEPOWER_DIV)
        return field_div.is_displayed()


class TensorAbout(BasePage):
    LOCATOR_ABOUT_IMAGES = (By.XPATH, "//div[contains(@class, 'tensor_ru-About__block3-image-wrapper')]/img")

    def check_current_url(self, url):
        return self.current_url == url

    @property
    def images(self):
        field = self.find_elements(TensorAbout.LOCATOR_ABOUT_IMAGES)
        self.reporter.log_step(f'Выполнено: получены искомые изображения')
        return field

    def check_width_height_of_images(self, images):
        res = [f"{image.size['height']}:{image.size['width']}" for image in images]
        if set(res).__len__() == 1:
            return True
        else:
            res = f'Размеры некоторых изображений отличаются: {res}'
            return res