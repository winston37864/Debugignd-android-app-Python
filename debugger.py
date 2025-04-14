import json
import logging
import tkinter as tk
from tkinter import messagebox, filedialog

# Ustawienia logowania
logging.basicConfig(filename='debugger.log', level=logging.INFO)

class DataDebugger:
    def __init__(self, data):
        self.data = data

    def display_data(self):
        return json.dumps(self.data, indent=4)

    def update_data(self, key, value):
        if key == "punkty":
            if not isinstance(value, int) or value < 0:
                raise ValueError("Wartość 'punkty' musi być liczbą całkowitą nie mniejszą niż 0.")
        if key in self.data:
            self.data[key] = value
            logging.info(f"Zaktualizowano '{key}' na '{value}'")
        else:
            raise KeyError(f"Klucz '{key}' nie istnieje w danych.")

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
        try:
            with open(filename, 'w') as file:
                json.dump(self.data, file, indent=4)
            logging.info(f"Dane zapisane do pliku '{filename}'.")
            return True
        except Exception as e:
            logging.error(f"Błąd podczas zapisywania do pliku '{filename}': {e}")
            return False

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                self.data = json.load(file)
            logging.info(f"Dane wczytane z pliku '{filename}'.")
            return True
        except FileNotFoundError:
            logging.error(f"Nie znaleziono pliku '{filename}'.")
            return False
        except json.JSONDecodeError as e:
            logging.error(f"Błąd dekodowania JSON z pliku '{filename}': {e}")
            return False
        except Exception as e:
            logging.error(f"Inny błąd podczas wczytywania z pliku '{filename}': {e}")
            return False

class DataDebuggerGUI:
    def __init__(self, master, debugger):
        self.master = master
        self.master.title("Debugger Danych")
        self.debugger = debugger

        self.data_display = DataDisplayFrame(self.master, self.debugger)
        self.data_manipulation = DataManipulationFrame(self.master, self.debugger, self.data_display.refresh)
        self.file_operations = FileOperationsFrame(self.master, self.debugger, self.data_display.refresh)

        self.data_display.pack(padx=10, pady=5, fill="both", expand=True)
        self.data_manipulation.pack(padx=10, pady=5, fill="x")
        self.file_operations.pack(padx=10, pady=10, fill="x")

class DataDisplayFrame(tk.Frame):
    def __init__(self, master, debugger):
        super().__init__(master)
        self.debugger = debugger
        tk.Label(self, text="Aktualne Dane:").pack(pady=5)
        self.text_area = tk.Text(self, width=60, height=15, state=tk.DISABLED)
        self.text_area.pack(padx=5, pady=5, fill="both", expand=True)
        self.refresh()

    def refresh(self):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, self.debugger.display_data())
        self.text_area.config(state=tk.DISABLED)

