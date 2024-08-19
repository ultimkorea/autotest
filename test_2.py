from pages.SbisPageRegion import SbisPageRegion


def test_check_region_partner(browser, reporter):
    """
    Тестовое задание СБИС (Автотестирование) №2
    1. Проверка текущего региона (МОСКВА)
    2. Проверка адресной строки, title и элемента выбора региона на наличие искомого региона
    3. Проверка списка партнеров
    """
    sbis_page = SbisPageRegion(browser, reporter)
    sbis_page.open_start_url()

    sbis_page.findclick_contacts_button()
    partners = sbis_page.get_partner_list(old=True)

    assert sbis_page.check_moscow_region, 'Текущий регион некорректный (!= Москва)'
    sbis_page.reporter.log_step(f'#Проверка: текущий регион корректый')

    sbis_page.chooseclick_new_region()

    assert sbis_page.check_kamchatka_region, f'Не пройдена проверка текущего региона (!= Камчатский край)'
    sbis_page.reporter.log_step(f'#Проверка элемента: новый регион - Камчатский край')
    assert sbis_page.check_kamchatka_url, f'Не пройдена проверка url'
    sbis_page.reporter.log_step(f'#Проверка url: новый регион - Камчатский край')
    assert sbis_page.check_kamchatka_title, f'Не пройдена проверка title'
    sbis_page.reporter.log_step(f'#Проверка title: новый регион - Камчатский край')

    new_partners = sbis_page.get_partner_list()

    assert sbis_page.matches_partners(partners), f'Изначальный список партнеров: {partners}, новый список: {new_partners}'
    sbis_page.reporter.log_step(f'#Проверка: списки партнеров отличаются')





