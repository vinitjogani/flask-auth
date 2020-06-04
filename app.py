import flask
from db import db
import auth

app = flask.Flask(__name__, static_folder='static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sample.db'
app.config['SECRET_KEY'] = b'\x93(V\xfd\xc3\x12\xf5\xd7\xa2\x0b\x01\xe8\xd6\xa9\xe1\x92\x97\xfa\x00C\xcc*\xcb\xfen\x16\xda\xe0'

db.app = app
db.init_app(app)

app.register_blueprint(auth.blueprint, url_prefix='/auth')

if __name__ == "__main__":
    app.run(debug=True)
