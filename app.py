from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import smtplib
from email.message import EmailMessage
import re
import html
import os

# Инициализируем приложение. Указываем папки для статики и шаблонов
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# ==============================================================
# НАСТРОЙКИ ПОЧТЫ (ВНИМАТЕЛЬНО ЗАПОЛНИ СВОИ ДАННЫЕ)
# ==============================================================
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
MY_EMAIL = "zeqnmap@gmail.com"
MY_PASSWORD = "gcgcjqujstjypybj"


def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


def is_valid_phone(phone):
    pattern = r'^\+?[\d\s\-\(\)]{7,20}$'
    return re.match(pattern, phone) is not None


# ==============================================================
# НОВЫЙ РОУТ: РАЗДАЧА HTML-САЙТА
# ==============================================================
@app.route('/')
def home():
    # Эта функция берет index.html из папки templates и показывает его пользователю
    return render_template('index.html')


# ==============================================================
# РОУТ ДЛЯ ОТПРАВКИ ПИСЕМ
# ==============================================================
@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Пустой запрос'}), 400

        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        client_email = data.get('email', '').strip()
        message = data.get('message', '').strip()

        if not all([name, phone, client_email, message]):
            return jsonify({'error': 'Пожалуйста, заполните все поля.'}), 400

        if len(name) > 50 or len(message) > 2000:
            return jsonify({'error': 'Превышен лимит символов.'}), 400

        if not is_valid_email(client_email):
            return jsonify({'error': 'Некорректный Email.'}), 400

        if not is_valid_phone(phone):
            return jsonify({'error': 'Некорректный телефон.'}), 400

        safe_name = html.escape(name)
        safe_phone = html.escape(phone)
        safe_email = html.escape(client_email)
        safe_message = html.escape(message)

        # ИСПОЛЬЗУЕМ СОВРЕМЕННЫЙ КЛАСС EmailMessage
        msg = EmailMessage()
        msg['From'] = MY_EMAIL
        msg['To'] = MY_EMAIL
        msg['Subject'] = f"🚀 Новая заявка на английский от {safe_name}"

        body = f"Имя: {safe_name}\nТелефон: {safe_phone}\nEmail: {safe_email}\n\nСообщение:\n{safe_message}"
        msg.set_content(body)

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(MY_EMAIL, MY_PASSWORD)
        server.send_message(msg)
        server.quit()

        return jsonify({'success': True, 'message': 'Письмо отправлено!'}), 200

    except Exception as e:
        print(f"Ошибка: {e}")
        return jsonify({'error': 'Ошибка сервера.'}), 500


if __name__ == '__main__':
    # Оставляем так для локального теста. На сервере это запустится через gunicorn
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))