import allure
from datetime import datetime
import logging

class Report:
    @staticmethod
    def log_step(step_title):
        """
        Отдельная функция для удобной записи шагов в allure и дебаг
        :param step_title: описание шага
        :return:
        """
        with allure.step(f'[{datetime.now()}]: {step_title}'):
            m = f'[{datetime.now()}]: {step_title}'
            with allure.step(m):
                logging.debug(m)