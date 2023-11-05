import data_io as io
import time
from datetime import datetime

data = io.Crud('data.json')


def get_input_from_user(message):
    return input(message)


def main_menu():
    while True:
        print('\n*** Главное меню ***\n')
        print('L – Отобразить список заметок (в порядке добавления)')
        print('S – Отобразить список заметок (отсортированный по дате, по убыванию)')
        print('O – Открыть заметку')
        print('A – Добавить заметку')
        print('U – Изменить заметку')
        print('D – Удалить заметку')
        print('Q – Выйти из программы\n')
        selection = input('Введите команду: ')
        match selection:
            case 'A' | 'a':
                uid = data.get_the_unique_id()
                entry_data_to_add = {
                    "Header": input('Введите заголовок заметки: '),
                    "Body": input('Введите тело заметки: '),
                    "Timestamp": int(time.time())
                }
                current_data = data.read_json_data_from_file()
                if current_data:
                    current_data[uid] = entry_data_to_add
                    data.write_json_data_to_file(current_data)
                else:
                    data.write_json_data_to_file({uid: entry_data_to_add})
                print('\n>>> Заметка успешно сохранена!')
            case 'O' | 'o':
                single_entry_id = input('Введите номер заметки, которую нужно отобразить: ')
                try:
                    single_entry_id = int(single_entry_id)
                except ValueError:
                    single_entry_id = 0
                single_entry = data.get_single_entry(single_entry_id)
                if single_entry:
                    print('\nID: ' + str(single_entry_id))
                    for key, value in single_entry.items():
                        if key == 'Timestamp':
                            dt_obj = datetime.fromtimestamp(value).strftime('%d-%m-%Y %H:%M:%S')
                            print('Дата и время публикации: ' + str(dt_obj))
                        elif key == 'Header':
                            print('Заголовок: ' + str(value))
                        elif key == 'Body':
                            print('Тело: ' + str(value))
                else:
                    print('\n>>> Заметки с ID ' + str(single_entry_id) + ' не существует')
            case 'L' | 'l':
                current_data = data.read_json_data_from_file()
                if current_data:
                    for uid, entry in current_data.items():
                        print('\nID: ' + uid)
                        for key, value in entry.items():
                            if key == 'Timestamp':
                                date_time = datetime.fromtimestamp(value).strftime('%d-%m-%Y %H:%M:%S')
                                print('Дата и время публикации: ' + str(date_time))
                            elif key == 'Header':
                                print('Заголовок: ' + str(value))
                else:
                    print('\n>>> Заметки отсутствуют')
            case 'D' | 'd':
                entry_id_to_delete = input('Введите номер заметки, которую нужно удалить: ')
                try:
                    entry_id_to_delete = int(entry_id_to_delete)
                except ValueError:
                    entry_id_to_delete = 0
                if data.single_entry_exists(entry_id_to_delete):
                    data.delete_single_entry(entry_id_to_delete)
                    print('\n>>> Заметка удалена')
                else:
                    print('\n>>> Заметки с ID ' + str(entry_id_to_delete) + ' не существует')
            case 'U' | 'u':
                entry_id_to_update = input('Введите номер заметки, которую нужно обновить: ')
                try:
                    entry_id_to_update = int(entry_id_to_update)
                except ValueError:
                    entry_id_to_update = 0
                if data.single_entry_exists(entry_id_to_update):
                    entry_to_update = {
                        "Header": input('Введите новый заголовок заметки: '),
                        "Body": input('Введите новое тело заметки: '),
                        "Timestamp": int(time.time())
                    }
                    data.update_single_entry(entry_id_to_update, entry_to_update)
                    print('\n>>> Заметка обновлена')
                else:
                    print('\n>>> Заметки с ID ' + str(entry_id_to_update) + ' не существует')
            case 'S' | 's':
                ordered_dict = data.sort_by_date_time()
                for uid, entries in ordered_dict.items():
                    print('\nID: ' + uid)
                    for k, v in entries.items():
                        if k == 'Timestamp':
                            dt_obj = datetime.fromtimestamp(v).strftime('%d-%m-%Y %H:%M:%S')
                            print('Дата и время публикации: ' + str(dt_obj))
                        elif k == 'Header':
                            print('Заголовок: ' + str(v))
            case 'Q' | 'q':
                return False
            case _:
                print('\n>>> Введена неверная команда')
                return main_menu()
