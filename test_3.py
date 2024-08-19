from pages.SbisPagePluginDownload import SbisPluginDownloader


def test_plugin_size(browser, reporter):
    """
    Тестовое задание СБИС (Автотестирование) №3
    1. Переходить по ссылке Скачать локальные версии
    2. Извлекаем ссылку и скачиваем файл
    3. Сверяем ожидаемый и реальный размер файла
    """

    sbis_page = SbisPluginDownloader(browser, reporter)
    sbis_page.open_start_url()
    sbis_page.findclick_download_page()

    filesize = sbis_page.get_filesize_from_head_request()

    plugin_plan_size = sbis_page.plugin_plan_size
    plugin_fact_size = sbis_page.plugin_fact_size(filesize)
    assert plugin_plan_size == plugin_fact_size, f'НЕ СОВПАДАЕТ РАЗМЕР ФАЙЛА. Ожидаемый размер: {plugin_plan_size}, реальный: {plugin_fact_size}'
    reporter.log_step(f'#Проверка: размер файла совпадает с заявленным')
