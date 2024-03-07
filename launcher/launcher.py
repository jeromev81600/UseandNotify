import psutil
import subprocess
import time

# Ecoute du processus correspondant au Launcher de StarCitizen
def check_RSILauncher_process():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'RSI Launcher.exe':
            return True
    return False

# Lancement de mon application Flask en arrière-plan
def start_flask_app():
    python_executable = r'C:\Users\jerom\AppData\Local\Programs\Python\Python312\python.exe'
    flask_script = r'C:\Users\jerom\Documents\Divers exo\python\UseandNotify\main.py'
    subprocess.Popen([python_executable, flask_script])
