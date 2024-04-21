"""
Данный файл содержит в себе функцию, взаимодействующую с переменными
окружения, а также некоторые другие объекты конфигурации
"""

from dotenv import dotenv_values

configuration = dotenv_values()

file_extension = ('.xls', '.xlsx')
