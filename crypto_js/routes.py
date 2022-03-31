from crypto_js import app
from flask import render_template, jsonify, request

@app.route("/")
def inicio():
    return render_template("index.html")