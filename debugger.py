```python
import json
import logging
import tkinter as tk
from tkinter import messagebox, filedialog

# Ustawienia logowania
logging.basicConfig(filename='debugger.log', level=logging.INFO)

class Debugger:
    def __init__(self, data):
        self.data = data

    def display_data(self):
        return json.dumps(self.data, indent=4)

    def update_data(self, key, value):
        if key == "punkty":
            if not isinstance(value, int) or value < 0:
                raise ValueError("Punkty powinny być liczbą całkowitą nie mniejszą niż 0.")
        if key in self.data:
            self.data[key] = value
            logging.info(f"Zaktualizowano '{key}' na '{value}'")
        else:
            raise KeyError(f"Klucz '{key}' nie znajduje się w danych.")

    def add_data(self, key, value):
        if key in self.data:
            raise KeyError(f"Klucz '{key}' już istnieje.")
        self.data[key] = value
        logging.info(f"Dodano '{key}' z wartością '{value}'")

    def delete_data(self, key):
        if key in self.data:
            del self.data[key]
            logging.info(f"Usunięto klucz '{key}'")
        else:
            raise KeyError(f"Klucz '{key}' nie występuje.")

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.data, file)
        logging.info(f"Dane zapisane w pliku '{filename}'.")

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            self.data = json.load(file)
        logging.info(f"Dane wczytane z pliku '{filename}'.")

class DebuggerGUI:
    def __init__(self, master, debugger):
        self.master = master
        self.master.title("Debugger")
        self.debugger = debugger

        self.label =
    
