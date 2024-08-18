from pages.SbisPageRegion import SbisPageRegion


def test_checkRegionPartners(browser, reporter):
    """
    Тестовое задание СБИС (Автотестирование) №2
    1. Проверка текущего региона (МОСКВА)
    2. Проверка адресной строки, title и элемента выбора региона на наличие искомого региона
    3. Проверка списка партнеров
    """
    sbis_page = SbisPageRegion(browser, reporter)
    sbis_page.open_start_url()

    sbis_page.findclick_contacts_button()
    partners = sbis_page.get_partner_list()

    assert sbis_page.check_moscow_region
    sbis_page.reporter.log_step(f'#Проверка: текущий регион корректый')

    sbis_page.region_click()
    sbis_page.chooseclick_new_region()

    assert sbis_page.check_kamchatka_region
    sbis_page.reporter.log_step(f'#Проверка элемента: новый регион - Камчатский край')
    assert sbis_page.check_kamchatka_url
    sbis_page.reporter.log_step(f'#Проверка url: новый регион - Камчатский край')
    assert sbis_page.check_kamchatka_title
    sbis_page.reporter.log_step(f'#Проверка title: новый регион - Камчатский край')

    new_partners = sbis_page.get_partner_list()

    assert sbis_page.matches_partners(partners, new_partners)
    sbis_page.reporter.log_step(f'#Проверка: списки партнеров отличаются')





