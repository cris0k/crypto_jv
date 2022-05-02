from crypto_js import GET_RATE_COINAPI, CRYPTO
from crypto_js.errors import APIError, CONNECT_ERROR
import sqlite3
import requests
import json
from decimal import Decimal
from datetime import datetime

class CryptoValueModels:
    def __init__(self, apikey, crypto_from = "", crypto_to = ""):
        self.apikey = apikey
        self.crypto_from = crypto_from
        self.crypto_to = crypto_to

        self.rate = 0

    def get_rate(self):

        # with open('crypto_js/mock.json') as json_file:
        #     answer = json.load(json_file)

        try:
            answer = requests.get(GET_RATE_COINAPI.format(
                self.crypto_from,
                self.crypto_to,
                self.apikey
            ))
        except:
            raise APIError(CONNECT_ERROR)            

        if answer.status_code != 200:
            #raise APIError(respuesta.status_code, respuesta.json()["error"])
            raise APIError(answer.status_code)

        self.rate = Decimal(answer.json()["rate"])
    
    def calculate_rate(self,amount_from=1):
        self.get_rate()
        amount_to= amount_from*self.rate
        return amount_to

class Database_inquiry:
    def __init__(self, file=":history.db:"):
        self.all_data = file 
 
 
    def create_table(self,cur):
        rows = cur.fetchall()

        field = []
        for item in cur.description:
            field.append(item[0])

            result = []
        
        for row in rows:
            registry = {}
            for key, value in zip(field, row):
                registry[key] = value
                
            result.append(registry)

        return result
    
    def results(self,cur,con):

        if cur.description:
            result = self.create_table(cur)
        else:
            result = None
            con.commit()
        return result
    
    def get_exchange_data(self, inquiry, params =[]):
        con = sqlite3.connect(self.all_data)
        cur = con.cursor()

        cur.execute(inquiry, params)

        result = self.results(cur,con)

        con.close()

        return result
    
    
    def date_now():
        now = datetime.today()
        date = now.strftime("%d/%m/%y")
        return date

    def time_now():
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        return time

    def save_data(self, params=[]):
        con = sqlite3.connect(self.all_data)
        cur = con.cursor()

        cur.execute(

                    """ INSERT INTO history (date, time, crypto_from, amount_from,crypto_to, amount_to)
                                    values (?, ?, ?, ?, ?, ?) """
                    , params)
        con.commit()
        con.close()
    
    def get_data(self):
        return self.get_exchange_data("""
                        SELECT id, date, time, crypto_from, amount_from, crypto_to, amount_to
                        FROM history
                        ORDER BY id
                    """
        )




    """ # ESTO ES EN EL MODELO
    # Distinguir si es EUR o no la divisa from_moneda. si es Euro grabo en la bbdd
    # Si no es Eur
    # Obtengo el saldo de la BBDD de la divisa from_moneda del usuario (mockear) y compruebo que sea igual o mayor a from_cantidad
    # Grabar BBDD con fecha y hora
    # Si no "mensaje": "No tienes suficiente saldo de {divisa_from}"   """ 

        








