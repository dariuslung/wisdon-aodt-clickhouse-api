from flask import Flask, jsonify
from flask_restx import Resource, Api
from flasgger import Swagger
import json
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
        result = client.execute("SELECT * FROM ues FORMAT JSON")
        print(result)
        return jsonify(result)