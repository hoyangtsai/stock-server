from flask import render_template, jsonify
from flask_cors import CORS
from datetime import datetime
from . import app
from FinMind.data import DataLoader
from dotenv import load_dotenv
import yfinance as yf
import os

load_dotenv()  # Load variables from .env file

finMind_api_token = os.getenv("FinMind_API_TOKEN")

CORS(app) 

@app.route("/")
def home():
    return "Hello, there!"

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )

@app.route("/stock/<code>")
def stock_info(code = None):
    if code is not None:
        current_year = datetime.now().year
        range = 10 # looking back for 10 years
        begin_year = current_year - range
        try:
            api = DataLoader()
            api.login_by_token(api_token=finMind_api_token)
            df = api.taiwan_stock_dividend(
                stock_id=code,
                start_date=str(begin_year)+'-01-01',
            )
            json_data = df.to_dict(orient='records')
            return jsonify({
                'message': 'success',
                'data': json_data,
            })
        except Exception as e:
            print("An error occurred:", e)
            return jsonify({
                'message': 'error',
            })
    return jsonify({'message': 'code required'})


@app.route("/yf/<code>")
def yf_stock_info(code = None):
    if code is not None:
        try:
            date = '2021-01-01'
            stock_no = str(code)+'.TW'
            stock = yf.Ticker(stock_no)
            dividend = stock.dividends
            print(dividend)
        except Exception as e:
            print("An error occurred:", e)
            return jsonify({
                'message': 'error',
            })
    return jsonify({'message': 'code required'})