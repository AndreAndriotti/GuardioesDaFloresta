import json

class JSONFileHandler:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = self.LoadData()

    def LoadData(self):
        try:
            with open(self.file_name, 'r') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            return {}
    
    def get(self, key):
        return self.data.get(key, None)

    def set(self, key, value):
        self.data[key] = value
        with open(self.file_name, 'w') as file:
            json.dump(self.data, file, indent=4)
