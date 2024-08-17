from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Erlaubt Cross-Origin-Requests (CORS), falls die App von einem anderen Server aus aufgerufen wird

# Beispiel-Router-Instanz
class HyperlinkRouter:
    def __init__(self):
        self.devices = []
        self.smart_home_devices = []
        self.nas_storage = {}

    def add_device(self, device_name):
        self.devices.append(device_name)
        return f"Gerät '{device_name}' hinzugefügt."

    def remove_device(self, device_name):
        if device_name in self.devices:
            self.devices.remove(device_name)
            return f"Gerät '{device_name}' entfernt."
        else:
            return f"Gerät '{device_name}' nicht gefunden."

    def get_devices(self):
        return self.devices

    def save_file_to_nas(self, file_path):
        if os.path.exists(file_path):
            file_name = os.path.basename(file_path)
            with open(file_path, 'rb') as file:
                self.nas_storage[file_name] = file.read()
            return f"Datei '{file_name}' ins NAS gespeichert."
        else:
            return f"Datei '{file_path}' nicht gefunden."

    def get_nas_files(self):
        return list(self.nas_storage.keys())

# Beispiel-Router-Instanz initialisieren
router = HyperlinkRouter()

# Indexseite
@app.route('/')
def index():
    return render_template('index.html')

# Geräteverwaltung
@app.route('/add_device', methods=['POST'])
def add_device():
    device_name = request.form['device_name']
    message = router.add_device(device_name)
    return jsonify({'message': message})

@app.route('/remove_device', methods=['POST'])
def remove_device():
    device_name = request.form['device_name']
    message = router.remove_device(device_name)
    return jsonify({'message': message})

@app.route('/get_devices', methods=['GET'])
def get_devices():
    devices = router.get_devices()
    return jsonify({'devices': devices})

# NAS Verwaltung
@app.route('/save_to_nas', methods=['POST'])
def save_to_nas():
    file_path = request.form['file_path']
    message = router.save_file_to_nas(file_path)
    return jsonify({'message': message})

@app.route('/get_nas_files', methods=['GET'])
def get_nas_files():
    files = router.get_nas_files()
    return jsonify({'files': files})

if __name__ == '__main__':
    app.run(debug=True)
