from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.utils import import_string
import pymysql

from Blog.Auth.init import auth
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:baggiovinci2@127.0.0.1:3306/NEW'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

db = SQLAlchemy(app)
db.init_app(app)

app.register_blueprint(auth, url_prefix="/auth")


if __name__ == '__main__':
    app.run(debug=True)