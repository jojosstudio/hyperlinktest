import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

class HyperlinkRouter:
    def __init__(self):
        self.devices = []
        self.smart_home_devices = []
        self.network_settings = {
            "ssid": "Hyperlink_WiFi",
            "password": "password123",
            "wifi_standard": "Wi-Fi 6e"
        }
        self.nas_storage = {}
        self.display_message = "Hyperlink Menu"
        self.chatgpt_assistant = ChatGPTAssistant()

    def add_device(self, device_name):
        self.devices.append(device_name)
        print(f"Device '{device_name}' added.")

    def remove_device(self, device_name):
        if device_name in self.devices:
            self.devices.remove(device_name)
            print(f"Device '{device_name}' removed.")
        else:
            print(f"Device '{device_name}' not found.")

    def add_smart_home_device(self, device_name):
        self.smart_home_devices.append(device_name)
        print(f"Smart Home Device '{device_name}' added.")

    def remove_smart_home_device(self, device_name):
        if device_name in self.smart_home_devices:
            self.smart_home_devices.remove(device_name)
            print(f"Smart Home Device '{device_name}' removed.")
        else:
            print(f"Smart Home Device '{device_name}' not found.")

    def set_display_message(self, message):
        self.display_message = message
        print(f"Display message set to: '{message}'")

    def save_file_to_nas(self, file_path):
        if os.path.exists(file_path):
            file_name = os.path.basename(file_path)
            with open(file_path, 'rb') as file:
                self.nas_storage[file_name] = file.read()
            print(f"File '{file_name}' saved to NAS.")
        else:
            print(f"File '{file_path}' not found.")

    def get_file_from_nas(self, file_name):
        if file_name in self.nas_storage:
            return self.nas_storage[file_name]
        else:
            print(f"File '{file_name}' not found in NAS.")
            return None

    def interact_with_assistant(self, user_input):
        response = self.chatgpt_assistant.respond(user_input)
        return response

class ChatGPTAssistant:
    def __init__(self):
        pass  # Initialize any necessary parameters here

    def respond(self, user_input):
        # Here, you'd integrate with the actual ChatGPT API
        # For demonstration purposes, we'll just echo the input
        return f"ChatGPT Response to '{user_input}'"

