from pages.sbis_page import SbisHome

def test_plugin_size(browser):
    """
    Тестовое задание СБИС (Автотестирование) №3
    1. Переходить по ссылке Скачать локальные версии
    2. Извлекаем ссылку и делаем head запрос для получения Content-Length == size of file
    3. Сверяем ожидаемый и реальный размер файла
    """

    sbis_home_page = SbisHome(browser)
    sbis_home_page.open_start_url()

    downloads_page = sbis_home_page.findclick_download_page()

    filesize = downloads_page.get_filesize_from_head_request()

    plugin_plan_size = downloads_page.plugin_plan_size
    plugin_fact_size = downloads_page.plugin_fact_size(filesize)
    assert plugin_plan_size == plugin_fact_size, f'НЕ СОВПАДАЕТ РАЗМЕР ФАЙЛА. Ожидаемый размер: {plugin_plan_size}, реальный: {plugin_fact_size}'
    downloads_page.reporter.log_step(f'#Проверка: размер файла совпадает с заявленным')
