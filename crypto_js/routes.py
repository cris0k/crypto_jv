from crypto_js import app
from flask import render_template, jsonify, request
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

@app.route("/api/v1/trading/<string:crypto_from>/<string:crypto_to>/<amount_from>", methods=['GET'])
def trading(crypto_from,crypto_to, amount_from):
  crypto_value = CryptoValueModels(apikey, crypto_from, crypto_to)
  rate = crypto_value.calculate_rate(Decimal(amount_from))
  # Dictionary to JSON Object using dumps() method
  # # Return JSON Object
  
  return {
        "status": "success",
        "data": {
            "trading": rate
            }
        }
 

@app.route("/api/v1/save_exchange", methods=["POST"])
def save_exchange():
    data = json.loads(request.data)
    date= Database_inquiry.date_now()
    time = Database_inquiry.time_now()
    
    print(date,time,data)

    try:
        data_manager.save_data((date,time,
                                data['crypto_from'], 
                                data['amount_from'], 
                                data['crypto_to'], 
                                data['amount_to'],
                                 ))
        return jsonify({'status': 'success'})
    except sqlite3.Error as e:
        return jsonify({'status': 'error', 'msg': str(e)})