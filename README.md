# Тестовое задание в автотестирование (tensor)

### Текущий статус тестов на Github Actions:
[![Tests](https://github.com/ultimkorea/autotest/actions/workflows/autotests.yml/badge.svg)](https://github.com/ultimkorea/autotest/actions/workflows/autotests.yml)

### Установка и запуск тестов
1. Склонировать репозиторий
2. Выполнить: `pip install -r requirements.txt`
3. Запустить тесты командой: `pytest`
   
Дополнительно доступно построение отчетов в Allure.
1. Выполнить: `pytest --allure-dir=/path/to/reports`
2. Для просмотра отчетов: `allure serve /path/to/reports`
