from flask import Flask
from apis import api

# Flask app
app = Flask(__name__)
api.init_app(app)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 2980, debug = True)