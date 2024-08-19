from pages.SbisPageImages import SbisPageImages


def test_check_width_height_of_images(browser, reporter):
    """
    Тестовое задание СБИС (Автотестирование) №1
    1. Проверка наличия блока Сила в людях
    2. Проверерка текущего URL после перехода из блока Сила в людях
    3. Проверка-сравнение высоты и ширины изображений на странице /about
    """

    sbis_page = SbisPageImages(browser, reporter)
    sbis_page.open_start_url()
    sbis_page.findclick_contacts_button()
    sbis_page.findclick_logo_image()

    assert sbis_page.check_peoplepower_is_displayed
    reporter.log_step(f'#Проверка: блок "Сила в людях" отображается')

    sbis_page.findclick_readmore_button()

    assert sbis_page.check_current_url, 'Текущий url не соответствует sbis.ru/about'
    reporter.log_step(f'#Проверка: текущий URL == sbis.ru/about')

    assert sbis_page.check_width_height_of_images(sbis_page.images)
    reporter.log_step(f'#Проверка: ширина и высота всех изображений корректна')
