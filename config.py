from flask import Flask, jsonify
from flask_restx import Resource, Api
from flasgger import Swagger
import json
import clickhouse_connect

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
@api.route('/ue/<string:database>')
class UE(Resource):
    def get(self, database):
        # Clickhouse client with specified database
        client = clickhouse_connect.get_client(host=Config.clickhouse_host, database=database)
        result = client.query("SELECT * FROM ues FORMAT JSONEachRow")
        print(result.result_rows)
        return jsonify(result.result_rows)