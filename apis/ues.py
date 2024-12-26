from flask_restx import Namespace, Resource, fields
from flask import jsonify
from .config import ClickhouseConfig
from clickhouse_driver import Client
import pandas as pd

api = Namespace('ues', description='User equipment related operations')

# API
@api.route('/throughput/<string:database>')
@api.param('database', 'The database identifier')
class UE_Throughput(Resource):
    @api.doc('get_ue_throughput')
    def get(self, database):
        # Clickhouse client with specified database
        client = Client(host=ClickhouseConfig.host, database=database)

        # clickhouse-driver ignores FORMAT clause
        data = client.execute_iter("SELECT * FROM ues", with_column_types=True)
        columns = [column[0] for column in next(data)]

        # Pandas process column key and value pairs
        df = pd.DataFrame.from_records(data, columns=columns)
        json_result = df.to_json(orient='records')

        # print(json_result)
        return jsonify(json_result)