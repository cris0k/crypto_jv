from crypto_js import GET_RATE_COINAPI
from crypto_js.errors import APIError
import sqlite3
import requests
from datetime import datetime
from crypto_js import app

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
        return self.get_exchange_data(

                    """ INSERT INTO history (date, time, crypto_from, amount_from,crypto_to, amount_to)
                                    values (?, ?, ?, ?, ?, ?) """
                    , params)
    
    def get_data(self):
        return self.get_exchange_data("""
                        SELECT id, date, time, crypto_from, amount_from, crypto_to, amount_to
                        FROM history
                        ORDER BY id
                    """
        )
    def getBalanceTo(self, currency):
        
        return self.get_exchange_data("""
                        SELECT
                            crypto_to,
                            SUM(amount_to) as 'amount_to'
                            FROM
                            history
                            WHERE
                            crypto_to = ?
                            GROUP BY
                            crypto_to
                    """, (currency,)
        )
    def getBalanceFrom(self, currency):
        
        return self.get_exchange_data("""
                        SELECT
                            crypto_from,
                            SUM(amount_from) as 'amount_from'
                            FROM
                            history
                            WHERE
                            crypto_from = ?
                            GROUP BY
                            crypto_from
                    """, (currency,)
        )

    def getBalanceFromTotal(self):
    
        return self.get_exchange_data("""
                        SELECT
                            crypto_from,
                            SUM(amount_from) as 'amount_from'
                            FROM
                            history
                            GROUP BY
                            crypto_from
                    """
        )

    def getBalanceToTotal(self):

        return self.get_exchange_data("""
                        SELECT
                            crypto_to,
                            SUM(amount_to) as 'amount_to'
                            FROM
                            history
                            GROUP BY
                            crypto_to
                    """
        )

    def getAllCurrencies(self):

        return self.get_exchange_data("""
                        SELECT
                            crypto_to as crypto
                        FROM
                            history
                        GROUP BY
                            crypto_to
                        UNION
                        SELECT
                            crypto_from
                        FROM
                            history
                        GROUP BY
                            crypto_from
                    """
        )

ruta_db = app.config['BB_DD']
data_manager = Database_inquiry(ruta_db)

class CryptoValueModels:
    def __init__(self, apikey, crypto_from = "", crypto_to = ""):
        self.apikey = apikey
        self.crypto_from = crypto_from
        self.crypto_to = crypto_to

        self.rate = 0

    def get_rate(self):
        try:
            answer = requests.get(GET_RATE_COINAPI.format(
            self.crypto_from,
            self.crypto_to,
            self.apikey
            ))
            
            self.rate = answer.json()["rate"]
        except:
            raise APIError(answer.status_code)
            
            
    def calculate_rate(self,amount_from=1):
        self.get_rate()

        
        amount_to = amount_from*self.rate
        return amount_to
    
    def checkBalance(self, currency):
        getbalanceFrom = data_manager.getBalanceFrom(currency)
        getbalanceTo = data_manager.getBalanceTo(currency)

        if not getbalanceTo:
            balance = 0

        elif not getbalanceFrom:
            balance = getbalanceTo[0]['amount_to']
        else:
            balanceFrom = getbalanceFrom[0]['amount_from']
            balanceTo = getbalanceTo[0]['amount_to']
            balance = balanceTo - balanceFrom
        return balance

    