class DataManipulationFrame(tk.Frame):
    def __init__(self, master, debugger, refresh_display_callback):
        super().__init__(master)
        self.debugger = debugger
        self.refresh_display = refresh_display_callback
        self._create_widgets()

    def _create_widgets(self):
        # Ramka modyfikacji
        modify_frame = tk.LabelFrame(self, text="Modyfikuj Klucz")
        modify_frame.pack(padx=5, pady=5, fill="x")
        tk.Label(modify_frame, text="Klucz:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.key_entry_modify = tk.Entry(modify_frame)
        self.key_entry_modify.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.key_entry_modify.insert(0, "np. punkty")
        self.key_entry_modify.bind("<FocusIn>", lambda e: self._clear_placeholder(self.key_entry_modify, "np. punkty"))
        self.key_entry_modify.bind("<FocusOut>", lambda e: self._set_placeholder(self.key_entry_modify, "np. punkty"))
        tk.Label(modify_frame, text="Wartość:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.value_entry_modify = tk.Entry(modify_frame)
        self.value_entry_modify.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.value_entry_modify.insert(0, "np. 200")
        self.value_entry_modify.bind("<FocusIn>", lambda e: self._clear_placeholder(self.value_entry_modify, "np. 200"))
        self.value_entry_modify.bind("<FocusOut>", lambda e: self._set_placeholder(self.value_entry_modify, "np. 200"))
        tk.Button(modify_frame, text="Zmień", command=self._modify_data).grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # Ramka dodawania
        add_frame = tk.LabelFrame(self, text="Dodaj Nowy Klucz")
        add_frame.pack(padx=5, pady=5, fill="x")
        tk.Label(add_frame, text="Nowy Klucz:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.key_entry_add = tk.Entry(add_frame)
        self.key_entry_add.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.key_entry_add.insert(0, "Nowy klucz")
        self.key_entry_add.bind("<FocusIn>", lambda e: self._clear_placeholder(self.key_entry_add, "Nowy klucz"))
        self.key_entry_add.bind("<FocusOut>", lambda e: self._set_placeholder(self.key_entry_add, "Nowy klucz"))
        tk.Label(add_frame, text="Wartość:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.value_entry_add = tk.Entry(add_frame)
        self.value_entry_add.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.value_entry_add.insert(0, "Nowa wartość")
        self.value_entry_add.bind("<FocusIn>", lambda e: self._clear_placeholder(self.value_entry_add, "Nowa wartość"))
        self.value_entry_add.bind("<FocusOut>", lambda e: self._set_placeholder(self.value_entry_add, "Nowa wartość"))
        tk.Button(add_frame, text="Dodaj", command=self._add_data).grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # Ramka usuwania
        remove_frame = tk.LabelFrame(self, text="Usuń Klucz")
        remove_frame.pack(padx=5, pady=5, fill="x")
        tk.Label(remove_frame, text="Klucz do usunięcia:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.key_entry_remove = tk.Entry(remove_frame)
        self.key_entry_remove.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.key_entry_remove.insert(0, "Klucz do usunięcia")
        self.key_entry_remove.bind("<FocusIn>", lambda e: self._clear_placeholder(self.key_entry_remove, "Klucz do usunięcia"))
        self.key_entry_remove.bind("<FocusOut>", lambda e: self._set_placeholder(self.key_entry_remove, "Klucz do usunięcia"))
        tk.Button(remove_frame, text="Usuń", command=self._remove_data).grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    def _clear_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)

    def _set_placeholder(self, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)

    def _modify_data(self):
        key = self.key_entry_modify.get()
        value_str = self.value_entry_modify.get()
        try:
            value = self._attempt_type_conversion(key, value_str)
            self.debugger.update_data(key, value)
            self.refresh_display()
            messagebox.showinfo("Sukces", f"Zaktualizowano '{key}' na '{value}'")
        except ValueError as e:
            messagebox.showerror("Błąd", str(e))
        except KeyError as e:
            messagebox.showerror("Błąd", str(e))

    def _add_data(self):
        key = self.key_entry_add.get()
        value_str = self.value_entry_add.get()
        try:
            value = self._attempt_type_conversion(key, value_str)
            self.debugger.add_data(key, value)
            self.refresh_display()
            messagebox.showinfo("Sukces", f"Dodano '{key}' z wartością '{value}'")
        except ValueError as e:
            messagebox.showerror("Błąd", str(e))
        except KeyError as e:
            messagebox.showerror("Błąd", str(e))

    def _remove_data(self):
        key = self.key_entry_remove.get()
        try:
            self.debugger.delete_data(key)
            self.refresh_display()
            messagebox.showinfo("Sukces", f"Usunięto klucz '{key}'")
        except KeyError as e:
            messagebox.showerror("Błąd", str(e))

    def _attempt_type_conversion(self, key, value_str):
        if key == "punkty":
            return int(value_str)
        try:
            return int(value_str)
        except ValueError:
            try:
                return float(value_str)
            except ValueError:
                return value_str

class FileOperationsFrame(tk.Frame):
    def __init__(self, master, debugger, refresh_display_callback):
        super().__init__(master)
        self.debugger = debugger
        self.refresh_display = refresh_display_callback
        self._create_widgets()

    def _create_widgets(self):
        save_button = tk.Button(self, text="Zapisz do Pliku", command=self._save_data)
        save_button.pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        load_button = tk.Button(self, text="Wczytaj z Pliku", command=self._load_data)
        load_button.pack(side=tk.RIGHT, padx=5, fill="x", expand=True)

    def _save_data(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json",
                                                filetypes=[("Pliki JSON", "*.json"),
                                                           ("Wszystkie pliki", "*.*")])
        if filename:
            if self.debugger.save_to_file(filename):
                messagebox.showinfo("Sukces", f"Dane zapisano do '{filename}'.")
            else:
                messagebox.showerror("Błąd", f"Wystąpił problem podczas zapisywania do '{filename}'. Sprawdź logi.")

    def _load_data(self):
        filename = filedialog.askopenfilename(defaultextension=".json",
                                              filetypes=[("Pliki JSON", "*.json"),
                                                         ("Wszystkie pliki", "*.*")])
        if filename:
            if self.debugger.load_from_file(filename):
                self.refresh_display()
                messagebox.showinfo("Sukces", f"Dane wczytano z '{filename}'.")
            else:
                messagebox.showerror("Błąd", f"Wystąpił problem podczas wczytywania z '{filename}'. Sprawdź logi.")

# Przykładowe dane początkowe
initial_data = {
    "nazwa_użytkownika":
