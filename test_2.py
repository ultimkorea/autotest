from pages.sbis_page import SbisHome

def test_check_region_partner(browser):
    """
    Тестовое задание СБИС (Автотестирование) №2
    1. Проверка текущего региона (МОСКВА)
    2. Проверка адресной строки, title и элемента выбора региона на наличие искомого региона
    3. Проверка списка партнеров
    """
    sbisHome_page = SbisHome(browser)
    sbisHome_page.open_start_url()

    sbis_contacts_page = sbisHome_page.findclick_contacts_button()
    old_partners = sbis_contacts_page.get_partner_list(old=True)

    assert sbis_contacts_page.check_moscow_region, 'Текущий регион некорректный (!= Москва)'
    sbis_contacts_page.reporter.log_step(f'#Проверка: текущий регион корректый')

    sbis_contacts_page.chooseclick_new_region()

    assert sbis_contacts_page.check_kamchatka_region, f'Не пройдена проверка текущего региона (!= Камчатский край)'
    sbis_contacts_page.reporter.log_step(f'#Проверка элемента: новый регион - Камчатский край')
    assert sbis_contacts_page.check_kamchatka_url, f'Не пройдена проверка url'
    sbis_contacts_page.reporter.log_step(f'#Проверка url: новый регион - Камчатский край')
    assert sbis_contacts_page.check_kamchatka_title, f'Не пройдена проверка title'
    sbis_contacts_page.reporter.log_step(f'#Проверка title: новый регион - Камчатский край')

    new_partners = sbis_contacts_page.get_partner_list()

    assert sbis_contacts_page.matches_partners(old_partners), f'Изначальный список партнеров: {old_partners}, новый список: {new_partners}'
    sbis_contacts_page.reporter.log_step(f'#Проверка: списки партнеров отличаются')





