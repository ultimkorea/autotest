from pages.sbis_page import SbisHome, SbisContacts
from pages.tensor_page import TensorHome, TensorAbout

def test_check_width_height_of_images(browser):
    """
    Тестовое задание СБИС (Автотестирование) №1
    1. Проверка наличия блока Сила в людях
    2. Проверерка текущего URL после перехода из блока Сила в людях
    3. Проверка-сравнение высоты и ширины изображений на странице /about
    """

    sbisHome_page = SbisHome(browser)
    sbisHome_page.open_start_url()

    sbis_contacs_page = sbisHome_page.findclick_contacts_button()

    tensor_home_page = sbis_contacs_page.findclick_logo_image()

    assert tensor_home_page.check_peoplepower_is_displayed
    tensor_home_page.reporter.log_step(f'#Проверка: блок "Сила в людях" отображается')

    tensor_about_page = tensor_home_page.findclick_readmore_button()

    assert tensor_about_page.check_current_url('https://tensor.ru/about'), 'Текущий url не соответствует https://tensor.ru/about'
    tensor_about_page.reporter.log_step(f'#Проверка: текущий URL == sbis.ru/about')

    assert tensor_about_page.check_width_height_of_images(tensor_about_page.images)
    tensor_about_page.reporter.log_step(f'#Проверка: ширина и высота всех изображений корректна')
