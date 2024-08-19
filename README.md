# Тестовое задание в автотестирование (tensor)

### autotests on Github Actions:
[![Tests](https://github.com/ultimkorea/autotest/actions/workflows/autotests.yml/badge.svg)](https://github.com/ultimkorea/autotest/actions/workflows/autotests.yml)
### allure-reports on Github Pages
https://ultimkorea.github.io/autotest/ (не успел разобраться с джобой: когда один из тестов = Failed, пока они в историю не пишутся)

### Установка и запуск тестов
1. Склонировать репозиторий
2. Выполнить: `pip install -r requirements.txt`
3. Запустить тесты командой: `pytest`
   
Дополнительно доступно построение отчетов в Allure.
1. Выполнить: `pytest --allure-dir=/path/to/reports`
2. Для просмотра отчетов: `allure serve /path/to/reports`


