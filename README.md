# CRYPTO_JS

## Description

Crypto_js is an application which allows you to see real-time crypto value.\
You are also able to buy and sell your assets and have all your transaction and values shown on a table,\
just remember these will not be real transacrions.


# INSTRUCTIONS TO RUN

## Clone the repository
After you have chosen where will you save the application in your terminal, copy this command to clone the repository:

```
git clone https://github.com/cris0k/crypto_jv.git
```
Then go to the folder:

```
cd crypto_js
```
## Create the virtual environment and activate it (Optional)

In your terminal, type the following commands:

```
python -m venv venv
```
```
. venv/bin/activate
```

## Install application's dependencies

```
pip install -r requirements.txt
```

## Create database

Go to **data** folder and create a database file:

Type in your terminal:

```
cd data/
```

```
sqlite3 history.db
```

After that copy the code from my **sql_table.sql** file,\
which is the database's structure and paste in your terminal.\
Press **Enter** to save it.

## Close database

```
.q
```

```
cd ..
```

## Edit files

Go to **.env_template** and choose **FLASK_ENV** environment.

```
nano .env_template
```
Then copy  **.env_template** as **.env** to rename it.

```
cp .env_template .env
```
## Configuration

Go to **config_template.py**.
```
nano config_template.py
```

Type the database path on **BB_DD** .If you followed the instruction without making any changes copypaste:

```
data/history.db
```

Type your **APIKEY** from CoinAPI. You can get it in the following link:

> [CoinAPI.io](https://www.coinapi.io/)

Type your **SECRET_KEY**

Finally, copy and rename your **config_template** file to **config.py**:

```
cp config_template.py config.py
```

## Start

To run the application, type on your terminal:

```
flask run
```

**Note** : To run it in virtual environment ,make sure you have activated it before running Flask