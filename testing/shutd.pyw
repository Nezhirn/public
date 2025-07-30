from flask import Flask
import os

app = Flask(__name__)

@app.route('/shutdown', methods=['POST'])
def shutdown():
    os.system('shutdown /s /t 1')  # Команда для выключения компьютера в Windows
    return 'Shutting down...'

if __name__ == '__main__':
    # Запускаем веб-сервер, слушающий на всех IP-адресах (0.0.0.0) и на порту 5000
    app.run(host='0.0.0.0', port=8080)