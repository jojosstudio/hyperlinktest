import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sqlite3

class SetupWizard:
    def __init__(self, root):
        self.root = root
        self.root.title("Setup Wizard")
        self.root.geometry("600x400")
        self.root.configure(bg='#E0E0E0')

        self.step = 1
        self.setup_steps = [
            {"title": "Welcome", "message": "Was soll ihr Wlan name sein?"},
            {"title": "Step 1", "message": "Was ist ihr Wlan Passwort?:"},
            {"title": "Step 2", "message": "Was ist die Wlan Stärke"},
            {"title": "Step 3", "message": "Was ist ihr anbieter:"},
        ]

        self.setup_variables = {
            "ssid": tk.StringVar(),
            "password": tk.StringVar(),
            "wifi_standard": tk.StringVar(),
            "anb": tk.StringVar()
        }

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="Setup Wizard", font=("Arial", 20), background='#E0E0E0').pack(pady=10)

        ttk.Label(self.root, text=self.setup_steps[self.step - 1]["message"], background='#E0E0E0').pack(pady=10)

        if self.step == 1:
            ttk.Entry(self.root, textvariable=self.setup_variables["ssid"]).pack()
        elif self.step == 2:
            ttk.Entry(self.root, textvariable=self.setup_variables["password"], show='*').pack()
        elif self.step == 3:
            wifi_standards = ["Wi-Fi 4", "Wi-Fi 5", "Wi-Fi 6", "Wi-Fi 6e"]
            ttk.Combobox(self.root, textvariable=self.setup_variables["wifi_standard"], values=wifi_standards).pack()
        elif self.step == 4:
            ttk.Entry(self.root, textvariable=self.setup_variables["anb"]).pack()

        ttk.Button(self.root, text="Next", command=self.next_step).pack(pady=10)

    def next_step(self):
        if self.step == 1:
            self.step += 1
        elif self.step == 2:
            self.step += 1
        elif self.step == 3:
            self.step += 1
        elif self.step == 4:
            self.step += 1
            if self.step > len(self.setup_steps):
                self.complete_setup()

        if self.step <= len(self.setup_steps):
            self.refresh_ui()

    def refresh_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        if self.step <= len(self.setup_steps):
            self.create_widgets()

    def complete_setup(self):
        ssid = self.setup_variables["ssid"].get()
        password = self.setup_variables["password"].get()
        wifi_standard = self.setup_variables["wifi_standard"].get()
        anbieter = self.setup_variables["anb"].get()

        # Zeige eine Info-Box mit den eingegebenen Informationen
        messagebox.showinfo("Setup Completed", f"WiFi Configuration:\nSSID: {ssid}\nPassword: {password}\nStandard: {wifi_standard}\nAnbieter: {anbieter}")

        # Speichern der Daten in der SQLite-Datenbank
        self.save_to_database(ssid, password, wifi_standard, anbieter)

        # Run test.py
        subprocess.Popen(["python", "test.py"])

        # Schließe das Setup-Fenster
        self.root.destroy()

    def save_to_database(self, ssid, password, wifi_standard, anbieter):
        # Verbindung zur SQLite-Datenbank herstellen (wird automatisch erstellt, falls nicht vorhanden)
        conn = sqlite3.connect('setup_data.db')
        c = conn.cursor()

        # Erstelle eine Tabelle, falls sie noch nicht existiert
        c.execute('''CREATE TABLE IF NOT EXISTS wifi_config 
                     (ssid TEXT, password TEXT, wifi_standard TEXT, anbieter TEXT)''')

        # Füge die eingegebenen Daten in die Tabelle ein
        c.execute("INSERT INTO wifi_config (ssid, password, wifi_standard, anbieter) VALUES (?, ?, ?, ?)",
                  (ssid, password, wifi_standard, anbieter))

        # Änderungen speichern und Verbindung schließen
        conn.commit()
        conn.close()

def main():
    root = tk.Tk()
    app = SetupWizard(root)
    root.mainloop()

if __name__ == "__main__":
    main()
