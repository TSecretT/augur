import json
import time

class Database:
    def __init__(self, filename):
        self.filename = filename
    
    def get(self, as_list=False):
        with open(self.filename) as f:
            data = json.load(f)
        if as_list:
            return [data[match_id] for match_id in data]
        else:
            return data

    def save(self, data: object):
        with open(self.filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def set_one(self, key, obj):
        data = self.get()
        data[key] = obj
        self.save(data)

    def set_many(self, keys: list, objs: list) -> None:
        start = time.time()
        data = self.get()
        for key, obj in zip(keys, objs):
            data[key] = obj
        self.save(data)
        print(f"DB saved in {round(time.time()-start, 4)} seconds")
    
    def find(self, key: str) -> object:
        data = self.get()
        if key in data:
            return data[key]

    def filter(self, key, value):
        data = self.get()
        matches = []
        for match_id in data:
            if (key in data[match_id]) and (data[match_id][key] == value):
                matches.append(data[match_id])
            elif key not in data[match_id] and value is None:
                matches.append(data[match_id])
        return matches

    def len(self) -> int:
        return len(self.get())

    def clear(self) -> None:
        self.save({})