class HyperlinkRouterGUI:
    def __init__(self, root, router):
        self.router = router
        self.root = root
        self.root.title("Hyperlink Router")

        # Set window size
        self.root.geometry("600x800")

        # Set background color
        self.root.configure(bg='#b9b9b9')

        # Optionally, set a background image
        self.background_image = None
        self._set_background_image('background.jpg')

        self.style = ttk.Style()
        self.style.configure('TButton', font=('Helvetica', 12), padding=10)
        self.style.configure('TLabel', font=('Helvetica', 14), background='#b9b9b9')

        self.create_widgets()
        self.update_display_message()

    def _set_background_image(self, image_path):
        if os.path.exists(image_path):
            image = Image.open(image_path)
            self.background_image = ImageTk.PhotoImage(image)
            background_label = tk.Label(self.root, image=self.background_image)
            background_label.place(relwidth=1, relheight=1)
        else:
            print(f"Background image '{image_path}' not found.")

    def create_widgets(self):
        # Display message
        self.display_label = ttk.Label(self.root, text=self.router.display_message, font=("Arial", 18))
        self.display_label.pack(pady=10)

        # Device management
        self._create_device_management_section()

        # Smart Home management
        self._create_smart_home_management_section()

        # NAS management
        self._create_nas_management_section()

        # ChatGPT Assistant
        self._create_chatgpt_assistant_section()

    def _create_device_management_section(self):
        ttk.Label(self.root, text="Device Management").pack(pady=5)
        self.device_entry = ttk.Entry(self.root)
        self.device_entry.pack()
        ttk.Button(self.root, text="Add Device", command=self.add_device).pack(pady=2)
        self.device_combobox = ttk.Combobox(self.root, values=self.router.devices)
        self.device_combobox.pack()
        ttk.Button(self.root, text="Remove Device", command=self.remove_device).pack(pady=2)
        ttk.Button(self.root, text="View Devices", command=self.view_devices).pack(pady=2)

    def _create_smart_home_management_section(self):
        ttk.Label(self.root, text="Smart Home Management").pack(pady=5)
        self.smart_home_entry = ttk.Entry(self.root)
        self.smart_home_entry.pack()
        ttk.Button(self.root, text="Add Smart Home Device", command=self.add_smart_home_device).pack(pady=2)
        self.smart_home_combobox = ttk.Combobox(self.root, values=self.router.smart_home_devices)
        self.smart_home_combobox.pack()
        ttk.Button(self.root, text="Remove Smart Home Device", command=self.remove_smart_home_device).pack(pady=2)
        ttk.Button(self.root, text="View Smart Home Devices", command=self.view_smart_home_devices).pack(pady=2)

    def _create_nas_management_section(self):
        ttk.Label(self.root, text="NAS Management").pack(pady=5)
        ttk.Button(self.root, text="Save File to NAS", command=self.save_file_to_nas).pack(pady=2)
        self.nas_combobox = ttk.Combobox(self.root, values=list(self.router.nas_storage.keys()))
        self.nas_combobox.pack()
        ttk.Button(self.root, text="Get File from NAS", command=self.get_file_from_nas).pack(pady=2)
        ttk.Button(self.root, text="View NAS Files", command=self.view_nas_files).pack(pady=2)

    def _create_chatgpt_assistant_section(self):
        ttk.Label(self.root, text="ChatGPT Assistant").pack(pady=5)
        self.assistant_entry = ttk.Entry(self.root)
        self.assistant_entry.pack()
        ttk.Button(self.root, text="Ask Assistant", command=self.ask_assistant).pack(pady=2)

    def update_display_message(self):
        self.display_label.config(text=self.router.display_message)

    def add_device(self):
        device_name = self.device_entry.get()
        if device_name:
            self.router.add_device(device_name)
            self.device_entry.delete(0, tk.END)
            self.device_combobox['values'] = self.router.devices
            messagebox.showinfo("Info", f"Device '{device_name}' added.")
        else:
            messagebox.showwarning("Warning", "Bitte geben sie ein namen ein.")

    def remove_device(self):
        device_name = self.device_combobox.get()
        if device_name:
            self.router.remove_device(device_name)
            self.device_combobox.set('')
            self.device_combobox['values'] = self.router.devices
            messagebox.showinfo("Info", f"Device '{device_name}' removed.")
        else:
            messagebox.showwarning("Warning", "Please select a device to remove.")

    def view_devices(self):
        devices = "\n".join(self.router.devices)
        messagebox.showinfo("Devices", f"Connected devices:\n{devices}")

    def add_smart_home_device(self):
        device_name = self.smart_home_entry.get()
        if device_name:
            self.router.add_smart_home_device(device_name)
            self.smart_home_entry.delete(0, tk.END)
            self.smart_home_combobox['values'] = self.router.smart_home_devices
            messagebox.showinfo("Info", f"Smart Home Device '{device_name}' added.")
        else:
            messagebox.showwarning("Warning", "Device name cannot be empty.")

    def remove_smart_home_device(self):
        device_name = self.smart_home_combobox.get()
        if device_name:
            self.router.remove_smart_home_device(device_name)
            self.smart_home_combobox.set('')
            self.smart_home_combobox['values'] = self.router.smart_home_devices
            messagebox.showinfo("Info", f"Smart Home Device '{device_name}' removed.")
        else:
            messagebox.showwarning("Warning", "Please select a smart home device to remove.")

    def view_smart_home_devices(self):
        devices = "\n".join(self.router.smart_home_devices)
        messagebox.showinfo("Smart Home Devices", f"Smart Home devices:\n{devices}")

    def save_file_to_nas(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.router.save_file_to_nas(file_path)
            self.nas_combobox['values'] = list(self.router.nas_storage.keys())
            messagebox.showinfo("Info", f"File '{os.path.basename(file_path)}' saved to NAS.")

    def get_file_from_nas(self):
        file_name = self.nas_combobox.get()
        if file_name:
            file_content = self.router.get_file_from_nas(file_name)
            if file_content:
                save_path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=file_name)
                if save_path:
                    with open(save_path, 'wb') as file:
                        file.write(file_content)
                    messagebox.showinfo("Info", f"File '{file_name}' saved to {save_path}.")
        else:
            messagebox.showwarning("Warning", "Please select a file to retrieve.")

    def view_nas_files(self):
        files = "\n".join(self.router.nas_storage.keys())
        messagebox.showinfo("NAS Files", f"Files in NAS:\n{files}")

    def ask_assistant(self):
        user_input = self.assistant_entry.get()
        if user_input:
            response = self.router.interact_with_assistant(user_input)
            self.assistant_entry.delete(0, tk.END)
            messagebox.showinfo("Assistant Response", response)

# Main function to run the application
def main():
    router = HyperlinkRouter()
    root = tk.Tk()
    app = HyperlinkRouterGUI(root, router)
    root.mainloop()

if __name__ == "__main__":
    main()
