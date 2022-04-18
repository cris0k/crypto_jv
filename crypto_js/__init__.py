from flask import Flask


app = Flask(__name__, instance_relative_config=True)
app.config.from_object("config")

import crypto_js.routes

GET_RATE_COINAPI = "https://rest.coinapi.io/v1/exchangerate/{}/{}?apikey={}"

CRYPTO = ['EUR', 'BTC', 'ETH', 'BNB', 'ADA', 'USDT', 'MATIC', 'LUNA','SOL','ATOM']
