from flask import render_template, jsonify
from flask_cors import CORS
from datetime import datetime
from . import app
from FinMind.data import DataLoader
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env file

finMind_api_token = os.getenv("FinMind_API_TOKEN")

CORS(app) 

@app.route("/")
def home():
    return "Hello, Flask!"

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
        range = 20
        year_gap = current_year - range
        try:
            api = DataLoader()
            api.login_by_token(api_token=finMind_api_token)
            df = api.taiwan_stock_dividend_result(
                stock_id=code,
                start_date=str(year_gap)+'-01-01',
            )
            json_data = df.to_dict(orient='records')
            return jsonify({
                'message': 'ok',
                'data': json_data,
            })
        except Exception as e:
            print("An error occurred:", e)
            return jsonify({
                'message': 'error',
            })
    return jsonify({'message': 'code required'})