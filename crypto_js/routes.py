from crypto_js import app
from flask import render_template, jsonify, request
from crypto_js.models import CryptoValueModels, Database_inquiry
import sqlite3
import json


ruta_db = app.config['BB_DD']
data_manager = Database_inquiry(ruta_db)

apikey = app.config['API_KEY']

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/api/v1/trading/<crypto_from>/<crypto_to>/<amount_from>", methods=['GET'])
def trading(crypto_from,crypto_to, amount_from):
    crypto_value = CryptoValueModels(apikey, crypto_from, crypto_to)
    balance = crypto_value.checkBalance(crypto_from)
    
    try:
        if balance >= float(amount_from) or crypto_from == 'EUR':
            rate = crypto_value.calculate_rate(float(amount_from))
            return {
            "status": "success",
            "data": {
                "trading": rate
                }
            }
            
        elif crypto_from != 'EUR' and balance >= float(amount_from):
            rate = crypto_value.calculate_rate(float(amount_from))
            return {
            "status": "success",
            "data": {
                "trading": rate
                }
            }
        else:
            return {
                'status': 'error',
                'message': 'Not enough balance'
                }
    except Exception:
        return {'status': 'error', 
                'message': 'The API is having some problems. Please,try again later'
                }  


@app.route("/api/v1/save_exchange", methods=["POST"])
def save_exchange():
    data = json.loads(request.data)
    date= Database_inquiry.date_now()
    time = Database_inquiry.time_now()

    try:
        data_manager.save_data((date,
                                time,
                                data['crypto_from'], 
                                data['amount_from'], 
                                data['crypto_to'], 
                                data['amount_to'],
                                 ))
        return {'status': 'success'}, 201
    except sqlite3.Error :

        return {'status': 'error', 
                'message': 'The database is having some problems. Please,try again later'
                }, 400


@app.route("/api/v1/trading_history")
def trading_history():   
    try:
        data = data_manager.get_data()
        return jsonify(data)
    
    except sqlite3.Error:

        return {'status': 'error', 
                'message': 'The database is having some problems. Please, try again later'
                }, 400

@app.route("/api/v1/wallet", methods=['GET'])
def get_wallet():   

    try:
        allCurrencies = data_manager.getAllCurrencies()
        balanceToTotal = data_manager.getBalanceToTotal()
        balanceFromTotal = data_manager.getBalanceFromTotal()

        wallet = []
        for currency in allCurrencies:
            totalValueTo = [c for c in balanceToTotal if c['crypto_to'] == currency['crypto']] or [{'amount_to': 0}]
            totalValueFrom= [c for c in balanceFromTotal if c['crypto_from'] == currency['crypto']] or [{'amount_from': 0}]
            total = totalValueTo[0]['amount_to'] - totalValueFrom[0]['amount_from']
            wallet.append({'crypto': currency['crypto'], 'amount': total})

        invested = [c for c in wallet if c['crypto'] == 'EUR'] or [{'amount': 0, 'crypto': 'EUR'}]
        amount_value =[a_dict['amount'] for a_dict in invested]
        invested_value = amount_value[0]
    

        totalValue = 0
        for mycrypto in wallet:
            if mycrypto['crypto'] != 'EUR':
                checkValue = CryptoValueModels(apikey, mycrypto['crypto'], 'EUR')
                totalValue = totalValue + checkValue.calculate_rate(mycrypto['amount'])
        
        
        earnings = totalValue + invested_value
        my_wallet = {
            'total_value': totalValue,
            'invested': invested_value,
            'earnings': earnings
            }


        return jsonify(my_wallet)
    except Exception:
            return {'status': 'error', 
                    'message': 'The API is having some problems. Please,try again later'
                }  


