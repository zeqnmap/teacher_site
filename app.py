from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import smtplib
from email.message import EmailMessage
import re
import html
import os
from dotenv import load_dotenv

load_dotenv()

# Инициализируем приложение. Указываем папки для статики и шаблонов
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

@app.route('/')
def home():
    # Эта функция берет index.html из папки templates и показывает его пользователю
    return render_template('index.html')



if __name__ == '__main__':
    # Оставляем так для локального теста. На сервере это запустится через gunicorn
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))