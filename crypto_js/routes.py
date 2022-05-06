from crypto_js import app
from flask import render_template, jsonify, request
from crypto_js.errors import CONNECT_ERROR, APIError
from crypto_js.models import CryptoValueModels, Database_inquiry
import sqlite3
from decimal import Decimal
import json


ruta_db = app.config['BB_DD']
data_manager = Database_inquiry(ruta_db)

apikey = app.config['API_KEY']

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/api/v1/trading/<string:crypto_from>/<string:crypto_to>/<float:amount_from>", methods=['GET'])
def trading(crypto_from,crypto_to, amount_from):
    crypto_value = CryptoValueModels(apikey, crypto_from, crypto_to)
    balance = crypto_value.checkBalance(crypto_from)

    try:
        if balance or crypto_from == 'EUR':
            rate = crypto_value.calculate_rate(amount_from)
            return {
                "status": "success",
                "data": {
                    "trading": rate
                    }
            }
        else:
            return {
                    'status': 'error',
                    'message': 'Not Balance'
                    }
    except Exception as e:
        print(e)
        return {'status': 'error', 'message': 'Ha fallado coinapi'}, 400    


@app.route("/api/v1/save_exchange", methods=["POST"])
def save_exchange():
    data = json.loads(request.data)
    date= Database_inquiry.date_now()
    time = Database_inquiry.time_now()
    
    print(date,time,data)

    try:
        data_manager.save_data((date,
                                time,
                                data['crypto_from'], 
                                data['amount_from'], 
                                data['crypto_to'], 
                                data['amount_to'],
                                 ))
        return {'status': 'success'}, 201
    except sqlite3.Error as e:

        return {'status': 'error', 'message': str(e)}, 400


@app.route("/api/v1/trading_history")
def trading_history():   
    try:
        data = data_manager.get_data()
        return jsonify(data)
    
    except sqlite3.Error as e:

        return {'status': 'error', 'message': str(e)}, 400

@app.route("/api/v1/wallet", methods=['GET'])
def get_wallet():   


        allCurrencies = data_manager.getAllCurrencies()
        balanceToTotal = data_manager.getBalanceToTotal()
        balanceFromTotal = data_manager.getBalanceFromTotal()

        wallet = []
        for currency in allCurrencies:
            balanceAuxTo = [p for p in balanceToTotal if p['crypto_to'] == currency['crypto']] or [{'amount_to': 0}]
            balanceAuxFrom = [p for p in balanceFromTotal if p['crypto_from'] == currency['crypto']] or [{'amount_from': 0}]
            total = balanceAuxTo[0]['amount_to'] - balanceAuxFrom[0]['amount_from']
            wallet.append({'crypto': currency['crypto'], 'amount': total})
        
        print('AUX', wallet)

        invertido = [p for p in wallet if p['crypto'] == 'EUR'] or [{'amount': 0, 'crypto': 'EUR'}]

        value = 0.0
        for currentWallet in wallet:
            if currentWallet['crypto'] != 'EUR':
                model = CryptoValueModels(apikey, currentWallet['crypto'], 'EUR')
                print(currentWallet['amount'])
                value = value + model.calculate_rate(currentWallet['amount'])

        print('VALUE', value)
        return {}

