from flask_restx import Api

from .ues import api as ues

api = Api(
    title='AODT Clickhouse API',
    version='0.1',
    description='WiSDONLab',
)

# Add api namespaces to api
api.add_namespace(ues)