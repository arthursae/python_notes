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
                # Add a new entry
                uid = data.get_the_unique_id()
                header = input('Введите заголовок заметки: ')
                while header == "":
                    print('>>> Заголовок не должен быть пустым!')
                    header = input('Введите заголовок заметки: ')
                body = input('Введите тело заметки: ')
                while body == "":
                    print('>>> Тело заметки не должно быть пустым!')
                    body = input('Введите тело заметки: ')
                entry_data_to_add = {
                    "Header": header,
                    "Body": body,
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
                # Display a single entry by ID
                single_entry_id = input('Введите ID номер заметки, которую нужно отобразить: ')
                while single_entry_id == "":
                    print('>>> Необходимо ввести ID номер заметки!')
                    single_entry_id = input('Введите ID номер заметки: ')
                try:
                    single_entry_id = int(single_entry_id)
                except ValueError:
                    single_entry_id = 0
                if single_entry_id != 0:
                    single_entry = data.get_single_entry(single_entry_id)
                    if single_entry:
                        print('\nID: ' + str(single_entry_id))
                        dt_obj = datetime.fromtimestamp(single_entry['Timestamp']).strftime('%d-%m-%Y %H:%M:%S')
                        print('Дата и время публикации: ' + str(dt_obj))
                        print('Заголовок: ' + str(single_entry['Header']))
                        print('Тело: ' + str(single_entry['Body']))
                else:
                    print('\n>>> Заметки с ID ' + str(single_entry_id) + ' не существует')
            case 'L' | 'l':
                # List all entries ommiting body content
                current_data = data.read_json_data_from_file()
                if current_data:
                    display_entries(current_data)
                else:
                    print('\n>>> Заметки отсутствуют')
            case 'D' | 'd':
                # Delete an entry by ID
                entry_id_to_delete = input('Введите номер заметки, которую нужно удалить: ')
                while entry_id_to_delete == "":
                    print('>>> Необходимо ввести ID номер заметки!')
                    entry_id_to_delete = input('Введите ID номер заметки: ')
                try:
                    entry_id_to_delete = int(entry_id_to_delete)
                except ValueError:
                    entry_id_to_delete = 0
                if entry_id_to_delete != 0 and data.single_entry_exists(entry_id_to_delete):
                    data.delete_single_entry(entry_id_to_delete)
                    print('\n>>> Заметка удалена')
                else:
                    print('\n>>> Заметки с ID ' + str(entry_id_to_delete) + ' не существует')
            case 'U' | 'u':
                # Update an entry by ID
                entry_id_to_update = input('Введите номер заметки, которую нужно обновить: ')
                try:
                    entry_id_to_update = int(entry_id_to_update)
                except ValueError:
                    entry_id_to_update = 0
                if entry_id_to_update != 0 and data.single_entry_exists(entry_id_to_update):
                    header = input('Введите новый заголовок заметки: ')
                    while header == "":
                        print('>>> Заголовок не должен быть пустым!')
                        header = input('Введите новый заголовок заметки: ')
                    body = input('Введите новое тело заметки: ')
                    while body == "":
                        print('>>> Тело заметки не должно быть пустым!')
                        body = input('Введите новое тело заметки: ')
                    entry_to_update = {
                        "Header": header,
                        "Body": body,
                        "Timestamp": int(time.time())
                    }
                    data.update_single_entry(entry_id_to_update, entry_to_update)
                    print('\n>>> Заметка обновлена')
                else:
                    print('\n>>> Заметки с ID ' + str(entry_id_to_update) + ' не существует')
            case 'S' | 's':
                # Sort a list by timestamp in descending order
                reverse_order = True  # Change for ASC or DESC order
                ordered_dict = data.sort_by_date_time(reverse_order)
                display_entries(ordered_dict)
            case 'Q' | 'q':
                # Quit the programme
                return False
            case _:
                print('\n>>> Введена неверная команда')
                return main_menu()


def display_entries(entries):
    for uid, entry in entries.items():
        print('\nID: ' + uid)
        for k, v in entry.items():
            if k == 'Timestamp':
                dt_obj = datetime.fromtimestamp(v).strftime('%d-%m-%Y %H:%M:%S')
                print('Дата и время публикации: ' + str(dt_obj))
            elif k == 'Header':
                print('Заголовок: ' + str(v))
