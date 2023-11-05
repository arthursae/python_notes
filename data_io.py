import json
import os
from collections import OrderedDict
from operator import getitem


class Crud:
    def __init__(self, file):
        self.file = file

    def file_exist(self):
        return os.path.exists(self.file)

    def write_json_data_to_file(self, data):
        if self.file_exist():
            with open(self.file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        else:
            with open(self.file, "x", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

    def read_json_data_from_file(self):
        if not self.file_exist() or os.stat(self.file).st_size == 0:
            return False
        with open(self.file, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_the_unique_id(self):
        uid = 1  # assuming that ID counter starts from 1,2,3...
        uid_set = set()
        if self.read_json_data_from_file():
            for k, _ in self.read_json_data_from_file().items():
                uid_set.add(int(k))
        if len(uid_set) > 0:
            not_unique = True
            while not_unique:
                if uid in uid_set:
                    uid += 1
                else:
                    not_unique = False
        return uid

    def get_single_entry(self, uid):
        if self.single_entry_exists(uid):
            return self.read_json_data_from_file()[str(uid)]
        return False

    def delete_single_entry(self, uid):
        if self.single_entry_exists(uid):
            data = self.read_json_data_from_file()
            del data[str(uid)]
            self.write_json_data_to_file(data)
            return True
        return False

    def update_single_entry(self, uid, new_data):
        data = self.read_json_data_from_file()
        data[str(uid)] = new_data
        self.write_json_data_to_file(data)

    def single_entry_exists(self, uid):
        if self.read_json_data_from_file():
            data = self.read_json_data_from_file()
            for k, _ in data.items():
                if k == str(uid):
                    return True
        return False

    def sort_by_date_time(self):
        if self.read_json_data_from_file():
            data = self.read_json_data_from_file()
            ordered_dict = OrderedDict(sorted(data.items(), key=lambda x: getitem(x[1], 'Timestamp'), reverse=True))
            return ordered_dict
        return False
