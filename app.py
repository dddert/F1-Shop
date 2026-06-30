import os
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Путь к файлу, где будут храниться заявки
ORDERS_FILE = os.path.join(os.path.dirname(__file__), 'orders.json')

F1_DATA = {
    "name": "NERO BLITZ F1-26",
    "tagline": "CUTTING EDGE AERODYNAMICS. ZERO COMPROMISE.",
    "price": 18500000,
    "power": 1070,
    "top_speed": 362,
    "weight": 798,
    "chassis": "Монокок из углеродного волокна военного класса с сотовой структурой Nomex.",
    "engine": "1.6-литровый V6 с турбонаддувом и интегрированными мотор-генераторами MGU-K и MGU-H."
}


# Помощник для чтения заявок
def read_orders():
    if not os.path.exists(ORDERS_FILE):
        return []
    try:
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []


# Помощник для записи заявок
def write_orders(orders):
    with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(orders, f, ensure_ascii=False, indent=4)


@app.route('/')
def index():
    return render_template('index.html', car=F1_DATA)


@app.route('/preorder')
def preorder_page():
    return render_template('preorder.html', car=F1_DATA)


# API для приема заявок
@app.route('/api/preorder', methods=['POST'])
def preorder_api():
    data = request.get_json()

    # Читаем текущие, добавляем новую
    orders = read_orders()
    new_order = {
        "id": len(orders) + 1,
        "name": data.get('name'),
        "lastname": data.get('lastname'),
        "email": data.get('email'),
        "phone": data.get('phone'),
        "package": data.get('package'),
        "color": data.get('color'),
        "engineer": "Да" if data.get('engineer') else "Нет"
    }
    orders.append(new_order)
    write_orders(orders)

    return jsonify({
        "status": "success",
        "message": "ВАШ ЗАПРОС УСПЕШНО ПРИНЯТ. Квантовый зашифрованный контракт отправлен на ваш Email. Менеджер свяжется с вами через Secure Line."
    })


# Простая админка для просмотра заявок
@app.route('/admin-panel')
def admin_panel():
    orders = read_orders()
    return render_template('admin.html', orders=orders)


if __name__ == '__main__':
    app.run(debug=True)