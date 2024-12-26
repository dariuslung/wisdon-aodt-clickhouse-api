from flask import Flask, jsonify
from flask_restx import Resource, Api
from flasgger import Swagger
import json
import pandas as pd
from clickhouse_driver import Client

# Flask app
app = Flask(__name__)
api = Api(app)

# Configurations
class Config:
    clickhouse_host='localhost'
    retry = 5
    delay = 10

# Swagger
app.config['SWAGGER'] = {
    "title": "AODT Clickhouse API",
    "description": "",
    "version": "1.0.0",
    "termsOfService": "",
    "openapi": "3.0.2",
    "hide_top_bar": True
}

swag = Swagger(app, template_file = 'openapi.yml')

# API
@api.route('/throughput/<string:database>')
class UE(Resource):
    def get(self, database):
        # Clickhouse client with specified database
        client = Client(host=Config.clickhouse_host, database=database)

        # clickhouse-driver ignores FORMAT clause
        data = client.execute_iter("SELECT * FROM ues", with_column_types=True)
        columns = [column[0] for column in next(data)]

        # Pandas process column key and value pairs
        df = pd.DataFrame.from_records(data, columns=columns)
        json_result = df.to_json(orient='records')

        # print(json_result)
        return jsonify(json_result)