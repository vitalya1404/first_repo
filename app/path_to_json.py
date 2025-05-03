import os

script_dir = os.path.dirname(os.path.abspath(__file__))# Получаем путь к директории текущего скрипта
parent_dir = os.path.dirname(script_dir)# Переходим на уровень выше
path_to_json = os.path.join(parent_dir, 'students.json')# Получаем путь к JSON